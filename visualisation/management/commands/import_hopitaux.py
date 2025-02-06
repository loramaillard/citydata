import csv
import re  # Ajout pour extraire les coordonnées
from django.core.management.base import BaseCommand
from visualisation.models import Hopital
from pyproj import Transformer

class Command(BaseCommand):
    help = "Importe les hôpitaux depuis un fichier CSV et convertit les coordonnées"

    def handle(self, *args, **kwargs):
        file_path = 'hospitals_point.csv'  # Assurez-vous du bon chemin du fichier

        # Transformateur de coordonnées (EPSG:3857 → EPSG:4326)
        transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')  # Ajuster si besoin
            
            for row in reader:
                try:
                    # Vérification des données
                    nom = row.get('name', '').strip()
                    geom = row.get('the_geom', '').strip()

                    if not nom or not geom.startswith("POINT"):
                        continue  # Ignorer les entrées sans nom ou sans géométrie valide

                    # Extraction correcte des coordonnées X et Y avec regex
                    match = re.match(r'POINT \(([-\d.]+) ([-\d.]+)\)', geom)
                    if not match:
                        continue  # Ignorer les entrées mal formatées

                    x_mercator, y_mercator = map(float, match.groups())

                    # Conversion des coordonnées
                    longitude, latitude = transformer.transform(x_mercator, y_mercator)

                    # Création de l'hôpital dans la base de données
                    Hopital.objects.create(
                        nom=nom,
                        latitude_hopital=latitude,
                        longitude_hopital=longitude
                    )

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erreur avec {nom}: {e}"))

        self.stdout.write(self.style.SUCCESS("Import des hôpitaux terminé !"))
