from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from strife import views
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Strife')

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'players', views.PlayerViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^schema/$', schema_view),
    url(r'^', include(router.urls)),
]