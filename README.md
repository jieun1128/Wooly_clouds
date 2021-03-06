# Wooly_Clouds
2021-2 데이터사이언스 캡스톤 디자인

클라우드 시각화 프로젝트

<img width="1033" alt="스크린샷 2021-12-05 오후 9 53 47" src="https://user-images.githubusercontent.com/49158155/144747379-2621afb0-0583-42ff-905a-5bdbb07bcec9.png">

aws의 user access key를 입력받아 <b>인프라간 관계를 시각화하고 인프라 생성 및 수정이 가능한 웹 사이트</b>입니다.

It is a website that can <b>visualize the relationship between infrastructures and create and modify infrastructure</b> by receiving the user access key of aws.

---
## System Architecture
<img width="690" alt="스크린샷 2021-12-05 오후 9 40 58" src="https://user-images.githubusercontent.com/49158155/144746953-058d9f81-abc9-44ca-87be-35f199556bd2.png">

    Backend: Flask, Boto3
    Frontend: html, css, javascript, D3.js
    Middleware: Gunicorn
    etc: Amazon Web Service

---
## Installation
>### Clone Repository

    $git clone git@github.com:jieun1128/Wooly_clouds.git

>### Docker 🐳
    docker-compose up -d 

>### Nginx 
```
http://localhost:8000
```

>### Local
```
WebPage: http://localhost:5000/
Swagger: http://localhost:5000/swagger 
```

---
## Features

```
 이 웹사이트는 인프라 시각화, 인프라 생성 및 수정 총 2가지 기능을 제공하고 있습니다.

1) Tree chart를 이용하여 인프라의 전체적 구조를 보여주며, 특정 인스턴스 선택 시 상세 정보를 확인 가능합니다.

2) 원하는 인프라를 선택하여 정보를 입력하면 새로 생성이 가능합니다.
```
### 1) Infra Visualization
<img width="1432" alt="스크린샷 2021-12-06 오후 11 42 46" src="https://user-images.githubusercontent.com/49158155/144865988-620b68ac-bf1e-4ad6-90ae-39d50460b9cf.png">
- 시각화 창에 들어가면 Tree Chart를 이용하여 인프라의 전체적인 구조를 확인 할 수 있습니다.
<img width="1435" alt="스크린샷 2021-12-06 오후 11 43 17" src="https://user-images.githubusercontent.com/49158155/144866053-830dea83-c886-4a27-8e9f-4a1a14887bd2.png">
- 또한 인스턴스 선택 시 상세 정보를 확인 할 수 있습니다.

### 2) Modify Infratructure
<img width="1431" alt="스크린샷 2021-12-05 오후 10 01 13" src="https://user-images.githubusercontent.com/49158155/144747648-702d282e-8677-4339-910e-95c5fd401cf3.png">
- addInstance창에 들어가서 생성할 인프라 선택 후 정보를 입력하면 새로운 인스턴스 생성이 가능합니다.
<img width="1394" alt="스크린샷 2021-12-07 오전 12 49 08" src="https://user-images.githubusercontent.com/49158155/144877397-93236c64-dedd-475f-ae14-0cab83b7f6d9.png">
- ec2의 경우 상세 정보 창에서 인스턴스 시작/종료 및 삭제가 가능합니다.

---
## Team Member
|김성식|김응민|박지은|오종엽|
|---|---|---|---|
|[**@tjdtlr1114**](https://github.com/tjdtlr1114)|[**@chrismin**](https://github.com/chrismin1205)|[**@jieun1128**](https://github.com/jieun1128)|[**@ojongy**](https://github.com/ojongy)


