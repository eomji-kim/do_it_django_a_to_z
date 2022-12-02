from django.db import models
from django.contrib.auth.models import User
import os


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'


class Category(models.Model):
    # unique=True : 동일한 이름 사용 안되게.
    name = models.CharField(max_length=50, unique=True)

    # slug : url을 생성하기 위해 문자를 조합하는 방식
    # SlugField : 사람이 읽을 수 있는 텍스트로 고유 url을 만들고 싶을 때 주로 사용.
    # 이 때, SlugField는 한국어를 지원하지 않으므로 allow_unicode=True로 한글로 만들 수 있게 함.
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # on_delete=models.SET_NULL : 카테고리가 삭제되어도 연결된 포스트는 삭제되지 않도록.
    category = models.ForeignKey(Category, null=True, blank=True,
                                 on_delete=models.SET_NULL)

    # on_delete=models.SET_NULL은 설정x, 연결된 태그가 삭제되면 해당 포스트의 tags는 필드는 알아서 빈칸으로 바뀜.
    # ManyToManyField는 기본적으로 null=True라 쓰지 않아야함.
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

