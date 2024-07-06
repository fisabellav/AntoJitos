from django.shortcuts import render, get_object_or_404, redirect, reverse  
from .models import *
from core.models import *
from .forms import *
from django.contrib import messages



# Create your views here.


def product_list(request):
    if 'usuario' in request.session:
        usuario = request.session['usuario']
        if usuario.get('rol') == 'ADMIN':
            CATEGORY_DICT = dict(Product.CATEGORY_CHOICES)
            productos = Product.objects.all()
            
            context = {
                'productos': productos,
                'category_dict': CATEGORY_DICT,
                'request': request
            }
            return render(request, 'crud/product-list.html', context)
        else:
            messages.error(request, "No tienes permisos para ver esta página.")
            request.session['level_mensaje'] = 'alert-danger'
            return redirect(reverse('login'))
    else:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        request.session['level_mensaje'] = 'alert-danger'
        return redirect(reverse('login'))

def order_list(request):
    if 'usuario' in request.session:
        usuario = request.session['usuario']
        if usuario.get('rol') == 'ADMIN':
            CATEGORY_DICT = dict(Product.CATEGORY_CHOICES)
            solicitudes = SolicitudProducto.objects.all()

            
            context = {
                'solicitudes': solicitudes,
                'category_dict': CATEGORY_DICT,
                'request': request
            }
            return render(request, 'crud/order-list.html', context)
        else:
            messages.error(request, "No tienes permisos para ver esta página.")
            request.session['level_mensaje'] = 'alert-danger'
            return redirect(reverse('login'))
    else:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        request.session['level_mensaje'] = 'alert-danger'
        return redirect(reverse('login'))

def filter_by_category(request, category):
    try:
        if 'usuario' in request.session:
            usuario = request.session['usuario']
            if usuario.get('rol') == 'ADMIN':
                productos = Product.objects.filter(category=category)
                CATEGORY_DICT = dict(Product.CATEGORY_CHOICES)

                context = {
                    'productos': productos,
                    'category_dict': CATEGORY_DICT,
                    'request': request,
                }
                return render(request, 'crud/product-list.html', context)
            else:
                messages.error(request, "No tienes permisos para ver esta página.")
                request.session['level_mensaje'] = 'alert-danger'
                return redirect(reverse('login'))
        else:
            messages.error(request, "Debes iniciar sesión para acceder a esta página.")
            request.session['level_mensaje'] = 'alert-danger'
            return redirect(reverse('login'))
    except:
        return redirect('login')


def filter_by_flavor(request, flavor):
    try:
        if 'usuario' in request.session:
            usuario = request.session['usuario']
            if usuario.get('rol') == 'ADMIN':
                productos = Product.objects.filter(flavor__flavor=flavor)
                CATEGORY_DICT = dict(Product.CATEGORY_CHOICES)

                context = {
                    'productos': productos,
                    'category_dict': CATEGORY_DICT,
                    'request': request,
                }
                return render(request, 'crud/product-list.html', context)
            else:
                messages.error(request, "No tienes permisos para ver esta página.")
                request.session['level_mensaje'] = 'alert-danger'
                return redirect(reverse('login'))
        else:
            messages.error(request, "Debes iniciar sesión para acceder a esta página.")
            request.session['level_mensaje'] = 'alert-danger'
            return redirect(reverse('login'))
    except:
        return redirect('login')


def add_product(request):
    try:
        if 'usuario' in request.session:
            usuario = request.session['usuario']
            if usuario.get('rol') == 'ADMIN':
                if request.method == 'POST':
                    form = ProductForm(request.POST, request.FILES)
                    if form.is_valid():
                        product = form.cleaned_data.get('product')
                        description = form.cleaned_data.get('description')
                        price = form.cleaned_data.get('price')
                        image = form.cleaned_data.get('image')
                        category = form.cleaned_data.get('category')
                        flavor = form.cleaned_data.get('flavor')

                        # Crear el objeto Product usando los datos limpios
                        obj = Product.objects.create(
                            product=product,
                            description=description,
                            price=price,
                            image=image,
                            category=category,
                        )
                        # Añadir sabores al producto utilizando el campo ManyToMany
                        obj.flavor.set(flavor)

                        obj.save()

                        return redirect(reverse('product-list') + '?OK')
                    else:
                        return redirect(reverse('add-product') + '?FAIL')
                else:
                    form = ProductForm()

                return render(request, 'crud/add-product.html', {'form': form})
            else:
                messages.error(request, "No tienes permisos para ver esta página.")
                request.session['level_mensaje'] = 'alert-danger'
                return redirect(reverse('login'))
        else:
            messages.error(request, "Debes iniciar sesión para acceder a esta página.")
            request.session['level_mensaje'] = 'alert-danger'
            return redirect(reverse('login'))
    except:
        return redirect('login')


def productlist_delete(request, id):
    try:
        if 'usuario' in request.session:
            usuario = request.session['usuario']
            if usuario.get('rol') == 'ADMIN':
                product = Product.objects.get(id=id)
                product.delete()
                return redirect(reverse('product-list') + '?DELETED')
            else:
                messages.error(request, "No tienes permisos para ver esta página.")
                request.session['level_mensaje'] = 'alert-danger'
                return redirect(reverse('login'))
        else:
            messages.error(request, "Debes iniciar sesión para acceder a esta página.")
            request.session['level_mensaje'] = 'alert-danger'
            return redirect(reverse('login'))
    except:
        return redirect(reverse('product-list') + '?FAIL')


def productlist_edit(request, id):
    if 'usuario' in request.session:
        usuario = request.session['usuario']
        if usuario.get('rol') == 'ADMIN':
            product = Product.objects.get(id=id)
            form = ProductForm(instance=product)

            if request.method == 'POST':
                form = ProductForm(request.POST, request.FILES, instance=product)

                if form.data.get('image_clear') == 'on':
                    product.image.delete(save=False)
                    form.instance.image = None  # Eliminar la referencia a la imagen en el formulario

                if form.is_valid():
                    form.save()
                    return redirect(reverse('product-list') + '?UPDATED')
                else:
                    return redirect(reverse('productlist-edit') + id)

            context = {'form': form}
            return render(request, 'crud/product-edit.html', context)
        else:
            messages.error(request, "No tienes permisos para ver esta página.")
            request.session['level_mensaje'] = 'alert-danger'
            return redirect(reverse('login'))
    else:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        request.session['level_mensaje'] = 'alert-danger'
        return redirect(reverse('login'))


def product_detail(request, id):
    if 'usuario' in request.session:
        usuario = request.session['usuario']
        if usuario.get('rol') == 'ADMIN':
            product = get_object_or_404(Product, id=id)
            CATEGORY_DICT = dict(Product.CATEGORY_CHOICES)

            context = {
                'producto': product,
                'category_dict': CATEGORY_DICT
            }
            return render(request, 'crud/detail.html', context)
        else:
            messages.error(request, "No tienes permisos para ver esta página.")
            request.session['level_mensaje'] = 'alert-danger'
            return redirect(reverse('login'))
    else:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        request.session['level_mensaje'] = 'alert-danger'
        return redirect(reverse('login'))