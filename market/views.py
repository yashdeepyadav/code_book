from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.

@login_required(login_url='profiles')
def addProject(request):
    profile = request.user.profile
    form=ProjectForm()
    context = {'form':form}

    if request.method =='POST':
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner=profile
            project.save()
            messages.success(request,'Project added Successfully')
            return redirect('projects')

    return render(request, 'market/addProject.html',context)

@login_required(login_url='profiles')
def updateProject(request,pk):
    profile = request.user.profile
    project=profile.project_set.get(id=pk)
    form=ProjectForm(instance=project)

    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES,instance=project)

        if form.is_valid:
            form.save()
            messages.success(request,'Project edited Successfully')
            return redirect('projects')

    return render(request,'market/addProject.html',{'form':form})

@login_required(login_url='profiles')
def deleteProject(request,pk):
    profile = request.user.profile
    project=profile.project_set.get(id=pk)

    if request.method =='POST':

        project.delete()

        return redirect('home')


    return render(request,'market/deleteProject.html',{"item":project})
    
def project(request,pk):
    pro=Project.objects.get(id=pk)
    return render(request, 'market/project.html',{'pro':pro})


def projects(request):

    pro=Project.objects.all()
    
    return render(request,'market/projects.html',{'pro':pro})
