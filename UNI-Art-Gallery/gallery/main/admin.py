# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User_Credentials, Art, User_Info, Tag_List, Art_Tags, Art_Rating,User_Social

admin.site.register(User_Credentials, UserAdmin)
admin.site.register(Art)
admin.site.register(User_Info)
admin.site.register(Tag_List)
admin.site.register(Art_Tags)
admin.site.register(Art_Rating)
admin.site.register(User_Social)

