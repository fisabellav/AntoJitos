import json
from django.shortcuts import render, HttpResponse, redirect, reverse
from crud.models import *
from login.models import *
from .models import *
from login.forms import UserForm
from .forms import SolicitudProductoForm


# Create your views here.
def index(request):
    context = {'productos':Product.objects.all(), 'request': request}
    return render(request, 'core/index.html', context)

def catalogo(request):
    # Diccionario para mapear códigos de categorías a nombres legibles
    CATEGORY_DICT = dict(Product.CATEGORY_CHOICES)

    # Obtener categorías y sabores únicos
    category_filter = list(set(Product.objects.all().values_list('category', flat=True)))
    category_filter = [CATEGORY_DICT[cat] for cat in category_filter]

    flavor_filter = list(set(Flavor.objects.all().values_list('flavor', flat=True)))

    # Obtener categorías y sabores seleccionados en el filtro
    selected_categories = request.GET.getlist('categories')
    selected_flavors = request.GET.getlist('flavors')

    # Filtrar productos
    filtered_products = Product.objects.all()

    if selected_categories:
        # Convertir nombres de categorías a sus códigos para el filtro
        selected_category_codes = [key for key, value in CATEGORY_DICT.items() if value in selected_categories]
        filtered_products = filtered_products.filter(category__in=selected_category_codes)

    if selected_flavors:
        filtered_products = filtered_products.filter(flavor__flavor__in=selected_flavors)

    context = {
        'filtro_categoria': category_filter,
        'filtro_sabor': flavor_filter,
        'productos': filtered_products,
        'request': request,
        'selected_categories': selected_categories,
        'selected_flavors': selected_flavors
    }
    return render(request, 'core/catalogo.html', context)

def filter_products(request):
    # Diccionario para mapear códigos de categorías a nombres legibles
    CATEGORY_DICT = dict(Product.CATEGORY_CHOICES)

    # Obtener categorías y sabores únicos
    category_filter = list(set(Product.objects.all().values_list('category', flat=True)))
    category_filter = [CATEGORY_DICT[cat] for cat in category_filter]

    flavor_filter = list(set(Flavor.objects.all().values_list('flavor', flat=True)))

    # Obtener categorías y sabores seleccionados en el filtro
    selected_categories = request.GET.getlist('categories')
    selected_flavors = request.GET.getlist('flavors')

    # Filtrar productos
    filtered_products = Product.objects.all()

    if selected_categories:
        # Convertir nombres de categorías a sus códigos para el filtro
        selected_category_codes = [key for key, value in CATEGORY_DICT.items() if value in selected_categories]
        filtered_products = filtered_products.filter(category__in=selected_category_codes)

    if selected_flavors:
        filtered_products = filtered_products.filter(flavor__flavor__in=selected_flavors)

    context = {
        'filtro_categoria': category_filter,
        'filtro_sabor': flavor_filter,
        'productos': filtered_products,
        'request': request,
        'selected_categories': selected_categories,
        'selected_flavors': selected_flavors
    }
    return render(request, 'core/catalogo.html', context)


def producto(request, id):
    try:
        product = Product.objects.get(id=id)
        if product:
            if request.method == 'POST':
                user_form = UserForm(request.POST, prefix='user')
                solicitud_form = SolicitudProductoForm(request.POST, prefix='solicitud')
                if user_form.is_valid() :
                    name = user_form.cleaned_data.get('name')
                    last_name = user_form.cleaned_data.get('last_name')
                    birthday = user_form.cleaned_data.get('birthday')
                    prefijo_telefono = request.POST.get('prefijo_telefono')
                    phone_number = user_form.cleaned_data.get('phone_number')
                    phone_number = ''.join(phone_number.split())  # Quitamos los espacios en blanco
                    phone_number = prefijo_telefono + phone_number
                    gender = user_form.cleaned_data.get('gender')
                    comuna = user_form.cleaned_data.get('comuna')
                    email = user_form.cleaned_data.get('email')
                    password = user_form.cleaned_data.get('password')

                    user = User.objects.create(
                        name=name,
                        last_name=last_name,
                        birthday=birthday,
                        phone_number=phone_number,
                        comuna=comuna,
                        gender=gender,
                        email=email,
                        password=password,
                    )
                    user.save()
                    
                    if solicitud_form.is_valid():

                        # Datos de la solicitud
                        quantity = solicitud_form.cleaned_data.get('quantity')
                        print(f"Quantity: {quantity}")  # Depuración
                        # Crear solicitud
                        solicitud = SolicitudProducto.objects.create(
                            user=user,
                            product=product,
                            quantity=quantity
                        )
                        solicitud.save()
                    return redirect(reverse('catalogo') + '?OK')

                else:
                    context = {
                        'producto': product,
                        'user_form': user_form,
                        'solicitud_form': solicitud_form
                    }
                    return render(request, 'core/producto.html', context)
            else:
                user_form = UserForm(prefix='user')
                solicitud_form = SolicitudProductoForm(prefix='solicitud')
                
            context = {
                'producto': product,
                'user_form': user_form,
                'solicitud_form': solicitud_form
            }
            return render(request, 'core/producto.html', context)
        else:
            return redirect(reverse('catalogo') + '?NO_EXIST')
    except Product.DoesNotExist:
        return redirect(reverse('catalogo') + '?NO_EXIST')

def contacto(request):
    try:
        if request.method == 'POST':
            user_form = UserForm(request.POST, prefix='user')
            solicitud_form = SolicitudProductoForm(request.POST, prefix='solicitud')
            if user_form.is_valid():
                name = user_form.cleaned_data.get('name')
                last_name = user_form.cleaned_data.get('last_name')
                birthday = user_form.cleaned_data.get('birthday')
                prefijo_telefono = request.POST.get('prefijo_telefono')
                phone_number = user_form.cleaned_data.get('phone_number')
                phone_number = ''.join(phone_number.split())  # Quitamos los espacios en blanco
                phone_number = prefijo_telefono + phone_number
                gender = user_form.cleaned_data.get('gender')
                comuna = user_form.cleaned_data.get('comuna')
                email = user_form.cleaned_data.get('email')
                password = user_form.cleaned_data.get('password')

                user = User.objects.create(
                    name=name,
                    last_name=last_name,
                    birthday=birthday,
                    phone_number=phone_number,
                    comuna=comuna,
                    gender=gender,
                    email=email,
                    password=password,
                )
                user.save()

                wishlist = request.POST.get('wishlist', '[]')
                wishlist_products = json.loads(wishlist)

                for item in wishlist_products:
                    product = Product.objects.get(id=item['id'])
                    SolicitudProducto.objects.create(user=user, product=product, quantity=item['quantity'])

                return redirect(reverse('contacto') + '?OK')
            else:
                context = {
                    'user_form': user_form,
                    'solicitud_form': solicitud_form
                }
                return render(request, 'core/contacto.html', context)
        else:
            user_form = UserForm(prefix='user')
            solicitud_form = SolicitudProductoForm(prefix='solicitud')
            
        context = {
            'user_form': user_form,
            'solicitud_form': solicitud_form
        }
        return render(request, 'core/contacto.html', context)
    except Product.DoesNotExist:
        return redirect(reverse('contacto') + '?NO_EXIST')

def cookies(request):
    if request.method == 'GET':
        selected_flavors = request.GET.getlist('flavors')
        
        # Filtrar productos por categoría 'GA' (Galletas) y sabores seleccionados
        productos_filtrados = Product.objects.filter(category='GA')
        if selected_flavors:
            # Filtrar por nombres de sabores en lugar de IDs
            productos_filtrados = productos_filtrados.filter(flavor__flavor__in=selected_flavors)
        
        context = {
            'productos': productos_filtrados,
            'selected_flavors': selected_flavors,
            'filtro_sabor': Flavor.objects.all(),  # Obtener todos los sabores disponibles
        }
        return render(request, 'core/cookies.html', context)

def filter_cookies(request):
    if request.method == 'GET':
        selected_flavors = request.GET.getlist('flavors')
        
        # Filtrar productos por categoría 'GA' (Galletas) y sabores seleccionados
        productos_filtrados = Product.objects.filter(category='GA')
        if selected_flavors:
            # Filtrar por nombres de sabores en lugar de IDs
            productos_filtrados = productos_filtrados.filter(flavor__flavor__in=selected_flavors)
        
        context = {
            'productos': productos_filtrados,
            'selected_flavors': selected_flavors,
            'filtro_sabor': Flavor.objects.all(),  # Obtener todos los sabores disponibles
        }
        return render(request, 'core/cookies.html', context)

def breakfast(request):
    if request.method == 'GET':
        
        # Filtrar productos por categoría 'DE' (Desayuno) y sabores seleccionados
        productos_filtrados = Product.objects.filter(category='DE')
        
        context = {
            'productos': productos_filtrados,
        }
        return render(request, 'core/breakfast.html', context)

        
def about(request):
            return render(request, 'core/about.html')

def editar_perfil(request, idUser):
    
        user = User.objects.get(idUser=id)
        form = ProductForm(instance = user)

        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance = product)

    
            if form.is_valid():
                form.save()
                return redirect(reverse('product-list') + '?UPDATED')
            else:
                return redirect(reverse('productlist-edit') + id)

        context = {'form':form}
        return render(request,'crud/product-edit.html',context)



