from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import PasswordChangeView, LogoutView

app_name = 'universities'

urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),  # Приветственная страница
    path('universities/', views.university_list, name='university_list'),  # Пример другого маршрута
    path('list/', views.university_list, name='university_list'),
    path('search/', views.university_search, name='university_search'),
    path('favorite/remove/<int:university_id>/', views.remove_favorite, name='remove_favorite'),
    path('detail/<int:university_id>/', views.university_detail, name='university_detail'),
    path('favorites/', views.favorite_universities, name='favorite_universities'),
    path('login/', auth_views.LoginView.as_view(template_name='universities/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='universities:university_list'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('save/<int:university_id>/', views.save_university, name='save_university'),
    path('remove/<int:university_id>/', views.remove_university, name='remove_university'),
    path('delete_exam_result/<int:result_id>/', views.delete_exam_result, name='delete_exam_result'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('password_change/', PasswordChangeView.as_view(template_name='universities/password_change.html'), name='password_change'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]