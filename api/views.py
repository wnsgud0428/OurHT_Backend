from django.db.models import base
from .models import User, Image
from .serializer import UserSerializer, ImageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

import base64

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {
            'Endpoint': '/users/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of users'
        },
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
def getUsers(request):
    # 'api/users'으로 온 GET 요청 처리 -> 유저들 목록 반환
    if request.method == 'GET':
        print("Users GET")
        users = User.objects.all().order_by()
        serializer = UserSerializer(users, many=True)
    
    # 'api/users'으로 온 POST 요청 처리 -> 유저 생성
    if request.method == 'POST':
        print("Users POST")
        data = request.data
        print(data)
        user = User.objects.create(name = data)
        serializer = UserSerializer(user, many=False)
    
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def getImages(request):
    # 
    if request.method == 'GET':
        print("Images GET")
        users = Image.objects.all().order_by()
        serializer = ImageSerializer(users, many=True)
    
    # Image 객체 생성
    if request.method == 'POST':
        print("Images POST")
        data = request.data

        # base64를 이미지로 바꿔야함!!
        data = data.encode()
        imgdata = base64.b64encode(data)
        with open('test.jpeg', 'wb') as f:
            f.write(imgdata)
        '''
        binary_data = a2b_base64(data)
        fd = open('test.jpeg', 'wb')
        fd.write(binary_data)
        fd.close()
        
        print("dd")
        image = Image.objects.create(image_url = binary_data)
        serializer = ImageSerializer(image, many=False)
        '''
    # return Response(serializer.data)