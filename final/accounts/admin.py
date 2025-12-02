'''
11/07 pjt 06 F02 
admin.py 수정
'''


from django.contrib import admin
from .models import CustomUser

admin.site.register(CustomUser)
