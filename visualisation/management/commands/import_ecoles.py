import csv
from django.core.management.base import BaseCommand
from visualisation.models import Ecole

class Command(BaseCommand):
    help = "Importe les écoles depuis un fichier CSV"

    def handle(self, *args, **kwargs):
        file_path = 'ecoles.csv'  # Assurez-vous du bon chemin

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')  # Adapter si autre séparateur

            for row in reader:
                try:
                    nom = row.get('appellation_officielle', '').strip()
                    latitude = row.get('latitude', '').strip()
                    longitude = row.get('longitude', '').strip()
                    secteur = row.get('secteur_public_prive_libe', '').strip()
                    nature = row.get('nature_uai_libe', '').strip()
                    nom_commune = row.get('libelle_commune', '').strip()
                    if not nom or not latitude or not longitude:
                        continue  # Ignorer les entrées incomplètes

                    # Conversion en float
                    latitude = float(latitude)
                    longitude = float(longitude)
                    print(nom, latitude, longitude)
                    # Création dans la base de données
                    Ecole.objects.create(
                        nom=nom,
                        latitude_ecole=latitude,
                        longitude_ecole=longitude,
                        secteur=secteur,
                        nature=nature,
                        nom_commune=nom_commune
                    )

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erreur avec {nom}: {e}"))

        self.stdout.write(self.style.SUCCESS("Import des écoles terminé !"))
