from django.core.files.storage import FileSystemStorage
from django.conf import settings

import speech_recognition as sr
import json
import requests
import time
import os

# date 포맷 형식
date_format_slash = f'%y/%m/%d/%H/%M/%S'

# 전체 명령어 리스트
ALL_COMMANDS = ['', '얘들아']

# STT
VITO_URL = 'https://openapi.vito.ai/v1/'
data={'client_id': os.environ.get('VITO_CLIENT_ID'),
        'client_secret': os.environ.get('VITO_CLIENT_SECRET')}

resp = requests.post(VITO_URL+'authenticate', data=data)
resp.raise_for_status()

vito_access_token = resp.json().get('access_token')
vito_refresh_token = resp.json().get('refresh_token')

def vito_stt_api(filename):
    config = {
    "diarization": {
        "use_ars": False,
        "use_verification": False
    },
    "use_multi_channel": False
    }
    resp = requests.post(
        VITO_URL+'transcribe',
        headers={'Authorization': 'bearer '+ vito_access_token},
        data={'config': json.dumps(config)},
        files={'file': open(f'{settings.MEDIA_ROOT}/{filename}', 'rb')}
    )
    resp.raise_for_status()
    id = resp.json().get('id')

    while True:
        resp = requests.get(
        VITO_URL + 'transcribe/' + id,
        headers={'Authorization': 'bearer '+ vito_access_token},
        )
        resp.raise_for_status()

        if resp.json().get('status') == 'completed':
            break
        time.sleep(0.5)

    result = ''

    for msg in resp.json().get('results').get('utterances'):
        result = result + msg.get('msg')

    return result

def google_stt_api(filename):
    r = sr.Recognizer()
    audio_file = sr.AudioFile(f'{settings.MEDIA_ROOT}/{filename}')

    with audio_file as source:
        audio = r.record(source)

    result = r.recognize_google(audio, language='ko-KR')
    return result


def speech_to_text(data=None):
    try:
        data = google_stt_api(data)
    except:
        data = vito_stt_api(data)
    return data


# 음성 임시 저장 -> STT -> 삭제
def recongize(username, audio):
    fs = FileSystemStorage()
    filename = fs.save(f'{username}.wav', audio)

    context = speech_to_text(filename)
    print('STT 결과입니다.', context)

    fs.delete(filename)
    fs.delete(settings.MEDIA_ROOT + f'/{filename}.wav')
    return context


# gold 보상 처리
def reward_gold(user, action, score=0):
    reward = {'eatting': 100, 'level_up': 777, 'talking_one': 100, 'talking_all': 100, 'playing': 50 * score}
    user.gold += reward[action]
    return user


# exp 보상 처리
def reward_exp(animal, user, action, score=0):
    lookup_grade = [1, 1, 1, 2, 2, 3]  # lookup_grade[level] = grade
    levelup_exp = [0, 0, 100, 200, 300, 400, float('inf')]
    reward = {'eatting': 80, 'talking_one': 50, 'playing': 5 * score}
    
    exp = animal.exp + reward[action]
    next_level = animal.level + 1

    if levelup_exp[next_level] <= exp:
        user = reward_gold(user, 'level_up')
        user.save()
        exp -= levelup_exp[next_level]
        animal.level = next_level
        animal.grade = lookup_grade[next_level]

    animal.exp = exp
    return animal


# 끝말잇기
# 두음 법칙 경우의 수
convert_dict = {
    "라":"나", "락":"낙", "란":"난", "랄":"날", "람":"남", "랍":"납", "랏":"낫", "랑":"낭",
    "략":"약", "량":"양",
    "렁":"넝",
    "려":"여", "녀":"여", "력":"역", "녁":"역",
    "련":"연", "년":"연", "렬":"열", "렴":"염", "념":"염", "렵":"엽", "령":"영", "녕":"영", 
    "로":"노", "록":"녹", "론":"논", "롤":"놀", "롬":"놈", "롭":"놉", "롯":"놋", "롱":"농", 
    "료":"요", "뇨":"요", "룡":"용", "뇽":"용", 
    "루":"누", "룩":"눅", "룬":"눈", "룰":"눌", "룸":"눔", "룻":"눗", "룽":"눙",
    "류":"유", "뉴":"유", "륙":"육", "률":"율", 
    "르":"느", "륵":"늑", "른":"는", "를":"늘", "름":"늠", "릅":"늡", "릇":"늣", "릉":"능", 
    "래":"내", "랙":"낵", "랜":"낸", "랠":"낼", "램":"냄", "랩":"냅", "랫":"냇", "랭":"냉", 
    "례":"예", 
    "뢰":"뇌", 
    "리":"이", "니":"이", "린":"인", "닌":"인", "릴":"일", "닐":"일", "림":"임", "님":"임", "립":"입", "닙":"입", "릿":"잇", "닛":"잇", "링":"잉", "닝":"잉" 
    }

# 시작 단어로 쓰기 안 좋은 단어 확인
blacklist = ['즘', '틱', '늄', '슘', '퓸', '늬', '뺌', '섯', '숍', '튼', '름', '늠', '쁨']

print('여기는 animals의 utils.py입니다.')