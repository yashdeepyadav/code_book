from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from market.models import Project



@api_view(['GET'])
def getRoutes(self):

    routes=[
        {"GET":"/projects/"},
        {"GET":"/projects/project/<id>"},
    ]


    return Response(routes)

@api_view(['GET'])
def getProjects(self):

    projects=Project.objects.all()
    serializer=ProjectSerializer(projects,many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getProject(request,pk):

    project=Project.objects.get(id=pk)

    serializer=ProjectSerializer(project,many=False)

    return Response(serializer.data)