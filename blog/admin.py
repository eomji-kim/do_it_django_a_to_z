from django.contrib import admin

# 관리자 페이지에 Post 모델 등록
from .models import Post

admin.site.register(Post)
