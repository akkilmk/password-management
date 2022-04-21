from django.urls import include, path
from . import views
urlpatterns = [
    path('',views.SignUP.as_view(),name='signup'),
    path('sites/',views.SiteRegistration.as_view(),name='sites'),
    path('shared/', views.SharingDetail.as_view(), name='shared'),
    path('permission/', views.Permission.as_view(), name='permission'),
]