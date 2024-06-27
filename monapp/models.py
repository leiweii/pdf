from django.db import models

class Client(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=20)
    email = models.EmailField()
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Produit(models.Model):
    CATEGORIE_CHOICES = [
        ('papeterie', 'Papeterie'),
        ('electronique', 'Électronique'),
    ]
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    nom = models.CharField(max_length=100)
    quantite = models.IntegerField(default=0)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2)
    remise = models.DecimalField(max_digits=5, decimal_places=2)
    prix_total_ttc = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        self.prix_total_ttc = (self.prix_unitaire * self.quantite) * (1 + self.taux_tva / 100) * (1 - self.remise / 100)
        super().save(*args, **kwargs)