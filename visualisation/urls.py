from django.urls import path
from . import views

app_name = "visualisation"
urlpatterns = [
    path('', views.search_view, name='search_view'),  # Page de recherche
    path('select/<int:commune_id>/', views.select_data_view, name='select_data'),  # Sélection des données
    path('map/<int:commune_id>/', views.map_view, name='map_view'),  # Carte interactive
    path('<int:commune_id>/population-pie-chart/', views.population_pie_chart_view, name='population_pie_chart'),
]
    
