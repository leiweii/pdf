from django.shortcuts import render, redirect
from .models import Client, Produit
from .forms import ClientForm, ProduitForm
from django.views.generic import View
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def saisie_informations(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            client = client_form.save()
            request.session['client_nom'] = client.nom
            request.session['client_prenom'] = client.prenom
            return redirect('liste_produits')
    else:
        client_form = ClientForm()

    return render(request, 'saisie_informations.html', {'client_form': client_form})


def ajouter_produit(request):
    if request.method == 'POST':
        produit_form = ProduitForm(request.POST)
        if produit_form.is_valid():
            produit = produit_form.save()
            return redirect('liste_produits')
    else:
        produit_form = ProduitForm()
    
    return render(request, 'ajouter_produit.html', {'produit_form': produit_form})

def liste_produits(request):
    produits = Produit.objects.all()
    client_nom = request.session.get('client_nom', None)
    client_prenom = request.session.get('client_prenom', None)

    return render(request, 'liste_produits.html', {'produits': produits, 'client_nom': client_nom, 'client_prenom': client_prenom})

def supprimer_produit(request, pk):
    produit = Produit.objects.get(pk=pk)
    if request.method == 'POST':
        produit.delete()
        return redirect('liste_produits')
    return render(request, 'supprimer_produit.html', {'produit': produit})

from django.templatetags.static import static  # Importer la fonction static

class GenererPDF(View):
    def get(self, request):
        dernier_client = Client.objects.last()
        produits = Produit.objects.all()
        
        template = get_template('facture.html')
        
        # Construire le chemin complet vers l'image
        logo_path = request.build_absolute_uri(static('images/logo.jpg'))
        
        context = {
            'client': dernier_client,
            'produits': produits,
            'logo_path': logo_path,  # Ajouter le chemin de l'image au contexte
        }
        html = template.render(context)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="facture.pdf"'
        
        # Générer le PDF à partir du HTML rendu
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('Nous avons rencontré des erreurs lors de la génération du PDF <pre>' + html + '</pre>')
        
        return response