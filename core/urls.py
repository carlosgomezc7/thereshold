from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/generate-summary/', views.generate_ai_summary,
         name='generate_ai_summary'),
    path('api/metrics/update/', views.update_metric_value,
         name='update_metric_value'),
    path('optimization/', views.optimization_view, name='optimization'),
]
