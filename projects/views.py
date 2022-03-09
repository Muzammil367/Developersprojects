from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse 
import datetime
from projects.models import Project,Review,Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

projectsList = [
    {
        'id': '1',
        'title': 'Ecommerce Website',
        'description': 'Fully functional commerce website'
    },
    {
        'id': '2',
        'title': 'Portfolio Website',
        'description': 'A personal website to write articles and display work'
    },
    {
        'id': '3',
        'title': 'Social Network',
        'description': 'An open source project built by the comapny'
    }
]

# Create your views here.
def projectAll(request):
    projects = Project.objects.all().order_by('vote_ratio')
    # current_date=datetime.datetime.today()
    context = {
        'projects':projects,
    }
    return render(request,'projects/project-all.html',context)

def project(request, pk):
    proj_obj=Project.objects.get(id=pk)
    tags=proj_obj.tags.all()
    # for project in projectsList:
    #     if project['id'] == pk:
    #         print('Object matched')
    #         proj_obj = project


    context ={ 
        'proj':proj_obj,'tags':tags
    }
    return render(request,'projects/project.html',context)


@login_required(login_url='users:login')
def createProject(request):
    profile = request.user.profile

    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project =form.save(commit=False)
            project.owner = profile
            form.save()
            return redirect('users:account')

    context={'form':form,}
    return render(request,'projects/project-form.html',context)

@login_required(login_url='users:login')
def updateProject(request,pk):
    profile = request.user.profile
    projectObj = Project.objects.get(id=pk)

    form = ProjectForm(instance=projectObj)

    if request.method == 'POST':
        form = ProjectForm(request.POST,instance=projectObj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project Updated Successfully')
            return redirect('users:account')
        
    context={'form':form,}
    return render(request,'projects/project-form.html',context)

@login_required(login_url='users:login')
def deleteProject(request,pk):
    profile = request.user.profile
    projObj = Project.objects.get(id=pk)

    if request.method == 'POST':
        projObj.delete()
        messages.success(request, 'Project Deleted Successfully')
        return redirect('users:account')

    context={'object':projObj}
    return render(request,'projects/delete-templates.html',context)


