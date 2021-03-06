from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'core'
urlpatterns = [
    path('', views.IndexRedirectView.as_view(), name='index-redirect'),
    path('accounts/registration/', views.RegistrationView.as_view(), name='registration'),
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/username_change/', views.ChangeUsernameView.as_view(), name='username_change'),
    path('accounts/password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/delete/', views.DeleteUserAccount.as_view(), name='account_delete'),
    path('accounts/password_reset/', views.ResetUserPasswordView.as_view(), name='password_reset'),
    path('<username>/logs/', views.IndexView.as_view(), name='index'),
    path('<username>/logs/<int:pk>/', views.LogView.as_view(), name='log'),
    path('<username>/logs/delete/', views.DeleteLog.as_view(), name='delete-log'),
    path('<username>/profile/', views.ProfileView.as_view(), name='profile'),
    path('<username>/profile/edit/', views.EditProfileView.as_view(), name='edit-profile'),
    path('<username>/profile/change_photo/', views.EditProfileImageView.as_view(), name='change-photo'),
    path('<username>/profile/delete_photo/', views.DeleteProfileImageView.as_view(), name='delete-photo'),
    path('<username>/note/create/', views.CreateNote.as_view(), name='create-note'),
    path('<username>/note/edit/', views.EditNote.as_view(), name='edit-note'),
    path('<username>/note/delete/', views.DeleteNote.as_view(), name='delete-note'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
