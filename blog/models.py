from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    # auto_now_add : 현 시간에 맞추고, 없으면 추가하기
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # author : 외래키 추후 작성 예정

    def __str__(self):
        return f'[{self.pk}] {self.title}'