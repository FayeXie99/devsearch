from email.policy import default
from enum import unique
from django.db import models
from users.models import Profile
import uuid
# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True,blank=True,default="default.jpg")
    demo_link = models.CharField(max_length=2000,null=True,blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True,editable=False)
    
    tags=models.ManyToManyField('Tag',blank=True)
    vote_total = models.IntegerField(default=0,null=True, blank=True)
    vote_ratio = models.IntegerField(default=0,null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering=['created'] #order by descending created


class Review(models.Model):
    #owner
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    VOTE_TYPE=(('up','UP Vote'),('down','Down Vote'))
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200,choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True,editable=False)
    def __str__(self) -> str:
        return self.value
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True,editable=False)
    def __str__(self) -> str:
        return self.name
    


