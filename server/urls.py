from django.urls import path

from . import views
from .views import RoomListView

urlpatterns = [
    path('', views.index, name='index'),
    # path('<str:room_name>/', views.room, name='room'),
    path('<str:room_name>/', RoomListView.as_view(), name='room'),

]