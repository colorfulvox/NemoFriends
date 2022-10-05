# 백엔드 서버 포팅 매뉴얼

본 글은 해당 레포지토리의 서버를 구동하기 위한 Django 설정을 하는 방법을 담고 있는 매뉴얼입니다.

버전 정보

python : 3.10.5
django : 3.2.12
redis : lastest

## 가상환경 생성 및 기본 실행
레포지토리를 내려받으면 먼저 Python 가상환경을 설정해주어야 합니다.

* backend 폴더 내부에 venv 폴더 생성
```
# 가상 환경 생성
python -m venv venv
```

다음은 가상환경으로 접속하는 방법입니다.

* 가상환경 실행
```
source venv/Scripts/active
```

가상환경을 생성하고 접속까지 진행했으면, 이제 requirements.txt에 정의되어있는 서버에 필요한 라이브러리를 설치합니다.
* requirements.txt에 있는 module 다운로드
```
pip install -r requirements.txt
```

서버를 정상적으로 실행하기 위해서는 git에 업로드되지 않도록 설정되어있는 파일 (예: env(Private 정보를 담고있는 파일))들에 대한 설정을 해 줄 필요가 있습니다. 저희 프로젝트에는 .env 파일로 private 데이터를 관리하기 때문에 .env 파일을 작성해줍시다.

프.env 파일 생성
```
SECRET_KEY='django-insecure-d0xo-huf@-+5k......' // 장고에 있는secret.key
DEBUG=True // Debug 모드 설정
DB_NAME='C201' // DB 이름
DB_USER='C201' // DB 유저이름
DB_PASSWORD='*********' // DB 접속 비밀번호
DB_HOST='**********' // DB 접속 주소 IP 또는 도메인
DB_PORT='3306' // DB 접속 포트
VITO_CLIENT_ID='sVyeoEIu.....' // VITO API를 사용하기 위한 ID
VITO_CLIENT_SECRET='bJdGEuaUb17dRi_o......' // VITO API를 사용하기 위한 비밀 키
```

또한 저희 프로젝트에서는 log 파일을 통해 서비스 로그를 저장하기 때문에, Settings.py에 설정되어있는 경로대로 폴더를 만들어 주어야 합니다. Backend 폴더 아래에 files/log 폴더를 생성해주시면 됩니다.

마지막으로 저희 프로젝트는 MYSQL뿐만아니라 Redis Cache DB를 사용합니다. 따라서 로컬 환경에 Redis를 설치해주어야합니다. 이는 윈도우에서 설치하는 방법과, ubuntu에서 Docker Container로써 설치하는 방법으로 나누겠습니다.

1. Windows
* Redis 설치
  * [Redis 공식홈페이지 링크](https://redis.io/download/)
  * 위 링크를 통해 최신버전 다운로드

윈도우 환경에서는 위 링크에서 Redis 최신버전을 다운로드 받고, 설치해주면 됩니다.


2. Ubuntu

```
sudo docker run --rm --name some-redis -d -p 6379:6379 redis
```

CICD 매뉴얼에서 Docker가 설치되어있다는 가정하에 진행하겠습니다. Docker 명령어로 컨테이너 이름은 some-redis, 포트는 6379로 redis 이미지를 이용해서 컨테이너를 생성하는 명령어입니다. 자동적으로 lastest 버전이 컨테이너로 설치됩니다.


이제 서버를 실행하여 정상적으로 작동하는 지 테스트 하면 됩니다.

* 서버실행
```
python manage.py runserver
```

현재 다운되어있는 라이브러리를 체크하려면 다음 명령어를 통해 체크합니다.
* 현재 적용 모듈 확인
```
pip list
```