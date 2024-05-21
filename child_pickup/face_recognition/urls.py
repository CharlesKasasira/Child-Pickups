from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.conf.urls.static import static
from .views import FaceRecognition

urlpatterns = [
    # path('', views.hello, name='hello'),
    # path('cam/', views.camera, name='hello2'),
    # path('detect_faces/', views.detect_faces, name='detect-faces'),
    # path('addFace/', views.addFace),
    path('capture_face/', views.capture_face, name='capture_face'),
    # path('register/', views.register, name='capture_face2'),
    path('register/', FaceRecognition.register, name='register'),
    path('login/', views.login, name='capture_face3'),
    path('listParents/', views.listParents, name='capture_face4'),
    path('list_users/', views.list_users, name='list_users'),


    # path('register/', FaceRecognition.register, name='register'),
    # path('train/', FaceRecognition.train, name='train'),
    # path('recognize/', FaceRecognition.recognize, name='recognize'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)