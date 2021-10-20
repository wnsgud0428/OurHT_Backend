from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
# 주석 달기
def getRoutes(request):

    routes = [
        {
            'Endpoint': '/users/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of users'
        },
        {
            'Endpoint'
        }
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
# 함수 이름 조금 더 고민
def getUsers(request):
    pass