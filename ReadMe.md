# Face Width Height Ratio

성균관대학교 글로벌경영학과 김영한 교수님 Research Assistant HaileyPARK, Donggeon Lee 작업.

* HaileyPARK : OpenCV의 Face shape predictor landmark을 사용한 fwhr 측정코드 작성, Frontend css 및 js 작업. (~ 2019.10)
* Donggeon Lee : views.py 디버깅, nginx와 gunicorn 활용해 AWS EC2에 Deploy 완료, AWS RDS로 데이터 수집 및 관리. 유지보수 작업 진행중 (2019.11 ~)

현재 운영되는 페이지는 http://fwhrmeasuring.com 로 확인할 수 있습니다.

---

1. input 박스에 필요한 데이터를 입력하고, 사람 한 명의 얼굴이 담긴 이미지를 업로드한다.

<img width="1261" alt="스크린샷 2020-04-01 오후 2 56 42" src="https://user-images.githubusercontent.com/26548454/78104033-5e222a80-7429-11ea-9cbb-04f6a4d9b76c.png">


2. Face Width / height 비율을 측정해 값을 알려주며, 지금까지 측정된 사람들의 비율 중 상위 몇 %에 해당하는지를 반환한다.


<img width="1212" alt="스크린샷 2020-04-01 오후 2 57 08" src="https://user-images.githubusercontent.com/26548454/78104108-83af3400-7429-11ea-8426-2b731d5a4262.png">

---


*The face of risk: CEO facial masculinity and firm risk* 라는 주제로 2018년에 발표한 논문의 Python 구현.

https://onlinelibrary.wiley.com/doi/abs/10.1111/eufm.12175
