import requests

def get_ecoles_from_api(nom_commune):
    """
    Récupère les écoles d'une commune via l'API OpenData du Ministère de l'Éducation Nationale.
    lien : "https://data.education.gouv.fr/explore/dataset/fr-en-annuaire-education/information/?disjunctive.type_etablissement&disjunctive.libelle_academie&disjunctive.libelle_region&disjunctive.ministere_tutelle&disjunctive.appartenance_education_prioritaire&disjunctive.nom_commune&disjunctive.code_postal&disjunctive.code_departement"
    """
    url = "https://data.education.gouv.fr/api/records/1.0/search/"
    params = {
        "dataset": "fr-en-annuaire-education",
        "rows": 100,  # Nombre max d'écoles à récupérer
        "q": nom_commune,  # Filtrer par nom de la ville
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        ecoles = []

        for record in data.get("records", []):
            fields = record.get("fields", {})
            if "latitude" in fields and "longitude" in fields:
                ecoles.append({
                    "nom": fields.get("nom_etablissement", "École sans nom"),
                    "latitude_ecole": fields["latitude"],
                    "longitude_ecole": fields["longitude"],
                    "secteur": fields.get("statut_public_prive", "Inconnu"),
                    "nature": fields.get("nature_uai_libe", "École"),
                })
        
        return ecoles
    else:
        print("Erreur API:", response.status_code)
        return []

# lien:https://public.opendatasoft.com/explore/dataset/osm-france-healthcare/information/?disjunctive.meta_code_com&disjunctive.meta_code_reg&disjunctive.meta_code_dep&sort=type&dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6Im9zbS1mcmFuY2UtaGVhbHRoY2FyZSIsIm9wdGlvbnMiOnsiZGlzanVuY3RpdmUubWV0YV9jb2RlX2NvbSI6dHJ1ZSwiZGlzanVuY3RpdmUubWV0YV9jb2RlX3JlZyI6dHJ1ZSwiZGlzanVuY3RpdmUubWV0YV9jb2RlX2RlcCI6dHJ1ZSwic29ydCI6InR5cGUifX0sImNoYXJ0cyI6W3siYWxpZ25Nb250aCI6dHJ1ZSwidHlwZSI6ImxpbmUiLCJmdW5jIjoiQVZHIiwieUF4aXMiOiJ0eXBlX2ZpbmVzcyIsInNjaWVudGlmaWNEaXNwbGF5Ijp0cnVlLCJjb2xvciI6IiNGRjUxNUEifV0sInhBeGlzIjoibWV0YV9sYXN0X3VwZGF0ZSIsIm1heHBvaW50cyI6IiIsInRpbWVzY2FsZSI6InllYXIiLCJzb3J0IjoiIn1dLCJkaXNwbGF5TGVnZW5kIjp0cnVlLCJhbGlnbk1vbnRoIjp0cnVlfQ%3D%3D&location=8,48.31973,4.08966&basemap=jawg.light
def get_sante_from_api(commune, type):  #type = hospital, pharmacy, nursing_home, doctors, dentist, clinic...
    url = "https://public.opendatasoft.com/api/records/1.0/search/"
    params = {
        "dataset": "osm-france-healthcare",
        "rows": 50,  # Limite les résultats
        "q": "",
        "facet": "amenity",
        "refine.amenity": "hospital",  # Assure qu'on récupère des hôpitaux
        "refine.meta_name_com": commune  # Filtrer par commune
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        hopitaux = []

        for record in data.get("records", []):
            fields = record.get("fields", {})
            if "name" in fields and "meta_geo_point" in fields and fields.get("type") == type:
                hopitaux.append({
                    "nom": fields["name"],
                    "latitude": fields["meta_geo_point"][0],
                    "longitude": fields["meta_geo_point"][1],
                    "region": fields.get("meta_name_reg", "Inconnue"),
                    "departement": fields.get("meta_name_dep", "Inconnu"),
                    "finess": fields.get("ref_finess", "N/A"),
                    "lien_osm": fields.get("meta_osm_url", "#"),
                    "telephone": fields.get("phone", "Non renseigné"),
                    "horaires": fields.get("opening_hours", "Non renseigné"),
                    "accessibilite": fields.get("wheelchair", "Non renseigné")
                })

        return hopitaux
    else:
        print(f"Erreur API: {response.status_code}")
        return []

#vacances scolaires
# https://public.opendatasoft.com/explore/dataset/vacances-scolaires-par-zone/information/?sort=date&refine.vacances_zone_a=Vacances+d%27%C3%A9t%C3%A9&refine.date=2026&dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiQ09VTlQiLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiJyYW5nZS1jdXN0b20ifV0sInhBeGlzIjoiZGF0ZSIsIm1heHBvaW50cyI6IiIsInRpbWVzY2FsZSI6ImRheSIsInNvcnQiOiIiLCJzZXJpZXNCcmVha2Rvd24iOiJ2YWNhbmNlc196b25lX2EiLCJjb25maWciOnsiZGF0YXNldCI6InZhY2FuY2VzLXNjb2xhaXJlcy1wYXItem9uZSIsIm9wdGlvbnMiOnsic29ydCI6ImRhdGUiLCJyZWZpbmUudmFjYW5jZXNfem9uZV9hIjoiVmFjYW5jZXMgZCdcdTAwRTl0XHUwMEU5IiwicmVmaW5lLmRhdGUiOiIyMDI2In19fV0sImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9