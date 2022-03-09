from email.policy import default
from django.db import models
from users.models import Profile

# Create your models here.
class Project(models.Model):
    project_type = [('static','Static Application'),
    ('dynamic','Web Application'),
    ]

    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length = 200, null = True, blank = True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='photos/',default='photos/logo.jpg',null=True,blank=True)
    demo_link = models.CharField(max_length=2000,null=True,blank=True)
    source_link = models.CharField(max_length=2000,null=True,blank=True)
    tags = models.ManyToManyField('Tag',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    vote_total = models.IntegerField(default=0,null=True,blank=True)
    vote_ratio = models.IntegerField(default=0,null=True,blank=True)
    type = models.CharField(max_length=30,choices=project_type,null=True,blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    values=[('up','Like'),('down','Dislike')]
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    body = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=20,choices=values)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
