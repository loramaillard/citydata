import csv
from django.core.management.base import BaseCommand
from visualisation.models import Aeroport

class Command(BaseCommand):
    help = "Importe les aéroports depuis un fichier CSV"

    def handle(self, *args, **kwargs):
        file_path = 'aeroports.csv'  # Mets le bon chemin

        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')  # Ajuste le délimiteur si besoin
            cnt=0
            for row in reader:
                print(row)
                if cnt>=0:
                    Aeroport.objects.create(
                        nom=row['Nom aeroport'],
                        code_oaci=row['Code OACI'],
                        code_iata=row['Code IATA'],
                        latitude_aeroport=float(row['latitude_centre']),
                        longitude_aeroport=float(row['longitude_centre']),
                        ville=row['Ville desservie']
                    )
                cnt=cnt+1
        
        self.stdout.write(self.style.SUCCESS("Import terminé !"))
