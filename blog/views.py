# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class PostList(ListView):
    model = Post
    # ListView는 모델명 뒤에 '_list'가 붙은 html 파일을 기본 템플릿으로 사용하도록 설정되어 있음
    # 템플릿 이름을 오버라이딩 해주거나, html 이름을 post_list.html로 바꾸어주어야 함.
    # template_name = 'blog/index.html'
    ordering = '-pk'

class PostDetail(DetailView):
    model = Post


# templates 폴더에 들어있는 것이 기본 값
# def index(request):
#     # 데이터베이스의 쿼리를 날려 원하는 레코드 가져오기
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(
#         request,
#         'blog/post_list.html',
#         {
#             'posts' : posts,
#         }
#     )

# def single_post_page(request, pk):
#     # .get : 쿼리에서 주어진 pk의 pk만 가져오겠다
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'post' : post,
#         }
#     )