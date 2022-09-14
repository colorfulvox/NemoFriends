# response
SUCCESS = {"success":True}
FAIL = {"success":False}

# date 포맷 형식
date_format_slash = f'%y/%m/%d/%H/%M/%S'

# level 및 exp
def level_up(exp, cur_level):
    '''
    경험치 확인 후 레벨업 여부를 돌려주는 함수 
    - 레벨업이 필요하면 True
    - 레벨업이 필요없으면 False
    '''
    need_exp = [0, 1000, 2000, float('inf')]

    for i in range(1, len(need_exp)):
        if exp < need_exp[i]:
            return i - 1
    raise Exception('레벌업 처리에서 오류가 발생했습니다.')