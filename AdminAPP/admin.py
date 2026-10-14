from django.contrib import admin

# Register your models here.
from .models import Signup, Project, Experience,  Skill

@admin.register(Signup)
class Signup(admin.ModelAdmin):
     list_display = ("id", "username", "fullname", "email", "phone", "title","location","bio", "password","pic")
     search_fields = ("fullname__startswith",)

@admin.register(Project)
class Project(admin.ModelAdmin):
    list_display = (
        "id","title","category","description","image","technologies","project_url","github_url","status","display_order","created_at", "updated_at",)
    search_fields = ("title", "category","description","technologies",)
   
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "id","title","company","start_date","end_date","employment_status","description","responsibilities","technologies","visibility","display_order","created_at","updated_at",)

    search_fields = ("title","company","description","responsibilities","technologies",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id","name","category","proficiency","display_order","icon","description","status","created_at", "updated_at",
    )
    search_fields = ("name","category", "description", "icon", )       