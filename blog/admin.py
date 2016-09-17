from django.contrib import admin
from .models import Blogpost, Tag

# Register your models here.

myModels = [Blogpost, Tag]

admin.site.register(myModels)
