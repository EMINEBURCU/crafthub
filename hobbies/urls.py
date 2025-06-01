from django.urls import path
from .views import home, create_post, post_detail, profile, like_toggle, category_detail
from .views import signup

urlpatterns = [
    path('', home, name='home'),
    path('create/', create_post, name='create_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('signup/', signup, name='signup'), 
    path('profile/', profile, name='profile'),
    path('like/<int:post_id>/', like_toggle, name='like_toggle'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
]
