from django.shortcuts import render,redirect
from django.db.models import Q

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project,Tag
from .form import ProjectForm

from .utils import searchProjects,paginateProjects


def projects(request):
    projects,search_query = searchProjects(request)
    custom_range,projects = paginateProjects(request,projects,6)




    context = {'projects':projects,'search_query':search_query,'custom_range':custom_range}
    return render(request,'projects/projects.html',context)

def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    return render(request,'projects/single-project.html',{'projectObj':projectObj})
    #return HttpResponse("Single project"+" "+str(pk))

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile

    form = ProjectForm()
    if request.method=='POST':
        #print(request.POST)
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save() #add new object in database
            return redirect('projects')
        
    context = {'form': form}
    return render(request,"projects/project_form.html",context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile = request.user.profile
    project=profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method=='POST':
        #print(request.POST)
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save() #add new object in database
            return redirect('account')
        
    context = {'form': form}
    return render(request,"projects/project_form.html",context)
    
@login_required(login_url="login")
def deleteProject(request,pk):
    
    profile = request.user.profile
    project=profile.project_set.get(id=pk)
    if request.method=="POST":
        project.delete()
        return redirect("account")
    context = {'object': project}
    return render(request,"delete_template.html",context)