from django.contrib import admin

# 관리자 페이지에 Post 모델 등록
from .models import Post, Category

admin.site.register(Post)

class CategotyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategotyAdmin)