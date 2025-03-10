from django.shortcuts import render, get_object_or_404, redirect
from .models import Commune, Aeroport, Centrale, Hopital, Ecole
from .field_labels import field_labels
from .services import get_ecoles_from_api, get_sante_from_api, get_gares_from_api
from django.http import HttpResponse, JsonResponse
import math
from django.urls import reverse
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from math import radians, sin, cos, sqrt, atan2
import json
from collections import defaultdict

def search_view(request):
    query = request.GET.get('query', '')  # Récupérer la recherche de l'utilisateur
    communes = []
    if query:
        communes = Commune.objects.filter(libgeo__icontains=query).order_by('libgeo')  # Chercher les villes correspondant au nom

    return render(request, 'visualisation/search.html', {'query': query, 'communes': communes})


def select_data_view(request, commune_id):
    commune = get_object_or_404(Commune, pk=commune_id)

    # Liste des types de données affichables
    #valid_fields = ["ecoles", "Aéroports", "centrales", "hopitaux", "ehpads", "pharmacies", "docteurs", "gares", "Données statistiques"]
    valid_fields = {
    "ecoles": 0,
    "Aéroports": 0,
    "centrales": 0,
    "hopitaux": 0,
    "ehpads":0,
    "pharmacies":0,
    "docteurs":0,   
    "gares":0,
    "Données statistiques":0,

    }
    valid_fields = {key: field_labels.get(key, key) for key in valid_fields.keys()}


    if request.method == "POST":
        selected_fields = request.POST.getlist('data_fields')  # Cases cochées par l'utilisateur
        request.session['selected_fields'] = selected_fields  # Sauvegarde des choix dans la session
        return redirect(reverse('visualisation:map_view', args=[commune_id]))

    return render(request, 'visualisation/select_data.html', {
       'commune': commune,
       'valid_fields': valid_fields,  # Liste des cases disponibles   
       'field_labels': field_labels, 
    })

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Rayon de la Terre en mètres
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance en mètres


def map_view(request, commune_id):
    commune = get_object_or_404(Commune, pk=commune_id)

    # Récupérer les champs sélectionnés depuis la session
    selected_fields = request.session.get('selected_fields', [])

    # Construire le contenu du popup si "Données statistiques" est sélectionné
    popup_content = f"<b>{commune.libgeo}</b><br>"
    if "Données statistiques" in selected_fields:
        fields = [field.name for field in Commune._meta.get_fields() if not field.is_relation]

        # Liste des champs à exclure
        excluded_fields = ['id', 'libgeo','codgeo','p21_pop0014','p21_pop1529','p21_pop3044','p21_pop4559'
                       ,'p21_pop6074','p21_pop7589','p21_pop90p','nombre_crime', 'latitude_centre', 'longitude_centre']

        # Filtrer les champs avec des valeurs non nulles ou non NaN
        valid_fields={}
        valid_fields.update({
        field: getattr(commune, field)
        for field in fields
        if field not in excluded_fields and
        getattr(commune, field) not in [None, '', float('nan'), 0] and 
        not (isinstance(getattr(commune, field), float) and math.isnan(getattr(commune, field)))
        })
    
        # Construire le contenu du popup
        for field in valid_fields:
            value = getattr(commune, field, None)
            if value is not None:
                # Arrondir les valeurs numériques
                if isinstance(value, float):
                    value = round(value, 2)
                popup_content += f"{field_labels.get(field)}: {value}<br>"
        # Si aucun champ sélectionné, ajouter un message par défaut
        if not popup_content:
            popup_content = "Aucune donnée sélectionnée."
    
    aeroports_data=[]
    # Recherche des aéroports si sélectionné
    if 'Aéroports' in selected_fields:
        centre_lat = commune.latitude_centre
        centre_lon = commune.longitude_centre
        aeroports_proches = []
        
        for aeroport in Aeroport.objects.all():
            distance = haversine(centre_lat, centre_lon, aeroport.latitude_aeroport, aeroport.longitude_aeroport)
            if distance <= 50000:  # 50 km
                aeroports_proches.append({
                    'nom': aeroport.nom,
                    'latitude_aeroport': aeroport.latitude_aeroport,
                    'longitude_aeroport': aeroport.longitude_aeroport,
                    'code_oaci': aeroport.code_oaci,
                    'code_iata': aeroport.code_iata,
                })
        aeroports_data = aeroports_proches
        #print(aeroports_data)    

    centrales_data = []
    if 'centrales' in selected_fields:
        centre_lat = commune.latitude_centre
        centre_lon = commune.longitude_centre

        # Grouper les centrales par leurs coordonnées exactes
        centrales_grouped = defaultdict(list)
        for centrale in Centrale.objects.all():
            distance = haversine(centre_lat, centre_lon, centrale.latitude_centrale, centrale.longitude_centrale)
            if distance <= 50000:  # Rayon de 50 km
                key = (centrale.latitude_centrale, centrale.longitude_centrale)
                centrales_grouped[key].append(centrale)

        offset = 0.002  # Décalage léger pour éviter la superposition (~30m)
        
        # Appliquer le décalage aux centrales qui ont les mêmes coordonnées
        for (lat, lon), centrales_list in centrales_grouped.items():
            for i, centrale in enumerate(centrales_list):
                centrales_data.append({
                    'nom': centrale.nom,
                    'latitude_centrale': lat + (i * offset),  # Décalage progressif
                    'longitude_centrale': lon + (i * offset),
                    'combustible': centrale.combustible,
                    'puissance_installee': centrale.puissance_installee,
                    'date_mise_en_service': centrale.date_mise_en_service.strftime('%Y-%m-%d'), 
                    'sous_filiere': centrale.sous_filiere,
                    'reserve_secondaire': centrale.reserve_secondaire
                })

    # Hôpitaux proches
    hopitaux_data = []
    if 'hopitaux' in selected_fields:
        hopitaux_data = get_sante_from_api(commune.libgeo, "hospital")
        hopitaux_data.extend(get_sante_from_api(commune.libgeo, "clinic"))

    ehpad_data = []
    if 'ehpads' in selected_fields:
        ehpad_data = get_sante_from_api(commune.libgeo, "nursing_home")
    
    pharmacies_data = []
    if 'pharmacies' in selected_fields:
        pharmacies_data = get_sante_from_api(commune.libgeo, "pharmacy")

    docteurs_data = []
    if 'docteurs' in selected_fields:
        docteurs_data = get_sante_from_api(commune.libgeo, "doctors")

    # hopitaux_data = []
    # if 'hopitaux' in selected_fields:
    #     centre_lat = commune.latitude_centre
    #     centre_lon = commune.longitude_centre
    # 
    #     for hopital in Hopital.objects.all():
    #         distance = haversine(centre_lat, centre_lon, hopital.latitude_hopital, hopital.longitude_hopital)
    #         if distance <= 5000:  # Rayon de 1 km
    #             hopitaux_data.append({
    #                 'nom': hopital.nom,
    #                 'latitude_hopital': hopital.latitude_hopital,
    #                 'longitude_hopital': hopital.longitude_hopital,
    #             })

    ecoles_data = []
    if 'ecoles' in selected_fields:  
        ecoles_data = get_ecoles_from_api(commune.libgeo)

    # ecoles_data = []
    # if 'ecoles' in selected_fields:  # Vérifier si l'utilisateur veut afficher les écoles
    #     ecoles = Ecole.objects.filter(nom_commune=commune.libgeo)  # Filtrer par la commune
    #     for ecole in ecoles:
    #         ecoles_data.append({
    #             'nom': ecole.nom,
    #             'latitude_ecole': ecole.latitude_ecole,
    #             'longitude_ecole': ecole.longitude_ecole,
    #             'secteur': ecole.secteur,
    #             'nature': ecole.nature,
    #             'nom_commune': ecole.nom_commune,
    #         })

    gares_data = []
    if 'gares' in selected_fields:
        gares_data = get_gares_from_api(commune.libgeo)


    context = {
        'commune': commune,
        'popup_content': popup_content,
        'aeroports_data': aeroports_data, 
        'centrales_data': centrales_data,
        'hopitaux_data':hopitaux_data,
        'ecoles_data':ecoles_data,
        'ehpad_data':ehpad_data,
        'pharmacies_data':pharmacies_data,
        'docteurs_data':docteurs_data,
        'gares_data':gares_data,
    }
    #print("ecoles envoyés au template:", ecoles_data if 'ecoles_data' in locals() else "Pas de données")

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