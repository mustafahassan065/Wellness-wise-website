
from django.urls import path 
from my_app import views  
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('' , views.home , name = 'home'),
    path('register/', views.register, name='register'),  
    path('register/login_view/', views.login_view, name='login_view'), 
    path('login_view/', views.login_view, name='login_view'), 
    path('wellness-resources/', views.wellness_resources, name='wellness_resources'),  
    path('expert-connections/', views.expert_connections, name='expert_connections'),  
    path('profile_view/', views.profile_view, name='profile_view'), 
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),  
    path('profile/delete/', views.delete_profile_view, name='delete_profile'),
    path('accounts/login/', views.login_view, name='login'),
    path('profile_view/resources/', views.resource_list, name='resource_list'),
    path('profile_view/resources/favorites/', views.favorite_list, name='favorite_list'),
    path('resources/', views.resource_list, name='resource_list'),
    path('profile_view/resources/', views.resource_list, name='resource_list'),
    path('resources/favorites/', views.favorite_list, name='favorite_list'),
    path('add_favorite/<int:resource_id>/', views.add_favorite, name='add_favorite'),
    path('advice_view/', views.advice_view, name='advice_view'),
    path('experts/list/', views.expert_list, name='expert_list'),
    path('book-session/<int:expert_id>/', views.book_session, name='book_session'),
    path('session-detail/<int:session_id>/', views.session_detail, name='session_detail'),
    path('expert-profile/<int:pk>/', views.expert_profile_detail, name='expert_profile_detail'),
    path('edit-expert-profile/<int:pk>/', views.edit_expert_profile, name='edit_expert_profile'),
    # Other URL patterns # Correct pattern
    path('create-expert-profile/', views.create_expert_profile , name = 'create_expert_profile'),
    path('expert-profile/delete/<int:expert_id>/', views.delete_expert_profile, name='delete_expert_profile'),
    path("user/", views.house, name="house"),
    path("edit/", views.EditProfile, name="edit"),
    path("user/<str:username>/", views.userprofile, name="username"),
    path("add_friend/", views.add_friend, name="add_friend"),
    path("accept_request/", views.accept_request, name="accept_request"),
    path("delete_friend/", views.delete_friend, name="delete_friend"),
    path("search/", views.search, name="search"),
    # re_path(r"^.*/$", RedirectView.as_view(pattern_name="login", permanent=False)),
    path("chat/<str:username>", views.chat, name="chat"),
    path('expert/<int:pk>/', views.expert_profile_detail, name='expert_profile'),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)