# response
SUCCESS = {"success":True}
FAIL = {"success":False}


# date 포맷 형식
date_format_slash = f'%y/%m/%d/%H/%M/%S'


# gold 보상 처리
def reward_gold(user, action):
    reward = {'eatting': 100, 'level_up': 777, 'talking': 100}
    user.gold += reward[action]
    return user


# exp 보상 처리
def reward_exp(animal, user, action):
    lookup_grade = [1, 1, 1, 2, 2, 3]  # lookup_grade[level] = grade
    levelup_exp = [0, 0, 100, 200, 300, 400, float('inf')]
    reward = {'eatting': 80, 'talking': 50}

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
