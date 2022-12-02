from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category

class PostList(ListView):
    model = Post
    ordering = '-pk'

    # **kwargs : 딕셔너리 형태로 처리.
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        # context에 get_context_data()에서 기존에 제공했던 기능 그대로를 저장.
        context = super(PostDetail, self).get_context_data()
        # 모든 카테고리를 가져와서 'categories'라는 키에 저장.
        context['categories'] = Category.objects.all()
        # Post.objects.filter(category=None).count() : 카테고리가 지정되지 않은 포스트의 개수를 세라는 의미의 쿼리셋
        # 을 'no_category_post_count'라는 키에 저장.
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )
