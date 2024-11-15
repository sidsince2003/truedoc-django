from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload_document/', views.upload_document, name='upload_document'),
    path('view_document/<str:file_id>/', views.view_document, name='view_document'),
    path('download_document/<str:file_id>/', views.download_document, name='download_document'),
    path('update_ocr/<str:file_id>/', views.update_ocr, name='update_ocr'),
    path('logout/', views.logout_view, name='logout'),
    # Add other URL patterns
] 
