# -*- coding: utf-8 -*-
import sys
import json
import traceback
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.utils.encoding import iri_to_uri
from .models import Image, MS_API
import time
import os
import requests
import cv2
import dlib
from concurrent.futures import ThreadPoolExecutor
from imutils import face_utils
from django.contrib import messages
from collections import OrderedDict
# from scipy import misc
# scipy.misc의 imread는 deprecated and removed after v 1.2.0
import imageio
import numpy as np


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_valid(request):
    arrs = ['age','height', "weight",'country','ethnicity','gender']
    for i in arrs:
        if len(request.POST.getlist(i)) == 0:
            print("invalid input error in "+ str(i))
            raise ValueError
    return
    
    

def main(request):
    # 이미지 입력을 POST로 받았을 경우
    if request.method == 'POST':
        # 로컬에 이미지 저장 (교수님 요청)
        fs = FileSystemStorage()
        myfile = request.FILES['photo']
        myfile_name = iri_to_uri(myfile.name)
        filename = fs.save(myfile_name, myfile)
        uploaded_file_url = os.path.join(settings.MEDIA_ROOT, filename)
       

        try:
            # request로 잘못된 요청이 들어오지는 않았는지 체크
            is_valid(request)

            l, f, fwhr_index, face_coord = fWHR(uploaded_file_url)
            l = fs.url(l)[6:]
            f = fs.url(f)[6:]
            
            age = int(request.POST.getlist('age')[0])
            height = float(request.POST.getlist('height')[0])
            weight = float(request.POST.getlist('weight')[0])
            country = request.POST.getlist('country')[0]
            ethnicity = request.POST.getlist('ethnicity')[0]
            gender = request.POST.getlist('gender')[0]
            occupation = request.POST.getlist('occupation')[0]


            image = Image.objects.create()
            image.image = filename
            image.gender = gender
            image.age = age
            image.ethnicity = ethnicity
            image.height = height
            image.weight = weight
            image.country = country
            image.occupation = occupation
            image.ip = get_client_ip(request)
            image.face_coord = json.dumps(face_coord)
            percentile, num_gt_entries, num_total = get_percentile(fwhr_index)
            
            # POST로 들어온 이미지값을 DB에 저장
            image.fwhr = fwhr_index
            image.save()

            # 교수님 요청으로 Azure의 Face Recognition API를 사용한 바 있음.
            # 2020년 1월 이후로 쓰지 않음.
            # get_ms_api = None
            get_ms_api = faceAPI(uploaded_file_url)
            if get_ms_api != None:
                ms_api = MS_API.objects.create()
                ms_api.image = filename
                # ms_api.faceid = get_ms_api['FaceId']
                ms_api.gender = get_ms_api['Gender']
                ms_api.age = get_ms_api['Age']
                ms_api.smiles = get_ms_api['Smiles']
                ms_api.anger = get_ms_api['Anger']
                ms_api.fear = get_ms_api['Fear']
                ms_api.sadness = get_ms_api['Sadness']
                ms_api.happiness = get_ms_api['Happiness']
                ms_api.contempt = get_ms_api['Contempt']
                ms_api.neutral = get_ms_api['Neutral']
                ms_api.surprise = get_ms_api['Surprise']
                ms_api.moustache = get_ms_api['Moustache']
                ms_api.sideburns = get_ms_api['Sideburns']
                ms_api.beard = get_ms_api['Beard']
                ms_api.bald = get_ms_api['Bald']
                ms_api.disgust = get_ms_api['Disgust']
                ms_api.save()

            # 동일한 이름의 이미지가 여러 번 저장될 경우, 중복방지를 위해 이름 맨 끝에 랜덤난수가 생긴다.
            # 파일 이름 뒤에 생긴 랜덤난수 값도 추적해 저장하기 위한 코드
            l,f = l.split("Face_width_height_ratio")[-1], f.split("Face_width_height_ratio")[-1]
            if uploaded_file_url != "".join(l.split("_landmarks")):
                print("".join(l.split("_landmarks")))
                uploaded_file_url = "".join(l.split("_landmarks"))
            
            return render(request, 'main.html', {
                'uploaded_file_url_no_media': myfile.name,
                'uploaded_file_url': uploaded_file_url,
                'landmark_file_url': l,
                'fWHR_file_url': f,
                'fwhr_index': fwhr_index,
                'percentile': percentile,
                'num_gt_entris':num_gt_entries, 'num_total':num_total,
                'get_ms_api':get_ms_api
            })    

        except IndexError:
            # fwhr 함수의 리턴값이 없어서 list index out of range 발생하는 경우.
            # 입력받은 이미지에 사람 얼굴이 1개 이상이거나 없을 때 발생하는 Exception.

            print("Request 보낸 곳: " + get_client_ip(request))
            route = os.path.join(settings.MEDIA_ROOT, filename)
            if os.path.isfile(route):
                os.remove(route)

            traceback.print_exc()
            messages.error(request, "Error: Can't find any face in the Image.\n \
                Possible reason: Too low resolution / Too many Faces / Too small images or faces / etc. ")
            return render(request,'main.html')
        except ValueError:
            # 이름, 나이 등의 input에 형식에 맞지 않는 값을 입력한 경우
            print("Request 보낸 곳: " + get_client_ip(request))
            route = os.path.join(settings.MEDIA_ROOT, filename)
            if os.path.isfile(route):
                os.remove(route)
            traceback.print_exc()
            return render(request,'error.html')
        except:
            # 아직까지 확인하지 못한 기타 에러. 서버가 죽어선 안 되기에, Exception Log만 저장한다.
            route = os.path.join(settings.MEDIA_ROOT, filename)
            if os.path.isfile(route):
                os.remove(route)
            traceback.print_exc()
            return render(request, 'main.html', {})

    return render(request, 'main.html', {})

# 이미지 다운로드 기능을 위한 함수
def image_download(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return render(request, 'main.html')



# MS Azure의 Face API. 현재는 쓰지 않는다.
def faceAPI(image_path):
    image_url = open(image_path,'rb')
    # ip = socket.gethostbyname(socket.gethostname())
    subscription_key = os.environ['MS_API_KEY']
    # "f78920ca9b6242a9ad0fbd48b543ef42"
    assert subscription_key
    face_api_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"

    # columns = ["SerialNum", "Age", "Gender", "Fear", "Sadness", "Disgust", "Contempt", "Neutral", "Happiness", "Anger",
    #            "Glasses", "Moustache", "Beard", "Sideburns", "Bald"]


    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,  
        'Content-type': 'application/octet-stream'
    }

    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur',
    }

    response = requests.post(face_api_url, params=params, headers=headers, data = image_url)

    faces = response.json()
    f = {}

    try:
        features = faces[0]["faceAttributes"]
        f = OrderedDict()
        f['Fear'] = features["emotion"]["fear"]
        f['Sadness'] = features["emotion"]["sadness"]
        f['Neutral'] = features["emotion"]["neutral"]
        f['Surprise'] = features['emotion']['surprise']
        f['Disgust'] = features["emotion"]["disgust"]
        f['Anger'] = features["emotion"]["anger"]
        f['Happiness'] = features["emotion"]["happiness"]
        f['Contempt'] = features["emotion"]["contempt"]
        f['Gender'] = features['gender']
        f['Beard'] = features["facialHair"]["beard"]
        f['Sideburns'] = features["facialHair"]["sideburns"]
        f['Moustache'] = features["facialHair"]["moustache"]
        f['Bald'] = features["hair"]["bald"]
        f['Smiles'] = features['smile']
        f['Glasses'] = features["glasses"]
        f['Age'] = features["age"]

    except:
        return None

    return f

# 데이터베이스에 입력된 fwhr 비율 중 본인의 비율은 상위 몇 %인지를 보여주는 함수
def get_percentile(f_value):
    num_total = Image.objects.all().exclude(fwhr=0.0).count()
    num_gt_entries = Image.objects.filter(fwhr__gt=f_value).count()
    percentile = 100
    if num_total > 0:
        percentile = int(num_gt_entries / num_total * 100)
    return percentile, num_gt_entries, num_total
    



# face width, height 비율을 계산하는 함수
def fWHR(image_url):
    image = cv2.imread(image_url)
    # print("fWHR method loaded image")
    gray = cv2.imread(image_url, 0)
    detector = dlib.get_frontal_face_detector()
    rects = detector(gray, 1)
    rect = rects[0]

    # 얼굴 여러 개면 에러 발생
    if len(rects) > 1:
        raise IndexError

    # pre-trained shape predictor's path
    shape_predictor_path = "media/pretrained/shape_predictor_68_face_landmarks.dat"

    predictor = dlib.shape_predictor(shape_predictor_path)
    shape = predictor(gray, rect)
    face_coord = [(p.x, p.y) for p in shape.parts()]
    shape = face_utils.shape_to_np(shape)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    img_lmrk = image.__copy__()
    for i, sh in enumerate(shape):
        if i in [1, 15, 21, 22, 51]:
            cv2.circle(img_lmrk, (sh[0], sh[1]), 2, (0, 0, 255), 3)
        cv2.circle(img_lmrk, (sh[0], sh[1]), 1, (0, 0, 255), 2)

    cv2.rectangle(image, (shape[1][0], (shape[21][1] + shape[22][1]) // 2), (shape[15][0], shape[51][1]),
                  (0, 0, 255), 3)

    landmark_image_path = "".join(image_url.split(".")[:-1]) + "_landmarks.jpg"
    fwhr_image_path = "".join(image_url.split(".")[:-1]) + "_fwhr.jpg"

    cv2.imwrite(landmark_image_path, img_lmrk)
    cv2.imwrite(fwhr_image_path, image)

    width = ((shape[0][0] - shape[15][0]) ** 2 +
         (shape[0][1] - shape[15][1]) ** 2) ** (0.5)

    avg_21_22 = (shape[21] + shape[22]) / 2.0
    height = ((avg_21_22[0] - shape[51][0]) ** 2 +
          (avg_21_22[1] - shape[51][1]) ** 2) ** (0.5)

    fwhr_index = round(width / height, 7)

    return landmark_image_path, fwhr_image_path, fwhr_index, face_coord