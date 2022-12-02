from django.contrib import admin
from .models import Post, Category, Tag

# 관리자 페이지에 Post 모델 등록
admin.site.register(Post)

class CategotyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

# 관리자 페이지에 Category, CategotyAdmin 모델 등록
admin.site.register(Category, CategotyAdmin)
admin.site.register(Tag, TagAdmin)