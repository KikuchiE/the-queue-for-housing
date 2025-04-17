from django.urls import path
from . import views
from .views import AuthenticateView, CreateApplicationView, UploadDocumentView

app_name = "users"

# urlpatterns = [
#     path('signup/', views.signup_view, name="signup"),
#     path('login/', views.login_view, name="login"),
#     path('logout/', views.logout_view, name="logout"),
#     path('profile', views.profile_view, name="profile"),
#     path('profile/update', views.update_profile, name="update_profile"),
#     path('profile/delete', views.delete_account, name="delete_account"),
# ]


urlpatterns = [
    # Authentication URLs
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Profile management URLs
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/delete/', views.DeleteAccountView.as_view(), name='delete_account'),
] + [
    path('api/authenticate/', AuthenticateView.as_view(), name='authenticate'),
    path('api/applications/', CreateApplicationView.as_view(), name='create_application'),
    path('api/applications/<int:application_id>/documents/', UploadDocumentView.as_view(), name='upload_document'),
]