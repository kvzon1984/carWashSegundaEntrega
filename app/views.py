from django.shortcuts import render, redirect, get_object_or_404
from .models import Slider, Gallery, Mision, Vision, Insumo, User
from .forms import ContactoForm, InsumoForm, CustomUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
<<<<<<< HEAD
from django.http import Http404
=======
from django.contrib.auth import authenticate, login
>>>>>>> 48b193230a3a3c1af2e30dff44d8b10c8ce64f94

# Create your views here.

def index(request):
    slider = Slider.objects.all()
    mision = Mision.objects.all()
    vision = Vision.objects.all()
    data = {
        'slider': slider,
        'mision': mision,
        'vision': vision 
    }
    return render(request, 'app/index.html', data)


def contacto(request):
    data = {
        'form': ContactoForm()
    }

    if request.method == 'POST':
        formulario = ContactoForm (data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "contacto guardado" 
        else:
            data["form"] = formulario

    return render(request, 'app/contacto.html',data)

def galeria(request):
    gallery = Gallery.objects.all()
    data = {
        'gallery': gallery
    }

    return render(request, 'app/galeria.html', data)

def registro(request):

    data = {
        'form' : CustomUserCreationForm()
    }
    
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formurario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Se a registrado de forma correcta")
            return redirect(to="index")
        data["form"] = formulario

    return render(request, 'registration/registro.html', data)

    
def agregar_insumo(request):


    data = {
        'form' : InsumoForm()
    }
    if request.method == 'POST':
        formulario = InsumoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Agregado correctamente")
        else:
            data["form"] = formulario

    return render(request,'app/insumo/agregar.html',data)



def listar_insumos(request):

    insumos = Insumo.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(insumos,5)
        insumos = paginator.page(page)
    except:
        raise Http404


    data = {
        'entity' : insumos,
        'paginator':paginator
    }

    return render(request, 'app/insumo/listar.html' , data)


def modificar_insumos(request, id):

    insumo = get_object_or_404(Insumo, id=id)

    data = {
        'form': InsumoForm(instance=insumo)
    }

    if request.method == 'POST':
        formulario = InsumoForm(data=request.POST, instance=insumo, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="listar_insumos")

            data["form"] = formulario
             

    return render(request, 'app/insumo/modificar.html',data)

def eliminar_insumos(request, id):
    insumo = get_object_or_404(Insumo, id=id)
    insumo.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="listar_insumos")