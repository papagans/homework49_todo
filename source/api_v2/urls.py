from django.urls import include, path
from rest_framework import routers
from api_v2 import views
from rest_framework.authtoken.views import obtain_auth_token

from api_v2.views import LogoutView

router = routers.DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'todo', views.TodoViewSet)
app_name = 'api_v2'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='api_token_delete')
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]