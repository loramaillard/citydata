from django.shortcuts import render, get_object_or_404, redirect
from .models import Commune
from .field_labels import field_labels
from django.http import HttpResponse
import folium  # Bibliothèque pour créer des cartes interactives
import math
from django.urls import reverse
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def search_view(request):
    query = request.GET.get('query', '')  # Récupérer la recherche de l'utilisateur
    communes = []
    if query:
        communes = Commune.objects.filter(libgeo__icontains=query)  # Chercher les villes correspondant au nom
    return render(request, 'visualisation/search.html', {'query': query, 'communes': communes})




def select_data_view(request, commune_id):
    commune = get_object_or_404(Commune, pk=commune_id)

    # Récupérer les champs du modèle Commune
    fields = [field.name for field in Commune._meta.get_fields() if not field.is_relation]
    # Liste des champs à exclure
    excluded_fields = ['id', 'libgeo','codgeo','p21_pop0014','p21_pop1529','p21_pop3044','p21_pop4559'
                       ,'p21_pop6074','p21_pop7589','p21_pop90p','nombre_crime', 'latitude_centre', 'longitude_centre']

    # Filtrer les champs avec des valeurs non nulles ou non NaN
    valid_fields = {
        field: getattr(commune, field)
        
        for field in fields 
        if field not in excluded_fields and
        getattr(commune, field) not in [None, '', float('nan'),0] and 
        not (isinstance(getattr(commune, field), float) and math.isnan(getattr(commune, field)))
    }
    
    valid_fields_1 = {}
    for key in valid_fields.keys():
        valid_fields_1[key] = field_labels.get(key)

    valid_fields.update(valid_fields_1)    

    # Créer un tableau contenant uniquement les labels correspondants aux clés de valid_fields
    #valid_field_labels = [
    #    field_labels.get(field, field) for field in valid_fields.keys()
    #]
    #print(valid_fields)
    if request.method == "POST":
        selected_fields = request.POST.getlist('data_fields')  # Cases sélectionnées
        request.session['selected_fields'] = selected_fields  # Sauvegarde des champs sélectionnés
        return redirect(reverse('visualisation:map_view', args=[commune_id]))

    return render(request, 'visualisation/select_data.html', {
        'commune': commune,
        'valid_fields': valid_fields,
    })


def map_view(request, commune_id):
    commune = get_object_or_404(Commune, pk=commune_id)

    # Récupérer les champs sélectionnés depuis la session
    selected_fields = request.session.get('selected_fields', [])

    # Construire le contenu du popup
    popup_content = f"<b>{commune.libgeo}</b><br>"
    for field in selected_fields:
        value = getattr(commune, field, None)
        if value is not None:
            # Arrondir les valeurs numériques
            if isinstance(value, float):
                value = round(value, 2)
            popup_content += f"{field_labels.get(field)}: {value}<br>"
    # Si aucun champ sélectionné, ajouter un message par défaut
    if not popup_content:
        popup_content = "Aucune donnée sélectionnée."
        
    context = {
        'commune': commune,
        'popup_content': popup_content,
    }
    return render(request, 'visualisation/map.html', context)

def population_pie_chart_view(request, commune_id):
    # Récupérer la commune sélectionnée
    commune = get_object_or_404(Commune, pk=commune_id)
    
    # Extraire les données de population par tranche d'âge
    population_data = {
        '0-14 ans': commune.p21_pop0014,
        '15-29 ans': commune.p21_pop1529,
        '30-44 ans': commune.p21_pop3044,
        '45-59 ans': commune.p21_pop4559,
        '60-74 ans': commune.p21_pop6074,
        '75-89 ans': commune.p21_pop7589,
        '90+ ans': commune.p21_pop90p,
    }
    
    # Filtrer les données non nulles
    population_data = {k: v for k, v in population_data.items() if v is not None}
    
    # Créer le graphique
    fig, ax = plt.subplots()
    ax.pie(
        population_data.values(), 
        labels=population_data.keys(), 
        autopct='%1.1f%%', 
        startangle=90
    )
    ax.axis('equal')  # Assure que le graphique est circulaire
    
    # Convertir le graphique en image encodée en base64
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    
    # Passer l'image à la page HTML
    return render(request, 'visualisation/population_pie_chart.html', {
        'commune': commune,
        'chart': image_base64,
    })