from django.db import models

class Commune(models.Model):
    codgeo = models.CharField(max_length=10, null=True, blank=True)
    libgeo = models.CharField(max_length=100, null=True, blank=True)
    med14 = models.FloatField(null=True, blank=True)
    nombre_batiments_historique = models.IntegerField(null=True, blank=True)
    nombre_hopitaux = models.IntegerField(null=True, blank=True)
    nombre_crime = models.IntegerField(null=True, blank=True)
    nombre_ecole = models.IntegerField(null=True, blank=True)
    p21_pop = models.FloatField(null=True, blank=True)
    p21_pop0014 = models.FloatField(null=True, blank=True)
    p21_pop1529 = models.FloatField(null=True, blank=True)
    p21_pop3044 = models.FloatField(null=True, blank=True)
    p21_pop4559 = models.FloatField(null=True, blank=True)
    p21_pop6074 = models.FloatField(null=True, blank=True)
    p21_pop7589 = models.FloatField(null=True, blank=True)
    p21_pop90p = models.FloatField(null=True, blank=True)
    p21_pop1564 = models.FloatField(null=True, blank=True)
    p21_pop1524 = models.FloatField(null=True, blank=True)
    p21_pop2554 = models.FloatField(null=True, blank=True)
    p21_chom1564 = models.FloatField(null=True, blank=True)
    p21_chom1524 = models.FloatField(null=True, blank=True)
    p21_chom2554 = models.FloatField(null=True, blank=True)
    nombre_cinemas = models.IntegerField(null=True, blank=True)
    nombre_musees = models.IntegerField(null=True, blank=True)
    nombre_festivals = models.IntegerField(null=True, blank=True)
    nb_mutations = models.FloatField(null=True, blank=True)
    nb_maisons = models.FloatField(null=True, blank=True)
    nb_apparts = models.FloatField(null=True, blank=True)
    propmaison = models.FloatField(null=True, blank=True)
    propappart = models.FloatField(null=True, blank=True)
    prix_moyen = models.FloatField(null=True, blank=True)
    prix_m2_moyen = models.FloatField(null=True, blank=True)
    surface_moy = models.FloatField(null=True, blank=True)
    nombre_gare = models.IntegerField(null=True, blank=True)
    dynamique_entrepreneuriale = models.FloatField(null=True, blank=True)
    dynamique_entrepreneuriale_service_et_commerce = models.FloatField(null=True, blank=True)
    synergie_medicale_commune = models.FloatField(null=True, blank=True)
    indice_synergie_medicale = models.FloatField(null=True, blank=True)
    nb_omnipraticiens_bv = models.FloatField(null=True, blank=True)
    nb_infirmiers_liberaux_bv = models.FloatField(null=True, blank=True)
    nb_dentistes_liberaux_bv = models.FloatField(null=True, blank=True)
    nb_pharmaciens_liberaux_bv = models.FloatField(null=True, blank=True)
    densite_medicale_bv = models.FloatField(null=True, blank=True)
    indice_demographique = models.FloatField(null=True, blank=True)
    indice_menages = models.FloatField(null=True, blank=True)
    evolution_pop_percent = models.FloatField(null=True, blank=True)
    nb_menages = models.FloatField(null=True, blank=True)
    nb_residences_principales = models.FloatField(null=True, blank=True)
    nb_proprietaire = models.FloatField(null=True, blank=True)
    nb_logement = models.FloatField(null=True, blank=True)
    nb_residences_secondaires = models.FloatField(null=True, blank=True)
    nb_log_vacants = models.FloatField(null=True, blank=True)
    nb_entreprises_secteur_services = models.FloatField(null=True, blank=True)
    nb_entreprises_secteur_commerce = models.FloatField(null=True, blank=True)
    nb_entreprises_secteur_construction = models.FloatField(null=True, blank=True)
    nb_entreprises_secteur_industrie = models.FloatField(null=True, blank=True)
    nb_creation_entreprises = models.FloatField(null=True, blank=True)
    nb_creation_industrielles = models.FloatField(null=True, blank=True)
    nb_creation_construction = models.FloatField(null=True, blank=True)
    nb_creation_commerces = models.FloatField(null=True, blank=True)
    nb_creation_services = models.FloatField(null=True, blank=True)
    nb_logement_secondaire_et_occasionnel = models.FloatField(null=True, blank=True)
    nb_hotel = models.FloatField(null=True, blank=True)
    nb_camping = models.FloatField(null=True, blank=True)
    taux_propriete = models.FloatField(null=True, blank=True)
    dynamique_demographique_insee = models.FloatField(null=True, blank=True)
    capacite_fiscale = models.FloatField(null=True, blank=True)
    nb_education_sante_action_sociale = models.FloatField(null=True, blank=True)
    nb_services_personnels_et_domestiques = models.FloatField(null=True, blank=True)
    nb_sante_action_sociale = models.FloatField(null=True, blank=True)
    nb_de_commerce = models.FloatField(null=True, blank=True)
    nb_de_services_aux_particuliers = models.FloatField(null=True, blank=True)
    nb_institution_de_education_sante_action_sociale_administration = models.FloatField(null=True, blank=True)
    score_croissance_population = models.FloatField(null=True, blank=True)
    score_croissance_entrepreneuriale = models.FloatField(null=True, blank=True)
    longitude_centre = models.FloatField(null=True, blank=True)
    latitude_centre = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.libgeo

class Aeroport(models.Model):
    nom = models.CharField(max_length=255)
    code_oaci = models.CharField(max_length=10, blank=True, null=True)
    code_iata = models.CharField(max_length=10, blank=True, null=True)
    latitude_aeroport = models.FloatField()
    longitude_aeroport = models.FloatField()
    ville = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

from django.db import models

class Centrale(models.Model):
    nom = models.CharField(max_length=255)
    combustible = models.CharField(max_length=255)
    sous_filiere = models.CharField(max_length=255)
    date_mise_en_service = models.DateField()
    puissance_installee = models.FloatField()
    puissance_minimum = models.FloatField()
    reserve_secondaire = models.FloatField()
    region = models.CharField(max_length=255)
    departement = models.CharField(max_length=255)
    commune = models.CharField(max_length=255)
    latitude_centrale = models.FloatField()
    longitude_centrale = models.FloatField()

    def __str__(self):
        return self.nom


class Hopital(models.Model):
    nom = models.CharField(max_length=255, null=True, blank=True)
    latitude_hopital = models.FloatField()
    longitude_hopital = models.FloatField()

    def __str__(self):
        return self.nom if self.nom else "Hôpital sans nom"
    


class Ecole(models.Model):
    nom = models.CharField(max_length=255)
    latitude_ecole = models.FloatField()
    longitude_ecole = models.FloatField()
    secteur = models.CharField(max_length=50, blank=True, null=True)
    nature = models.CharField(max_length=100, blank=True, null=True)
    nom_commune = models.CharField(max_length=100)  # 🔹 Nouveau champ

    def __str__(self):
        return f"{self.nom} - {self.nom_commune}"


