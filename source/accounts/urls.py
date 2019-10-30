from accounts.views import logout_view, login_view, register_view, user_activate, UserDetailView
from django.urls import path

app_name = 'accounts'


urlpatterns = [
   path('login/', login_view, name='login'),
   path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('register/activate/', user_activate, name='user_activate'),
    path('<pk>/', UserDetailView.as_view(), name='detail'),

]