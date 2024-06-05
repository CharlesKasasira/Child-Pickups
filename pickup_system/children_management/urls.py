from django.urls import path
from . import views
from .views import register_parent
from .views import register_guardian
from .views import register_driver
from .views import drivers_list
from .views import register_child
from .views import parents_list
from .views import guardians_list, sendSMS, login_view, logout_user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main_dashboard, name='dashboard'),
    path('login', login_view, name='login'),
    path('logout', logout_user, name='logout'),
    path('register/child/', register_child, name='register_child'),
    path('message/parent/', sendSMS, name='message_parent'),
    path('register/parent/', register_parent, name='register_parent'),
    path('register/driver/', register_driver, name='register_driver'),
    path('drivers/', drivers_list, name='drivers_list'),
    path('register/guardian/', register_guardian, name='register_guardian'),
    path('search/', views.search_child, name='search_child'),
    path('list_children/', views.list_children, name='list_children'),
    path('parents/', parents_list, name='parents_list'),
    path('guardians/', guardians_list, name='guardians_list'),
    # Define URLs for other views
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


