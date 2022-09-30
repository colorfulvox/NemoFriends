# Backend

## 가상환경 생성 및 기본 실행
* backend 폴더 내부에 venv 폴더 생성
```
# 가상 환경 생성
python -m venv venv
```
* 가상환경 실행
```
source venv/Scripts/active
```
* requirements.txt에 있는 module 다운로드
```
pip install -r requirements.txt
```

* 서버실행
```
python manage.py runserver
```
* 현재 적용 모듈 확인
```
pip list
```

## Redis 설치 및 다프네로 서버 구동

* Redis 설치
  * [Redis 공식홈페이지 링크](https://redis.io/download/)
  * 위 링크를 통해 최신버전 다운로드

* build 명령어
```
daphen -b 0.0.0.0 -p 8000 educolab.asgi:application
```

## .env 파일
* 주의할 점 : 변수명 뒤에 띄어쓰기 없이 = 과 내용을 붙여야합니다.
```
SECRET_KEY='django SECRETKEY'
DEBUG=True
DB_NAME='사용하는 데이터베이스 이름'
DB_USER='사용하는 데이터베이스 유저 이름'
DB_PASSWORD='사용하는 데이터베이스 비밀번호'
DB_HOST='사용하는 데이터 베이스 HOST'
DB_PORT='사용하는 데이터 베이스 PORT'
EMAIL_HOST_USER='이메일 인증 시 메일 보내는 이메일'
EMAIL_HOST_PASSWORD='이메일 인증 시 메일 보내는 이메일 비밀번호’
```