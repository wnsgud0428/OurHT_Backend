## 10/20
  - Done
    1. User Model, User Serializer 완성
    2. User url, views, admin 생성 해 놓은 상태

  - To do
    1. User url, views 완성하기
    2. 로그인 기능 완성하기

## 10/21
  - Done
    1. 로그인 함수 로직 구현 완료

  - To do
    1. 웹으로 어떤 응답을 줄껀지, GET, POST 방식 어느게 효율적인지 파악
    2. Feedback, Photo 모델 구현
  
## 10/22
  - Done
    1. Feedback, Photo 모델 구체화, Admin, Serializer 파일도 조금 수정
    2. 피드백 알고리즘 함수 어떻게 짤지 구상중(feedback.py 파일 생성)
    3. 유저 이름을 받아 웹에 유저 정보 전달해주는 getuserinfo 함수 구현 완료

  - To do
    1. 피드백 알고리즘 함수 구현에 필요한 OpenCV, Numpy 등등 라이브러리 익히기
    2. GET, POST 방식 고민 & 모델 구현 또한 계속 고민
    3. 필요한 API 함수들 고민하기

## 10/23
  - Done
    1. 피드백 알고리즘 위한 기초 함수들 제작(util.py에 제작)

  - To do
    2. 10/22일 To do와 동일.

## 10/25
  - Done
    1. OpenCV, numpy 라이브러리 익히기
    2. 피드백 알고리즘 위한 기초 함수 추가 제작

  - To do
    1. 웹으로부터 넘겨져오는 이미지, 관절 포인트 관련 api 제작
    2. 수학적 좌표와 배열 상의 좌표 차이 해결하기
    3. GET, POST 방식 고민 & 모델 구현 또한 계속 고민

## 10/28
  - Done
    1. 관절 포인트 관련 api 제작 중
    2. 피드백 알고리즘 관련 간단 코드 작성
    3. 수학적 좌표로 변환 (Y 좌표만 변경하면 됌)

  - To do
    1. Feedback 모델에 날짜 속성 고민
    2. 알고리즘의 정확성을 높이기 위한 다양한 관절 분석 방법 생각해보기
    3. GET, POST 방식 & 모델 구현 & 더 필요한 api 있는지 계속 고민
    4. 관절 포인트 api에서, 받은 Json 형식 관절 포인트들을 보기좋게 변수에 저장하기