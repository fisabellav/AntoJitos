# 🍪 **Antojitos** - Sitio Web para Galletas

**Antojitos** es un sitio web desarrollado para un negocio de galletas, realizado como proyecto final de mis estudios. Permite a los usuarios interactuar con el catálogo, gestionar una lista de deseos y recibir notificaciones por correo.

---

## 🧰 **Tecnologías**

- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Base de datos:** SQLite
- **API de correos:** [MailerSend](https://www.mailersend.com/)

---

## 🏠 **Funcionalidades**

### Página de Inicio
- Carrusel de productos con las últimas adiciones.
- Accesos rápidos a "Cookies" y "Catálogo".

### Catálogo
- Productos mostrados como tarjetas con detalles.
- Lista de deseos para añadir, modificar o eliminar productos.

### Filtros
- Filtros para mostrar galletas, pasteles, o productos por sabor (ej. nuez).

### Página de Cookies
- Solo galletas, filtradas por sabor (ej. chips).

### Sobre Nosotros
- Logo del negocio con accesos a secciones previas.

### Login y Registro
- Formulario de registro y validación de login con alertas en caso de error.

### Panel de Administración
- CRUD de productos con opciones para crear, editar y eliminar productos.

---

## 📬 **Envío de Correos**

- Usamos la API de **MailerSend** para enviar:
  - Confirmación de solicitudes.
  - Notificación de cambios de estado.
  - Recuperación de contraseñas con token.

---

## 🔐 **Seguridad**

- Validación de credenciales de login.
- Recuperación de contraseña con token enviado por correo.

---

## 📂 **Estructura del Proyecto**

```
/antojos
├── /static
│   ├── /css
│   ├── /images
│   └── /js
├── /templates
│   ├── about.html
│   ├── catalogo.html
│   └── index.html
├── /antojos
│   ├── /migrations
│   └── /models
├── manage.py
└── settings.py
```

