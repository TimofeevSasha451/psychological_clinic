from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (SpecialistViewSet, RedirectToSpecialistsView, UserViewSet,
                    ApplicationViewSet,)

router_v1 = DefaultRouter()
router_v1.register('specialists', SpecialistViewSet, basename='specialist')
router_v1.register('users', UserViewSet, basename='user')
router_v1.register('join-team', ApplicationViewSet,
                   basename='join-to-specialists')


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('choose-session/', RedirectToSpecialistsView.as_view(),
         name='redirect-to-specialists'),
    path('', include(router_v1.urls))
]
