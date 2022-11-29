from django.shortcuts import render
from .models import Post

# templates 폴더에 들어있는 것이 기본 값
def index(request):
    # 데이터베이스의 쿼리를 날려 원하는 레코드 가져오기
    posts = Post.objects.all().order_by('-pk')

    return render(
        request,
        'blog/index.html',
        {
            'posts' : posts,
        }
    )
