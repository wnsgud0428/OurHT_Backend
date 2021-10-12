## 초기세팅

1. 한 폴더 안에 backend , frontend 폴더 만들어서 각각 저장소에서 클론

2. Backend / Frontend 폴더 안에서 터미널 따로 실행

- Backend 

    1. backend 폴더 안에서 가상환경 실행 -> pipenv shell

    2. pipenv install -r requirements.txt

    3. python manage.py makemigrations / python manage.py migrate

- Frontend

    1. npm install / npm install react-router-dom / npm install react-webcam
    2. npm run-script build  or  yarn build -> 수정할때마다 해줘야 반영됌!


이후 python manage.py runserver

## 연습 중인 방법

- Post 요청으로 data 전송 시 여러 데이터 담기
ex) 이름, 나이 등등 한번에 보내기

- Image를 캡쳐해서 url 이용해 띄우는 것 까지는 함, 이제 Image를 api 통해 보내기

