from .models import Profile,Skill
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage

def paginateProfiles(request,profiles,result):
    page=request.GET.get('page')
    #page = 1
    paginator= Paginator(profiles,result)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1 
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

        
    leftIndex = (int(page) - 1)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page) + 2)
    if rightIndex > paginator.num_pages+1:
        rightIndex=paginator.num_pages

    
    custom_range=range(leftIndex,rightIndex)
    return custom_range,profiles

def searchProfiles(request):
    search_query=''
    if request.GET.get('search_query'):
        search_query=request.GET.get('search_query')
    
    skills=Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) | 
        Q(skill__in=skills)

    )
    return profiles,search_query
