#  네모난친구들
<img src="![logo](/uploads/00984e0b3a440152bb0a4119a67c1851/logo.png)" width="250">

### UCC : [링크]()

### 시연 시나리오 : [링크]()

## ✨Overview
1. 인공지능 기술을 접목한 동물 키우기 게임입니다. 주어진 필드를 자유롭게 꾸미고 나만의 동물과 상호작용 해보세요!

## 팀 소개 : 꾸미는 방법 찾아보기

노은영, 전윤희, 조예지, 최용욱, 추희원, 한진성

## 핵심 서비스

### 먹이주기
![선생_013_설문조사_등록](/uploads/1dd1b65146c0f9b696f1ac4dca000f9a/선생_013_설문조사_등록.gif)

### 대화하기
![학생_임베디드__003_설문조사_제출](/uploads/be5d1c289a81ddc4b8c20fea8b30a2a5/학생_임베디드__003_설문조사_제출.gif)

### 놀아주기 - 끝말잇기
![선생_017_설문조사_통계](/uploads/275cf0fd357a5e5410a5f66a44090d3e/선생_017_설문조사_통계.gif)

### 놀아주기 - 미로찾기
![선생_005_과제_등록](/uploads/ae6174c6390b86dd22d4d0b6b300cb06/선생_005_과제_등록.gif)

### 필드 꾸미기
![학생_004_과제_제출](/uploads/d3c93c60a3e82bcc1e6cd7f975e7326a/학생_004_과제_제출.gif)

## 뽑기
![학생_004_과제_제출](/uploads/d3c93c60a3e82bcc1e6cd7f975e7326a/학생_004_과제_제출.gif)

## ✨ 주요 기능
---
- 서비스 설명 : 이미지 분류를 통한 먹이주기, 음성 텍스트 변환(STT)을 이용한 대화하기 등의 기능을 통해 내 동물을 키우고, 그 과정에서 받게 되는 골드를 통해 새 동물이나 조경을 얻어 필드를 꾸밀 수 있습니다.
- 주요 기능 :
    - QuickDraw 데이터셋 을 이용한 낙서 이미지 분류 기능을 통해 동물에게 먹이를 직접 그려서 줄 수 있는 기능
    - STT 모델을 이용한 동물과 대화하기, 끝말잇기 기능
    - 조경을 상점에서 구매하고, 필드에 배치할 수 있는 기능
    - 미로를 돌아다니며 골드를 모을 수 있는 미로찾기 게임

### 개발 환경

---

**AI**
- Jupyter notebook(GPU Server)
- tensorflow-gpu 2.1.0
- Keras 2.10.0
- kospeech
- pytorch 1.12.1
- QuickDraw
- AI HUB 한국어 음성 데이터셋
- VITO
- Googlespeech

**Backend**
- Visual Studio Code
- pyton 3.10.5
- Django 3.2.12
- simple jwt
- mysql 8.0.30
- redis lastest

**Application**

- Visual Studio Code
- Unity 2020.3.38.f1
- Baracuda 1.0.4


**CI/CD**
- AWS EC2 ubuntu 20.04
- docker 20.10.18
- nginx 1.18.0
- jenkins 2.361.1 lts

###각 개발 환경 별 포팅 매뉴얼

App : [링크]()

Backend : [링크]()

### 아키텍쳐 구성도

---

![아키텍쳐 구성도](/uploads/31a3e7022d4965f7348781040e7f73ac/image.png)

### Jenkins를 이용한 CD 구축 및 SSL 인증서 적용

---

백엔드 CICD 배포 및 SSL 인증서 적용 과정은 [여기](https://lab.ssafy.com/s07-webmobile3-sub2/S07P12C102/-/blob/master/CICD.md)에서 설명해두었습니다.

### 특이점

---

- Unity

동물 키우기를 기획하는 도중 아이소매트릭 형태의 디자인 아이디어가 나왔고, 동물에 대해 생동감을 부여해주고 필드를 꾸밀 수 있도록 하기 위해서 3D 화면으로 구현하기로 결정했습니다. three.js, Unity, AndroidStudio 등의 후보를 두고 고민하고 토의를 한 결과 Unity를 사용하는 것으로 결정했습니다.

- Baracuda

Unity에서 AI모델을 사용하기 위해서는 해당 라이브러리를 꼭 사용해야 했습니다. 기존의 Keras나 Pytorch로 학습시킨 모델을 ONNX 파일로 변환하여 Baracuda 라이브러리가 인식할 수 있도록 했고, Baracuda를 이용하여 그림을 인식하는 AI를 구현하였습니다.

- Redis

저희 프로젝트의 기능 중, 끝말잇기의 경우 App과 Backend가 지속적으로 통신하면서 데이터 교환이 이루어집니다. 이 때, 한 게임 씩 단발성으로 진행되는 형태의 게임인 끝말잇기에 관계형 DB를 그대로 사용하는 것은 효율이 떨어지고 속도가 느릴 것이라고 생각했습니다. 중복사용 단어의 처리와 통신속도 향상을 위해서 Redis를 사용하였습니다.

- QuickDraw Model

저희는 AI 음성 팀이지만, 프로젝트 기획 내용에 이미지 처리까지 포함이 되어있었기 때문에 이미지 처리 모델도 학습시켜 만들었습니다. 모든 학습은 SSAFY에서 제공한 GPU 서버에서 진행하였습니다. QuickDraw 데이터셋을 이용한 낙서 인식 모델은 Keras를 이용해 학습시켰습니다. 46만개의 이미지를 5 Epoch만큼 돌렸습니다. GPU서버에서 병렬 처리를 할 수 있도록 설정하여 이미지 학습시간을 21초까지 단축시켰습니다.


- 한국어 음성인식 모델

AI HUB에서 내려받은 한국어 데이터셋을 이용한 STT(Speech to Text) 모델은 Pytorch와 Kospeech를 이용하여 학습시켰습니다. 음성 데이터 양이 1000시간으로, 20 Epoch만큼 돌려 총 학습시간은 220시간이 걸렸습니다. 해당 모델에, Vito 및 GoogleSpeech API를 함께 사용하여 인식이 잘 되는 데이터를 반환하도록 설정했습니다.

- 배포

Docker, Nginx, Jenkins를 이용하여 무중단 자동 배포를 구축하였습니다. Nginx는 Aws에 서버를 띄워 FE를 서비스했고, Django 서버는 도커의 컨테이너로 넣어 AWS EC2의 Nginx에 리버스 프록시로 연결했습니다.



### 협업

---
- Git
- Jira
- Notion
- Mattermost
- Webex
- discode

### ✨Git 컨벤션

---

## 📌 Commit 규칙

<aside>
💡 **#git이슈번호 종류 - 내용(한국어/영어 상관없음)**

</aside>

**예시)** 

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7207e7bd-faba-474f-aa1d-26e2c78f660e/Untitled.png)

**#31 fix 빌드실패 - blob → recordedBlob**

**#31 feat params fd 하나만 보내지말고 applicantNo 추가해서 백엔드에 보내기**

## 📌 종류 (+[깃모지 추가](https://gitmoji.dev/))

- **feat - 기능 추가**

```
 ✨ :sparkles: 기능 추가 Introduce new features.
```

- **fix - 버그 수정**

```
🐛	:bug:	버그 수정	Fix a bug.
```

- **docs - 문서 수정 (README.md)**

```
📝 :memo: 문서 추가/수정 Add or update documentation.
```

- **style - 스타일 관련 기능(코드 포맷팅, 세미콜론 누락, 코드 자체의 변경이 없는 경우)**

```
🎨 :art: 코드의 구조/형태 개선 Improve structure / format of the code.
```

- **refactor - 코드 리팩토링**

```
♻️ :recycle: 코드 리팩토링 Refactor code.
```

- **test - 테스트 코드**

```
✅ :white_check_mark: 테스트 추가/수정 Add or update tests.
```

- **database - DB 관련 작업**

```
🗃️ :card_file_box: DB 관련 작업 Perform database related changes.
```

- **simple_fix - 심플 이슈 수정**

```
🩹 :adhesive_bandage: 심플 이슈(오타 등) 수정 Simple fix for a non-critical issue.
```

- **comments - 주석**

```
💡 :bulb: 주석 추가 및 수정 Add or update comments in source code.
```

- **catch - 에러 해결**

```
🥅 :goal_net: 에러 잡음 Catch errors.
```

- **chore - 빌드 업무 수정, 패키지 매니저 수정(ex .gitignore 수정 같은 경우)**

```
🙈 :see_no_evil: .gitignore 추가/수정 Add or update a .gitignore file.
```

- **delete - 코드/파일 삭제**

```
🔥 :fire: 코드/파일 삭제 Remove code or files.
```

- **improve - 개선할 필요가 있는 코드**

```
💩  :poop: 똥싼 코드 Write bad code that needs to be improved.
```

`**깃모지 출처**: [https://inpa.tistory.com/entry/GIT-⚡️-Gitmoji-사용법-Gitmoji-cli](https://inpa.tistory.com/entry/GIT-%E2%9A%A1%EF%B8%8F-Gitmoji-%EC%82%AC%EC%9A%A9%EB%B2%95-Gitmoji-cli)`

**~~(제목과 본문은 필자도 잘 안지켰긴 한데 회의 후 확실히 정하는 걸로 합시다!)~~**

### 제목

1. 제목과 본문을 `빈 행으로 구분`한다.
2. 제목 첫 글자는 `대문자`로 작성.
3. 제목은 `명령문`으로 사용하며 과거형을 사용하지 않는다.

### 본문

1. `72자 단위로 개행`한다.
2. 양에 구애 받지 않고 `최대한 상세히 작성`
3. 어떻게 했는지 보다는 `무엇을` 바꾸었고 `왜` 바꿨는지 설명

## 📌 GIT FLOW

- Main: 배포
- Develop: BE, FE를 모두 합쳐서 Master 브랜치에 배포
- FrontEnd : Feature합쳐서 develop에 배포
- BackEnd : Feature합쳐서 develop에 배포
- Feature : 각 기능들 (보통 FrontEnd와 BackEnd에서 브랜치가 나눠진다. 예를 들어, 브랜치 이름은 Frontend_기능명으로 통일하기로 한다.)

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/605413d7-2b9d-4639-8ed0-84a386d25a9e/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/605413d7-2b9d-4639-8ed0-84a386d25a9e/Untitled.png)

###  ER Diagram

---

![ERD](/uploads/53e58cf572132880d670c9944203a78b/image.png)

- ERD입니다.
