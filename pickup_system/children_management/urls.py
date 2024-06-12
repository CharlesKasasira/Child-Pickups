from django.urls import path
from . import views
from .views import register_parent
from .views import register_guardian
from .views import register_driver
from .views import drivers_list
from .views import register_child
from .views import parents_list
from .views import guardians_list
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main_dashboard, name='dashboard'),
    path('register/child/', register_child, name='register_child'),
    path('register/parent/', register_parent, name='register_parent'),
    path('register/driver/', register_driver, name='register_driver'),
    path('drivers/', drivers_list, name='drivers_list'),
    path('register/guardian/', register_guardian, name='register_guardian'),
    path('search/', views.search_child, name='search_child'),
    path('list_children/', views.list_children, name='list_children'),
    path('parents/', parents_list, name='parents_list'),
    path('guardians/', guardians_list, name='guardians_list'),
    path('edit_parent/<int:pk>/', views.edit_parent, name='edit_parent'),
    path('delete_parent/<int:pk>/', views.delete_parent, name='delete_parent'),
    path('edit_guardian/<int:pk>/', views.edit_guardian, name='edit_guardian'),
    path('delete_guardian/<int:pk>/', views.delete_guardian, name='delete_guardian'),
    path('edit_driver/<int:pk>/', views.edit_driver, name='edit_driver'),
    path('delete_driver/<int:pk>/', views.delete_driver, name='delete_driver'),
    path('edit_child/<int:pk>/', views.edit_child, name='edit_child'),
    path('delete_child/<int:pk>/', views.delete_child, name='delete_child'),
    # Define URLs for other views
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
