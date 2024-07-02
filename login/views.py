from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .models import *
from .forms import UserForm
import bcrypt
import json
from django.http import JsonResponse
import requests
import bcrypt


def signup(request):
    if request.method == 'GET':
        context = {
            'gender_choices': UserForm.GENERO_CHOICES,
            'comuna_choices': Comuna.objects.all(),
        }
        return render(request, 'login/signup.html', context)
    
    if request.method == 'POST':
        errors = User.objects.validador_campos(request.POST)

        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            
            # Preserve form data in session
            request.session['registro_nombre'] = request.POST.get('first_name', '')
            request.session['registro_apellido'] = request.POST.get('last_name', '')
            request.session['registro_email'] = request.POST.get('email', '')
            request.session['registro_phone'] = request.POST.get('phone_number', '')
            request.session['registro_comuna'] = request.POST.get('comuna', '')
            request.session['registro_genero'] = request.POST.get('gender', '')
            request.session['registro_birthday'] = request.POST.get('birthday', '')
            request.session['level_mensaje'] = 'alert-danger'
            
            # Pass session data as context variables
            context = {
                'first_name': request.session['registro_nombre'],
                'last_name': request.session['registro_apellido'],
                'email': request.session['registro_email'],
                'phone_number': request.session['registro_phone'],
                'comuna': request.session['registro_comuna'],
                'birthday': request.session['registro_birthday'],
                'gender': request.session['registro_genero'],
            }
            return render(request, 'login/signup.html', context)
        
        else:
            # Clear session data
            request.session['registro_nombre'] = ""
            request.session['registro_apellido'] = ""
            request.session['registro_email'] = ""
            request.session['registro_phone'] = ""
            request.session['registro_comuna'] = ""
            request.session['registro_birthday'] = ""
            request.session['registro_genero'] = ""
            
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            password = request.POST['password']
            comuna_id = request.POST['comuna']  # Assuming 'comuna' is passed as the ID of Comuna object
            birthday = request.POST['birthday']
            gender = request.POST['gender']
            
            # Check if user already exists with the same email or phone number
            existing_user_email = User.objects.filter(email=email).first()
            existing_user_phone = User.objects.filter(phone_number=phone_number).first()
            
            if existing_user_email or existing_user_phone:
                existing_user = existing_user_email if existing_user_email else existing_user_phone
                
                # If user exists but doesn't have a password set (password is None or empty)
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
                    
                    messages.warning(request, "El correo o teléfono ya están registrados. Se ha enviado un correo para completar tu registro.")
                    return redirect(reverse('login'))
                else:
                    messages.warning(request, "El correo o teléfono ya están registrados. Ingrese con su contraseña.")
            else:
                # Create a new user if not exists
                comuna = Comuna.objects.get(pk=comuna_id)
                password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                User.objects.create(
                    name=first_name,
                    last_name=last_name,
                    email=email,
                    birthday=birthday,
                    phone_number=phone_number,
                    password=password_hash,
                    comuna=comuna,
                    gender=gender
                )
                messages.success(request, "Usuario registrado con éxito!!!!")
        
        request.session['level_mensaje'] = 'alert-success'
        request.session['email_login'] = email
        return redirect(reverse('login'))
    
    return render(request, 'login/signup.html')
            
def complete_registration(request, token):
    try:
        user = User.objects.get(verification_token=token)
        
        if request.method == 'GET':
            return render(request, 'login/complete_registration.html', {'token': token})
        
        elif request.method == 'POST':
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            if password != password_confirm:
                messages.error(request, "Las contraseñas no coinciden.")
                return redirect(reverse('complete-registration', kwargs={'token': token}))
            
            # Hash and save the password
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user.password = password_hash
            user.verification_token = None  # Clear verification token after setting password
            user.save()
            
            messages.success(request, "Contraseña establecida correctamente. Ahora puedes iniciar sesión.")
            return redirect(reverse('login'))
    
    except User.DoesNotExist:
        messages.error(request, "El enlace de verificación no es válido.")
        return redirect(reverse('login'))

def login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
    else:
        if request.method == 'POST':
            email_login = request.POST['email_login']
            request.session['email_login'] = email_login  # Store email in session
            
            user = User.objects.filter(email=request.POST['email_login']) #Buscamos el correo ingresado en la BD             
            
            if user : #Si el usuario existe

                usuario_registrado = user[0]
                
                if bcrypt.checkpw(request.POST['password_login'].encode(), usuario_registrado.password.encode()): 
                    usuario = {
                        'id':usuario_registrado.id,
                        'first_name':usuario_registrado.name,
                        'last_name':usuario_registrado.last_name,
                        'email':usuario_registrado.email,
                        'rol':usuario_registrado.rol,
                    }

                    request.session['usuario'] = usuario
                    

                    if usuario_registrado.rol == 'ADMIN' :
                        messages.success(request,"Ingreso exitoso")
                        request.session['level_mensaje'] = 'alert-success'
                        return redirect(reverse('product-list') + '?SUCCESS')
                        
                    else:
                        messages.success(request,"Ingreso exitoso")
                        request.session['level_mensaje'] = 'alert-success'
                        return redirect(reverse('index') + '?SUCCESS')
                else:
                    messages.error(request,"Datos mal ingresados o el usuario no existe")
                    request.session['level_mensaje'] = 'alert-danger'
                    return redirect(reverse('login') + '?FAIL')
            else:
                messages.error(request,"Datos mal ingresados o el usuario no existe")
                request.session['level_mensaje'] = 'alert-danger'
                return redirect(reverse('login') + '?FAIL')
            
def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    
    return redirect('/')

def cargar_comunas_rm_desde_api(request):
    url_api_comunas = "https://gist.githubusercontent.com/juanbrujo/0fd2f4d126b3ce5a95a7dd1f28b3d8dd/raw/b8575eb82dce974fd2647f46819a7568278396bd/comunas-regiones.json"  # Reemplaza con la URL de la API de comunas
    response = requests.get(url_api_comunas)
    if response.status_code == 200:
        comunas_data = response.json()
        region_rm = next((region for region in comunas_data["regiones"] if region["region"] == "Región Metropolitana de Santiago"), None)
        if region_rm:
            for comuna in region_rm["comunas"]:
                nombre_comuna = comuna
                # Verifica si la comuna ya existe en la base de datos
                if not Comuna.objects.filter(comuna=nombre_comuna).exists():
                    comuna_obj = Comuna(comuna=nombre_comuna)
                    comuna_obj.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})