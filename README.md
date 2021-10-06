## 초기세팅

1. 한 폴더 안에 backend , frontend 폴더 만들어서 각각 저장소에서 클론

2. Backend / Frontend 폴더 안에서 터미널 따로 실행

- Backend 

    1. backend 폴더 안에서 가상환경 실행 -> pipenv shell

    2. pipenv install -r requirements.txt

    3. python manage.py makemigrations / python manage.py migrate

- Frontend

    1. npm run-script build  or  yarn build -> 수정할때마다 해줘야 반영됌!

이후 python manage.py runserver


