import json
from django.shortcuts import render, HttpResponse, redirect, reverse
from crud.models import *
from login.models import *
from .models import *
from django.contrib import messages
from login.forms import UserForm
from .forms import OrderDetailForm, OrderForm
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
import bcrypt


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
        producto = Product.objects.get(id=id)

        if request.method == 'POST':
            user_form = UserForm(request.POST, prefix='')
            orderdetail_form = OrderDetailForm(request.POST, prefix='order-detail')
            order_form = OrderForm(request.POST, prefix='order')

            # Obtener datos del formulario POST
            name = request.POST.get('name')
            last_name = request.POST.get('last_name')
            birthday = request.POST.get('birthday')
            comuna = request.POST.get('comuna')
            gender = request.POST.get('gender')
            phone_number = request.POST.get('formatted_phone_number')
            email = request.POST.get('email')
            password = request.POST.get('password', '')

            # Comprueba si ya existe un usuario con el correo electrónico o el número de teléfono
            existing_user_email = User.objects.filter(email=email).first()
            existing_user_phone = User.objects.filter(phone_number=phone_number).first()
            
            if existing_user_email or existing_user_phone:
                existing_user = existing_user_email if existing_user_email else existing_user_phone

                if password:
                    if existing_user and not existing_user.password:
                        # Generate a unique token for verification
                        verification_token = get_random_string(length=32)
                        
                        # Save the token with the user record
                        existing_user.verification_token = verification_token
                        existing_user.save()
                        
                        # Send an email with a link for completing registration
                        verification_link = reverse('complete-registration', kwargs={'token': verification_token})
                        verification_url = request.build_absolute_uri(verification_link)
                        
                        send_mail(
                            'Completa tu registro en nuestro sitio',
                            f'Para completar tu registro, haz clic en el siguiente enlace: {verification_url}',
                            'noreply@tudominio.com',
                            [existing_user.email],
                            fail_silently=False,
                        )
                        request.session['level_mensaje'] = 'alert-warning'
                        messages.warning(request, "El correo o teléfono ya están registrados. Se ha enviado un correo para completar tu registro.")
                        return redirect(reverse('login'))
                else:   
                
                    context = {
                        'user_form': user_form,
                        'orderdetail_form': orderdetail_form,
                        'order_form': order_form,
                        'producto': producto
                    }
                    request.session['level_mensaje'] = 'alert-warning'
                    messages.warning(request, "El correo o teléfono ya están asociados a una cuenta. Inicie sesión, ingrese una contraseña para registrarse o corrija sus datos.")
                    return render(request, 'core/producto.html', context)
            else:

                if user_form.is_valid() and  orderdetail_form.is_valid():

                    name = user_form.cleaned_data.get('name')
                    last_name = user_form.cleaned_data.get('last_name')
                    birthday = user_form.cleaned_data.get('birthday')
                    comuna = user_form.cleaned_data.get('comuna')
                    gender = user_form.cleaned_data.get('gender')
                    phone_number = user_form.cleaned_data.get('formatted_phone_number')

                    email = user_form.cleaned_data.get('email')
                    password = user_form.cleaned_data.get('password', '')

                    quantity = orderdetail_form.cleaned_data.get('quantity')
                    print(quantity)
                    postData = request.POST.copy()
                    postData['phone_number'] = phone_number
                    errors = User.objects.validador_campos(postData)

                    if errors:
                        for key, value in errors.items():
                            messages.error(request, value)
                        # Preserve form data in session
                        request.session['registro_nombre'] = request.POST.get('name', '')
                        request.session['registro_apellido'] = request.POST.get('last_name', '')
                        request.session['registro_email'] = request.POST.get('email', '')
                        request.session['registro_phone'] = request.POST.get('phone_number', '')
                        request.session['registro_comuna'] = request.POST.get('comuna', '')
                        request.session['registro_genero'] = request.POST.get('gender', '')
                        request.session['registro_birthday'] = request.POST.get('birthday', '')
                        request.session['level_mensaje'] = 'alert-danger'
                        
                        # Pass session data as context variables
                        context = {
                            'name': request.session['registro_nombre'],
                            'last_name': request.session['registro_apellido'],
                            'email': request.session['registro_email'],
                            'phone_number': request.session['registro_phone'],
                            'comuna': request.session['registro_comuna'],
                            'birthday': request.session['registro_birthday'],
                            'gender': request.session['registro_genero'],
                            'user_form': user_form,
                            'orderdetail_form': orderdetail_form,
                            'order_form': order_form,
                            'producto': producto  
                        }
                        return render(request, 'core/producto.html', context)
                    
                    else:
                        # Clear session data
                        request.session['registro_nombre'] = ""
                        request.session['registro_apellido'] = ""
                        request.session['registro_email'] = ""
                        request.session['registro_phone'] = ""
                        request.session['registro_comuna'] = ""
                        request.session['registro_birthday'] = ""
                        request.session['registro_genero'] = ""
                        if password:
                                password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()   

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

                    
                        total = producto.price * quantity
                        order = Order.objects.create(
                            user=user,
                            total=total,

                        )
                        order.save()

                        order_detail = OrderDetail.objects.create(
                            order=order,
                            product=producto,
                            quantity=quantity,
                            unit_price=producto.price,
                            subtotal=total,
                        )
                        order_detail.save()

                        # send_mail(
                        #     'Pedido por confirmar',
                        #     f'Para completar tu registro, haz clic en el siguiente enlace:',
                        #     settings.DEFAULT_FROM_EMAIL,
                        #     [email],
                        #     fail_silently=False,
                        # )

                        request.session['level_mensaje'] = 'alert-success'
                        messages.success(request, 'Pedido enviado. En breve le llegará el correo de confirmación')
                        return redirect(reverse('catalogo') + '?OK')
            
        if request.method == 'GET':
            user_form = UserForm(prefix='')
            orderdetail_form = OrderDetailForm(prefix='order-detail')
            order_form = OrderForm(prefix='order')
            context = {
                'user_form': user_form,
                'orderdetail_form': orderdetail_form,
                'order_form': order_form,
                'producto': producto
            }
            return render(request, 'core/producto.html', context)
    except Product.DoesNotExist:
        return redirect(reverse('catalogo') + '?NO_EXIST')

def contacto(request):
    try:
        if request.method == 'POST':
            user_form = UserForm(request.POST, prefix='user')
            order_form = OrderForm(request.POST, prefix='order')
            orderdetail_form = OrderDetailForm(request.POST, prefix='order-detail')

            # Obtener datos del formulario POST
            name = request.POST.get('user-name')
            last_name = request.POST.get('user-last_name')
            birthday = request.POST.get('user-birthday')
            comuna = request.POST.get('user-comuna')
            gender = request.POST.get('user-gender')
            phone_number = request.POST.get('user-phone_number')
            email = request.POST.get('user-email')
            password = request.POST.get('user-password', '')

            # Comprueba si ya existe un usuario con el correo electrónico o el número de teléfono
            existing_user_email = User.objects.filter(email=email).first()
            existing_user_phone = User.objects.filter(phone_number=phone_number).first()

            if existing_user_email or existing_user_phone:
                existing_user = existing_user_email if existing_user_email else existing_user_phone

                if password:
                    if existing_user and not existing_user.password:
                        # Genera un token único para la verificación
                        verification_token = get_random_string(length=32)
                        
                        # Guarda el token con el registro del usuario
                        existing_user.verification_token = verification_token
                        existing_user.save()
                        
                        # Envía un correo electrónico con un enlace para completar el registro
                        verification_link = reverse('complete-registration', kwargs={'token': verification_token})
                        verification_url = request.build_absolute_uri(verification_link)
                        
                        send_mail(
                            'Completa tu registro en nuestro sitio',
                            f'Para completar tu registro, haz clic en el siguiente enlace: {verification_url}',
                            'noreply@tudominio.com',
                            [existing_user.email],
                            fail_silently=False,
                        )
                        request.session['level_mensaje'] = 'alert-warning'
                        messages.warning(request, "El correo o teléfono ya están registrados. Se ha enviado un correo para completar tu registro.")
                        return redirect(reverse('login'))
                else:
                    context = {
                        'user_form': user_form,
                        'order_form': order_form,
                        'orderdetail_form': orderdetail_form,
                    }
                    request.session['level_mensaje'] = 'alert-warning'
                    messages.warning(request, "El correo o teléfono ya están asociados a una cuenta. Inicie sesión, ingrese una contraseña para registrarse o corrija sus datos.")
                    return render(request, 'core/contacto.html', context)
            else:
                if user_form.is_valid():
                    name = user_form.cleaned_data.get('name')
                    last_name = user_form.cleaned_data.get('last_name')
                    birthday = user_form.cleaned_data.get('birthday')
                    comuna = user_form.cleaned_data.get('comuna')
                    gender = user_form.cleaned_data.get('gender')
                    phone_number = user_form.cleaned_data.get('formatted_phone_number')

                    email = user_form.cleaned_data.get('email')
                    password = user_form.cleaned_data.get('password', '')

                    if password:
                        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

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

                    order = Order.objects.create(
                        user=user,
                        total=0,  # Inicialmente en 0, se actualizará más tarde
                    )
                    order.save()

                    wishlist = request.POST.get('wishlist', '[]')
                    wishlist_products = json.loads(wishlist)

                    total = 0
                    for item in wishlist_products:
                        product = Product.objects.get(id=item['id'])
                        quantity = item['quantity']
                        subtotal = product.price * quantity
                        total += subtotal

                        OrderDetail.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            unit_price=product.price,
                            subtotal=subtotal,
                        )

                        order.total = total
                        order.save()

                    request.session['level_mensaje'] = 'alert-success'
                    messages.success(request, 'Solicitud enviada. En breve le llegará el correo de confirmación')
                    return redirect(reverse('contacto') + '?OK')
                else:
                    context = {
                        'user_form': user_form,
                        'order_form': order_form,
                        'orderdetail_form': orderdetail_form,
                    }
                    request.session['level_mensaje'] = 'alert-success'
                    messages.warning(request, 'ALGO NO FUNCIONA')
                    return render(request, 'core/contacto.html', context)
        else:
            user_form = UserForm(prefix='user')
            order_form = OrderForm(prefix='order')
            orderdetail_form = OrderDetailForm(prefix='order-detail')
            
        context = {
            'user_form': user_form,
            'order_form': order_form,
            'orderdetail_form': orderdetail_form,
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



