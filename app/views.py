
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contacto, Slider, Gallery, Mision, Vision, Insumo
from .forms import ContactoForm, InsumoForm, CustomUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import   viewsets
from .serializers import InsumoSerializer, ContactoSerializer, TokenSerializer

from django.http import JsonResponse
from rest_framework.decorators import api_view
from fcm_django.models import FCMDevice

# Create your views here.

@api_view(["POST"])
def save_token(request):
    serializador = TokenSerializer(data= request.data)

    if serializador.is_valid():
        token = serializador.data["token"]

        dispositivo = FCMDevice.objects.filter(registration_id=token, active=True).first()

        if not dispositivo:
            dispositivo = FCMDevice(registration_id=token, active=True)
        
        if request.user.is_authenticated:
            dispositivo.user = request.user

        dispositivo.save()

        return JsonResponse({"mensaje": "ok"}, status=200)
    
    return JsonResponse({"mensaje": "No se Guardo Token"}, status=400)

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
            messages.success(request, "Send")
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

        if formulario.is_valid():
            formulario.save()                
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            if request.user.is_authenticated:
                if user.is_superuser:
                    dispositivo = FCMDevice.is_superuser.all()
                    dispositivo.send_message(
                        title= "Nuevo Usuario Registrado",
                        body="Se ha ingresado un nuevo registro",
                        icon= "/media/admin-interface/favicon/logo.jpg"
                    )

        messages.success(request, "Successful registration")
        return redirect(to="index")
        data["form"] = formulario

    return render(request, 'registration/registro.html', data)



@permission_required('app.add_insumo')    
def agregar_insumo(request):


    data = {
        'form' : InsumoForm()
    }
    if request.method == 'POST':
        formulario = InsumoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()

            if request.user.is_authenticated:

                dispositivo = FCMDevice.objects.filter(active=True)
                nombre_contacto = formulario.cleaned_data["name"]
                stock_insumo = formulario.cleaned_data["Stock"]
                nombre_insumo = formulario.cleaned_data["Description"]
                dispositivo.send_message(
                    title= "Nuevo Insumo Ingresado",
                    body=f"{nombre_contacto} ha ingreso {stock_insumo} {nombre_insumo}",
                    icon= "/static/app/img/logo.jpg"
                )

            messages.success(request, "Added correctly")
        else:
            data["form"] = formulario

    return render(request,'app/insumo/agregar.html',data)


@permission_required('app.view_insumo') 
def listar_insumos(request):

    insumos = Insumo.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(insumos,10)
        insumos = paginator.page(page)
    except:
        raise Http404


    data = {
        'entity' : insumos,
        'paginator':paginator
    }

    return render(request, 'app/insumo/listar.html' , data)


@permission_required('app.change_insumo') 
def modificar_insumos(request, id):

    insumo = get_object_or_404(Insumo, id=id)

    data = {
        'form': InsumoForm(instance=insumo)
    }

    if request.method == 'POST':
        formulario = InsumoForm(data=request.POST, instance=insumo, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modified Correctly")
            return redirect(to="listar_insumos")

            data["form"] = formulario
             

    return render(request, 'app/insumo/modificar.html',data)


@permission_required('app.delete_insumo') 
def eliminar_insumos(request, id):
    insumo = get_object_or_404(Insumo, id=id)
    insumo.delete()
    messages.success(request, "Deleted correctly")
    return redirect(to="listar_insumos")



# views para el serializers

class InsumoViewset(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    
    def get_queryset(self):
        insumos = Insumo.objects.all()

        name = self.request.GET.get('name')
        Stock = self.request.GET.get('Stock')

        if name :

            insumos = insumos.filter(name__contains=name)

        if Stock:

            insumos = insumos.filter(Stock__contains=Stock)

        return  insumos


class ContactoViewset(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer

    def get_queryset(self):
        contacto = Contacto.objects.all()

        subject = self.request.GET.get('subject')
        contact_type = self.request.GET.get('contact_type')

        if subject:
            contacto = contacto.filter(subject__contains=subject)

        if contact_type:
            contacto = contacto.filter(contact_type__contains=contact_type)

        return contacto