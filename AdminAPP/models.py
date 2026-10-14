from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Signup(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, default='')
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    bio = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=15)
    pic = models.ImageField(upload_to='media/')
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "Signup"       
    def __str__(self):
         return "Name: {}, Pnone: {}".format(self.fullname, self.phone)

class Project(models.Model):
    STATUS_CHOICES = (('published', 'Published'),
        ('draft', 'Draft'), )
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media/')
    technologies = models.CharField(max_length=500,blank=True)
    project_url = models.URLField(blank=True,null=True)
    github_url = models.URLField(blank=True,null=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='published')
    display_order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Project"
    def __str__(self):

        return self.title

class Experience(models.Model):
    EMPLOYMENT_STATUS_CHOICES = (
        ('current', 'Current Position'),
        ('completed', 'Completed'),
    )
    VISIBILITY_CHOICES = (
        ('published', 'Published'),
        ('draft', 'Draft'),
    )
    title = models.CharField( max_length=200)
    company = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField( blank=True,null=True)
    employment_status = models.CharField(max_length=20,choices=EMPLOYMENT_STATUS_CHOICES,
        default='current')
    description = models.TextField()
    responsibilities = models.TextField(blank=True)
    technologies = models.CharField(max_length=500,blank=True)
    visibility = models.CharField( max_length=20,choices=VISIBILITY_CHOICES,default='published')
    display_order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Experience"
        ordering = ['display_order', '-start_date']

    def __str__(self):
        return f"{self.title} - {self.company}"

    @property
    def responsibility_list(self):
      return [
          responsibility.strip()
          for responsibility in self.responsibilities.split(',')
          if responsibility.strip()
    ]

class Skill(models.Model):
    proficiency = models.PositiveIntegerField(
    default=80,
    validators=[
        MinValueValidator(0),
        MaxValueValidator(100),
    ]
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(default=80)
    display_order = models.PositiveIntegerField(default=1)
    icon = models.CharField(max_length=200,blank=True)
    description = models.TextField(blank=True)
    status = models.CharField( max_length=20,choices=STATUS_CHOICES,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Skill"
        ordering = ['display_order', '-id']
    def __str__(self):
        return self.name    