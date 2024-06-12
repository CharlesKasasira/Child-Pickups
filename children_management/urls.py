from django.urls import path
from . import views, driver_views, child_views, parent_views, guardian_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Main Dashboard and Authentication
    path('', views.main_dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    
    
    
    # Guardian Related
    path('guardians/', guardian_views.guardians_list, name='guardians_list'),
    path('recognize_guardian/', guardian_views.start_recognition, name='recognize_guardian'),
    path('guardians_logs/', guardian_views.guardians_logs, name='guardians_logs'),
    path('register_guardian/', guardian_views.register_guardian, name='register_guardian'),
    path('capture_and_train/<int:guardian_id>/', guardian_views.capture_and_train, name='capture_and_train_guardian'),
    path('update_pickup_status/<int:log_id>/', guardian_views.update_pickup_status, name='update_pickup_status_guardian'),

    
    # Parent Related
    path('parents/', parent_views.parents_list, name='parents_list'),
    path('recognize_parent/', parent_views.start_recognition, name='recognize_parent'),
    path('parents_logs/', parent_views.parents_logs, name='parents_logs'),
    path('register_parent/', parent_views.register_parent, name='register_parent'),
    path('capture_and_train/<int:parent_id>/', parent_views.capture_and_train, name='capture_and_train_parent'),
    path('update_pickup_status/<int:log_id>/', parent_views.update_pickup_status, name='update_pickup_status_parent'),
    
    # Search and Lists
    path('search/', views.search_child, name='search_child'),
    path('list_children/', views.list_children, name='list_children'),
    path('parents/', views.parents_list, name='parents_list'),
    path('guardians/', views.guardians_list, name='guardians_list'),
    
    # Driver Related
    path('drivers/', driver_views.drivers_list, name='drivers_list'),
    path('recognize/', driver_views.start_recognition, name='recognize'),
    path('recognition_logs/', driver_views.recognition_logs, name='recognition_logs'),
    path('register_driver/', driver_views.register_driver, name='register_driver'),
    path('capture_and_train/<int:driver_id>/', driver_views.capture_and_train, name='capture_and_train_driver'),
    path('update_pickup_status/<int:log_id>/', driver_views.update_pickup_status, name='update_pickup_status_driver'),
    
    # Child Related
    path('children_logs/', child_views.children_logs, name='children_logs'),
    path('register_child/', child_views.register_child, name='register_child'),
    path('capture_and_train_child/<int:child_id>/', child_views.capture_and_train, name='capture_and_train_child'),
    path('update_pickup_status_child/<int:log_id>/', child_views.update_pickup_status, name='update_pickup_status_child'),
    path('children/', child_views.children_list, name='children_list'),
    path('recognize_child/', child_views.start_recognition, name='recognize_child'),
    
    # Other URLs can be defined here 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
