from django.urls import path
from . import views

urlpatterns = [
    path('', views.case_search_view, name='case_search'),
    path('api/cases/', views.fetch_case_data, name='fetch_case_data'),
]