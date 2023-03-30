from django.contrib import admin
# 모델에 있는 것 전부 import 해라
# from .models import Board, Comment 이렇게 해도 됨
from .models import *

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    search_fields = ['subject','content']

admin.site.register(Board,BoardAdmin)
admin.site.register(Comment)