from django.urls import path

from . import views

urlpatterns = [
    path('reservation', views.ResListView.as_view(), name = 'reservation.list'),
    path('reservation/<int:pk>', views.ResDetailView.as_view(), name = 'reservation.detail'),
    path('reservation/<int:pk>/edit', views.ResUpdateView.as_view(), name = 'reservation.update'),
    path('reservation/<int:pk>/delete', views.ResDeleteView.as_view(), name = 'reservation.delete'),
    path('reservation/new', views.ResCreateView.as_view(), name = 'reservation.new'),
    path('platform', views.PltListView.as_view(), name = 'platform.list'),
    path('platform/<int:pk>', views.PltDetailView.as_view(), name = 'platform.detail'),
    path('platform/<int:pk>/edit', views.PltUpdateView.as_view(), name = 'platform.update'),
    path('platform/<int:pk>/delete', views.PltDeleteView.as_view(), name = 'platform.delete'),
    path('platform/new', views.PltCreateView.as_view(), name = 'platform.new'),
    path('apartment', views.AptListView.as_view(), name = 'apartment.list'),
    path('apartment/<int:pk>', views.AptDetailView.as_view(), name = 'apartment.detail'),
    path('apartment/<int:pk>/edit', views.AptUpdateView.as_view(), name = 'apartment.update'),
    path('apartment/<int:pk>/delete', views.AptDeleteView.as_view(), name = 'apartment.delete'),
    path('apartment/new', views.AptCreateView.as_view(), name = 'apartment.new'),
    path('invoice/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice.detail'),
    path('invoice1/<int:pk>/', views.InvoiceDetailedView.as_view(), name='invoice1.detail'),

    path('invoice', views.InvoiceListView.as_view(), name='invoice.list'),
    path('taxrate', views.TaxRateListView.as_view(), name='taxrate.list'),
    path('taxrate/<int:pk>', views.TaxRateDetailView.as_view(), name='taxrate.detail'),
    path('taxrate/<int:pk>/edit', views.TaxRateUpdateView.as_view(), name='taxrate.update'),
    path('taxrate/new', views.TaxRateCreateView.as_view(), name='taxrate.new'),
    



] 