from django import forms
from .models import Client, Produit

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        exclude = ['prix_total_ttc']

    def __init__(self, *args, **kwargs):
        categorie = kwargs.pop('categorie', None)
        super().__init__(*args, **kwargs)
        if categorie:
            self.fields['nom'].queryset = Produit.objects.filter(categorie=categorie)
        else:
            self.fields['nom'].queryset = Produit.objects.none()