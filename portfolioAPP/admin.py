from django.contrib import admin

# Register your models here.
from .models import Contact


@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('id','name','email','phone','service','budget','timeline','subject','is_read', 'created_at',)
    search_fields = ('name','email','phone','subject','message',
    )
