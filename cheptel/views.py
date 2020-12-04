from django.shortcuts import render, get_object_or_404
from .models import Animal, Equipement
from .forms import AnimalForm
from django.shortcuts import redirect


def home(request):
    animaux = Animal.objects.order_by('id_animal')
    equipements = Equipement.objects.order_by('id_equip')
    return render(request, 'cheptel/home.html', {'animaux': animaux, 'equipements': equipements})


def animal_detail(request, pk, modal=None):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'cheptel/animal_detail.html', {'animal': animal, 'modal': modal})


def equip_detail(request, pk):
    equip = get_object_or_404(Equipement, pk=pk)
    animaux = Animal.objects.filter(lieu=equip)
    return render(request, 'cheptel/equip_detail.html', {'equip': equip, 'animaux': animaux})


def nourrir(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if animal.etat == "affamé":
        mangeoire = get_object_or_404(Equipement, pk="Mangeoire")
        if mangeoire.disponibilite == "Occupé":
            return animal_detail(request, pk, "Nourrir_no")
        else :
            animal.lieu = mangeoire
            mangeoire.disponibilite = "Occupé"
            animal.etat = "repus"
            animal.save()
            mangeoire.save()
            return animal_detail(request, pk, "Nourrir_ok")
    return animal_detail(request, pk)


def divertir(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if animal.etat == "repus":
        roue = get_object_or_404(Equipement, pk="Roue")
        if roue.disponibilite == "Occupé":
            return animal_detail(request, pk, "Divertir_no")
        else:
            animal.lieu = roue
            mangeoire = get_object_or_404(Equipement, pk="Mangeoire")
            mangeoire.disponibilite = "Libre"
            roue.disponibilite = "Occupé"
            animal.etat = "fatigué"
            animal.save()
            mangeoire.save()
            roue.save()
            return animal_detail(request, pk, "Divertir_ok")
    return animal_detail(request, pk)

def coucher(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if animal.etat == "fatigué":
        nid = get_object_or_404(Equipement, pk="Nid")
        if nid.disponibilite == "Occupé":
            return animal_detail(request, pk, "Coucher_no")
        else :
            animal.lieu = nid
            roue = get_object_or_404(Equipement, pk="Roue")
            roue.disponibilite = "Libre"
            nid.disponibilite = "Occupé"
            animal.etat = "endormi"
            animal.save()
            nid.save()
            roue.save()
            return animal_detail(request, pk, "Coucher_ok")
    return animal_detail(request, pk)

def reveiller(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if animal.etat == "endormi":
        litiere = get_object_or_404(Equipement, pk="Litière")
        animal.lieu = litiere
        nid = get_object_or_404(Equipement, pk="Nid")
        nid.disponibilite = "Libre"
        animal.etat = "affamé"
        animal.save()
        nid.save()
        return animal_detail(request, pk, "Reveiller_ok")
    return animal_detail(request, pk)


def animal_new(request):
    if request.method == "POST":
        form = AnimalForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.etat = "affamé"
            animal.lieu = get_object_or_404(Equipement, pk="Litière")
            animal.save()
            return redirect('animal_detail', pk=animal.pk)
    else:
        form = AnimalForm()
    return render(request, 'cheptel/animal_edit.html', {'form': form})


def animal_edit(request, pk):
    post = get_object_or_404(Animal, pk=pk)
    if request.method == "POST":
        form = AnimalForm(request.POST, instance=post)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.save()
            return redirect('animal_detail', pk=animal.pk)
    else:
        form = AnimalForm(instance=post)
    return render(request, 'cheptel/animal_edit.html', {'form': form})
