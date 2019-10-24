from accounts.views import logout_view, login_view
from django.urls import path

app_name = 'accounts'


urlpatterns = [
   path('login/', login_view, name='login'),
   path('logout/', logout_view, name='logout')

]