from django.urls import path

from . import views

urlpatterns = [
    path('reservation', views.ResListView.as_view(), name = 'reservation.list'),
    path('reservation/<int:pk>', views.ResDetailView.as_view(), name = 'reservation.detail'),
    path('reservation/<int:pk>/edit', views.ResUpdateView.as_view(), name = 'reservation.update'),
    path('reservation/<int:pk>/delete', views.ResDeleteView.as_view(), name = 'reservation.delete'),

    path('reservation/new', views.ResCreateView.as_view(), name = 'reservation.new'),

] 