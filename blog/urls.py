from django.urls import path
from  . import  views

urlpatterns = [
    # slug 인자 : url localhost:8000/blog/category/programming/ 이라고 입력하면
    # programming/ 만 떼어 views.py의 category_page()함수로 보냄.
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
    # path('', views.index),
    # path('<int:pk>/' , views.single_post_page),
]