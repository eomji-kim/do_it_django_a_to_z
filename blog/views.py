from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Category, Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


# 믹스인 : 클래스를 상속하지 않고도 메소드를 조합할 수 있는 기법 혹은 개념(객체지향 프로그램의 범용적인 용어이자 표현)
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    # Post 모델에 사용할 필드명을 리스트로 작성.
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author =  current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')


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

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
        }
    )

