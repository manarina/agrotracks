from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
class Role(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('agriculteur', 'Agriculteur'),
        ('chercheur', 'Chercheur'),
    ]

    nom = models.CharField(max_length=255, unique=True, choices=ROLE_CHOICES, default='admin')
    
    def __str__(self):
        return self.nom

class User(AbstractUser):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, max_length=255)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/avatars/', default='uploads/avatars/avatar1.jpg')
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_users",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_users",
        related_query_name="custom_user",
    )

class Commune(models.Model):
    nom = models.CharField(max_length=255)

    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création de commune")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification de commune")

    def __str__(self):
        return f"{self.nom}"

    class Meta:
        ordering = ['date_creation']


class District(models.Model):
    nom = models.CharField(max_length=255)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name="districts_commune", verbose_name=_("Commune"),)

    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création de district")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification de district")

    def __str__(self):
        return f"{self.nom}"

    class Meta:
        ordering = ['date_creation']


class Region(models.Model):
    nom = models.CharField(max_length=255)

    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="regions_district", verbose_name=_("District"),)

    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création de region")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification de region")    

    def __str__(self):
        return f"{self.nom}"

    class Meta:
        ordering = ['date_creation']
    

class ZonePlantation(models.Model):
    localisation = models.CharField(max_length=255)

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="zonePlantations_region", verbose_name=_("Region"),)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="zonePlantations_district", verbose_name=_("District"),)      
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name="zonePlantations_commune", verbose_name=_("Commune"),)

    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création de zone plantation")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification de zone plantation")    

    def __str__(self):
        return f"{self.localisation}"

    class Meta:
        ordering = ['date_creation']
        

class Plantation(models.Model):
    
    TYPE_CHOICES = [
     (_('agroforesterie'), _('AgroForesterie')),
     (_('mangroves'), _('Mangroves')),  
     (_('agricultures'), _('Agricultures')),
     (_('permaculture'), _('Permaculture')),   
    ]

    ETAT_CHOICES = [
       (_('en preparation'), _('En preparation')),
       (_('en germination'), _('En germination')),
       (_('en croissance'), _('En Croissance')),
       (_('semee'), _('Semee')),
       (_('en repos'), _('En repos')),
       (_('endommagee'), _('Endommagee')),
       (_('abandonnee'), _('Abandonnee')),
       (_('replantee'), _('Replantee')),
    ]

    nomPlantation = models.CharField(max_length=255, help_text="Nom de plantation")
    typePlantation = models.CharField(max_length=255, choices=TYPE_CHOICES, verbose_name=_("Type de plantation"),)
    emplacements =  models.ForeignKey(ZonePlantation, on_delete=models.CASCADE, related_name="plantations_zonePlantation", verbose_name=_("Emplacements"),)
    
    etat = models.CharField(max_length=255, choices=ETAT_CHOICES, verbose_name=_("Etats de plantation"),)
    datePlantation = models.DateField(auto_now_add=True, verbose_name=_("Date de plantation"))

    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création de la plantation")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification de la plantation") 

    def __str__(self):
        return f"{self.nomPlantation}"

    class Meta:
        ordering = ['datePlantation']



class GuidePlantation(models.Model):
    titre = models.CharField(max_length=255, help_text="Titre")
    contenu = models.CharField(max_length=255, help_text="Contenu")

    plantations = models.ForeignKey(Plantation, on_delete=models.CASCADE, related_name="guidePlantations_Plantation", verbose_name=_("Plantation"),)

    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création de la pepiniere")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification de la pepiniere")

    def __str__(self):
        return f"{self.titre}"

    class Meta:
        ordering = ['date_creation']


class SuiviPlantation(models.Model):
    hauteur = models.FloatField(default=0.00, null=True, blank=True, verbose_name=_("Hauteur de plantation"),)
    diametre = models.FloatField(default=0.00, null=True, blank=True, verbose_name=_("Diametre de plantation"),)
    
    plantations = models.ForeignKey(Plantation, on_delete=models.CASCADE, related_name="suiviPlantations_Plantation", verbose_name=_("Plantation"),)

    observation = models.CharField(max_length=255,help_text="Observation")
    dateSuivi = models.DateField(auto_now_add=True, verbose_name=_("Date de suivi de plantation"))

    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création de la suiuvi")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification de la suivi")

    class Meta:
        ordering = ['date_creation']

class Pepiniere(models.Model):
    
    quantiteStock = models.IntegerField(default=0,blank=True, verbose_name=_("Quantite Stock"), null=True)
    capaciteProd = models.IntegerField(default=0, blank=True, verbose_name=_("Capacite de Production"), null=True)

    typePlants = models.ForeignKey(Plantation, on_delete=models.CASCADE, related_name="pepinieres_Plantation", verbose_name=_("TypePlants"),)
    
    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création de la pepiniere")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification de la pepiniere") 

    class Meta:
        ordering = ['date_creation']


class PhotoGallery(models.Model):
     
    description = models.CharField(max_length=255,help_text="Description")
    photos = models.ImageField(upload_to='uploads/photos', null=True, blank=True)
    videos = models.FileField(upload_to='uploads/videos', null=True, blank=True)

    plantations = models.ForeignKey(Plantation, on_delete=models.CASCADE, related_name="photoGallerys_Plantation", verbose_name=_("Plantation"),)

    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création de la suiuvi")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification de la suivi")

    
    def __str__(self):
        return f"{self.description}"

    class Meta:
        ordering = ['date_creation']

class Forum(models.Model):
    topic = models.CharField(max_length=255,help_text="Topic")
    message = models.CharField(max_length=255,help_text="Message")

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Utilisateur"), related_name="forums_utilisateur", to_field='email')
   
    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création de forum")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification de forum")

    def __str__(self):
        return f"{self.topic}"

    class Meta:
        ordering = ['date_creation']

class Rapport(models.Model):
    titre = models.CharField(max_length=255,help_text="Titre")
    contenu = models.CharField(max_length=255,help_text="Contenu")

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Utilisateur"), related_name="rapports_utilisateur", to_field='email')
   
    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création de rapport")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification de rapport")

    def __str__(self):
        return f"{self.titre}"

    class Meta:
        ordering = ['date_creation']
