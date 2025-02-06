import csv
from django.core.management.base import BaseCommand
from visualisation.models import Centrale

class Command(BaseCommand):
    help = "Importe les aéroports depuis un fichier CSV"

    def handle(self, *args, **kwargs):
        file_path = 'data_centrale.csv'  # Mets le bon chemin

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')  # Ajuste le délimiteur si besoin
            for row in reader:
                Centrale.objects.create(
                    nom=row['Centrale'],
                    combustible=row['Combustible'],
                    sous_filiere=row['Sous-filière'],
                    date_mise_en_service=row['Date de mise en service industrielle'],
                    puissance_installee=row['Puissance installée (MW)'],
                    puissance_minimum=row['Puissance minimum de conception (MW)'],
                    reserve_secondaire=row['Réserve secondaire maximale (MW)'],
                    region=row['Région'],
                    departement=row['Département'],
                    commune=row['Commune'],
                    latitude_centrale=row['latitude_centre'],
                    longitude_centrale=row['longitude_centre'],
                )
        
        self.stdout.write(self.style.SUCCESS("Import terminé !"))


