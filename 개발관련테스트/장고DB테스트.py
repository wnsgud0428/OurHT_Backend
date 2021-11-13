'''
from users import models as user_models
user = users_models.User.objects.get(username = username)
print(user)
'''

'''
from exercises import models as exercise_models

# 이러면 모든 모션 담김
querysets = exercise_models.Motion.objects.all()

# 특정 요소 접근 방법
querysets[0].count_number
querysets[0].exercise.user

# 필터 써서 쿼리셋 찾기
queryset = exercise_models.Motion.objects.filter(count_number = 1)
'''