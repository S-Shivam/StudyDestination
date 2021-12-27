from django.urls import path
from . import views

app_name = 'study'
urlpatterns = [
    # /study/
    path('', views.index, name='index'),
    # /study/search/
    path('search/', views.search, name='search'),
    # /study/register/
    path('register/', views.register, name='register'),
    # /study/login/
    path('login/', views.user_login, name='user_login'),
    # /study/logout/
    path('logout/', views.user_logout, name='user_logout'),
    # study/<country_id>/
    path('<int:country_id>/', views.detail, name='detail'),
    # study/<country_id>/favorite/
    path('<int:country_id>/favorite/', views.favorite, name='favorite'),
    # study/country/add/
    path('country/add/', views.add_country, name='add_country'),
    # study/country/<country_id>/
    path('country/<int:country_id>/', views.edit_country, name='edit_country'),
    # study/country/<country_id>/delete/
    path('country/<int:country_id>/delete/', views.delete_country, name='delete_country'),
    # study/university/<university_id>/delete/
    path('university/<int:university_id>/delete/', views.delete_univ, name='delete_univ'),
    # study/<country_id>/university/add/
    path('<int:country_id>/university/add/', views.add_university, name='add_university'),
    # study/university/<university_id>
    path('university/<int:university_id>/', views.edit_university, name='edit_university'),
    # study/university/
    path('university/', views.all_university, name='all_university'),
    # study/university/shortlists/
    path('university/shortlists/', views.shortlists, name='shortlists'),
    # study/university/details/<university_id>/
    path('university/details/<int:university_id>/', views.univ_details, name='univ_details'),
    # test
    path('test', views.test1, name='test'),
]
