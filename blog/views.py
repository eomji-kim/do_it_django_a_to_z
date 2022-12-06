from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag, Comment
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        # 댓글 작성자와 로그인한 사용자가 다른 경우 PermissionDenied 오류가 발생하도록
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            # PermissionDenied 의 사용자가 요청 된 작업을 수행 할 수있는 권한이 없는 경우 예외가 발생합니다.
            raise PermissionDenied



class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)

        return context


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response


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
            form.instance.author = current_user
            # CreateView의 form_valid() 함수의 결괏값을 변수에 임시로 담아두기.
            response = super(PostCreate, self).form_valid(form)

            # input의 값을 가져와라
            tags_str = self.request.POST.get('tags_str')

            # input이 빈칸인 경우 태그와 관련된 동작 필요x, 따라서 if 문으로 처리
            if tags_str:
                # strip() : 양쪽의 공백 제거
                tags_str = tags_str.strip()
                # ',', ';' 구분자로 처리하기 위해 tags_str로 받은 값의 쉼표(,)를 세미콜론(;)으로 변경해줌.
                tags_str = tags_str.replace(',', ';')
                # 변경한 후 세미콜론으로 split해서 리스트 형태로 tags_list에 담는다.
                tags_list = tags_str.split(';')

                for t in tags_list:
                    # tags_list에 리스트 형태로 담겨 있는 값은 문자열 형태이므로 Tag 모델의 인스턴스로 변환하는 과정 필요.
                    t = t.strip()
                    # 이 값을 name으로 갖는 태그가 있다면 가져오고, 없다면 새로 만듦.
                    # get_or_create()는 두 가지 값을 동시에 return. 첫 번째는 Tag 모델의 인스턴스,
                    # 두 번째는 이 인스턴스가 새로 생성되었는지를 나타내는 bool 형태의 값
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    # 같은 name을 갖는 태그가 없어 새로 생성 했아면 slug 값은 없는 상태이므로 slug 값을 생성해줘야 함.
                    # slugify()라는 함수를 사용해 slug 값 생성할 수 있도록
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    # self.object : 이번에 새로 만든 포스트
                    self.object.tags.add(tag)

            return response
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
        context['comment_form'] = CommentForm
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

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())

        else:
            return redirect(post.get_absolute_url())

    else:
        raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

