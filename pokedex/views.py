from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from .models import Pokemon, Trainer
from .forms import PokemonForm, TrainerForm
#Importaciones de libreria de autenticacion de Django
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


def index(request):
    #pokemons = Pokemon.objects.all() ## SELECT * FROM pokedex_pokemon
    pokemons = Pokemon.objects.order_by('type') ## SELECT * FROM pokedex_pokemon ORD
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'pokemons': pokemons}, request))

def index(request):
    #pokemons = Pokemon.objects.all() ## SELECT * FROM pokedex_pokemon
    trainers = Trainer.objects.order_by('type') ## SELECT * FROM pokedex_pokemon ORD
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'trainers': trainers}, request))

@login_required
def pokemon(request, pokemon_id):
    #SELECT * FROM pokedex_pokemon WHERE id='pokemon_id'
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    template = loader.get_template('display_pokemon.html')
    context = {
        'pokemon': pokemon
    }
    return HttpResponse(template.render(context, request))

@login_required
def trainer(request, trainer_id):
    #SELECT * FROM pokedex_pokemon WHERE id='pokemon_id'
    trainer = get_object_or_404(Trainer, id=trainer_id)
    template = loader.get_template('display_trainer.html')
    context = {
        'trainer': trainer
    }
    return HttpResponse(template.render(context, request))

@login_required
def add_pokemon(request):
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pokedex:index')
    else:
        form = PokemonForm()
        
    return render(request, 'pokemon_form.html', {'form':form})

@login_required
def add_trainer(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pokedex:index')
    else:
        form = TrainerForm()
        
    return render(request, 'trainer_form.html', {'form':form})

@login_required
def edit_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, pk = id)
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect('pokedex:index')
    else:
        form = PokemonForm(instance=pokemon)
        
    return render(request, 'pokemon_form.html', {'form':form})

@login_required
def edit_trainer(request, id):
    pokemon = get_object_or_404(Trainer, pk = id)
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('pokedex:index')
    else:
        form = PokemonForm(instance=trainer)
        
    return render(request, 'trainer_form.html', {'form':form})
    
@login_required 
def delete_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, pk = id) 
    pokemon.delete() 
    return redirect('pokedex:index')

@login_required 
def delete_trainer(request, id):
    trainer = get_object_or_404(Trainer, pk = id) 
    trainer.delete() 
    return redirect('pokedex:index')

class CustomLoginView(LoginView):
    template_name = "login.html"

