# **Rental Car DriveX - Proyecto de Prácticas**

Guía de instalación y comandos para el proyecto "Rental Car DriveX".

## **Instalación del Ambiente**

### Requerimientos

- Python 3.10 o superior
- PostgreSQL

### Configuración de la Base de Datos
Antes de instalar las dependencias, asegúrate de crear la base de datos en PostgreSQL.
~~~sql
-- Desde una terminal psql Opción 1:
CREATE USER drivex_user WITH PASSWORD 'password'
CREATE DATABASE drivex_db OWNER drivex_user;
~~~

~~~sql 
-- Desde una terminal psql Opción 2:
CREATE DATABASE drivex_db;
CREATE USER drivex_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE drivex_db TO drivex_user;
GRANT USAGE, CREATE ON SCHEMA public TO drivex_user;
~~~
> **Nota:** Recuerda actualizar las credenciales en el archivo `ProyectoY/settings.py` para que coincidan con las que creaste.

### Ubuntu Linux / MacOS

Creación del ambiente virtual
~~~
python3 -m venv .venv
~~~
Activación del ambiente virtual
~~~
source .venv/bin/activate
~~~
Instalación de dependencias del proyecto
~~~
pip3 install -r requirements.txt
~~~

### Windows

Creación del ambiente virtual
~~~
py -m venv .venv
~~~
Activación del ambiente virtual (CMD)
~~~
.venv\Scripts\activate
~~~
Activación del ambiente virtual (PowerShell)
~~~
.venv\Scripts\activate.ps1
~~~
Instalación de dependencias del proyecto
~~~
pip install -r requirements.txt
~~~

---

## **Comandos Útiles de Django**

Todos los comandos se ejecutan desde la carpeta raíz del proyecto y con el entorno virtual activado.

### Iniciar Servidor de Desarrollo
#### Linux o MacOS
~~~
python3 manage.py runserver
~~~
#### Windows
~~~
py manage.py runserver
~~~
> Una vez iniciado, el sitio estará disponible en: http://127.0.0.1:8000

### Crear Archivos de Migración
Se ejecuta después de hacer cambios en los modelos (`models.py`).
#### Linux o MacOS
~~~
python3 manage.py makemigrations
~~~
#### Windows
~~~
py manage.py makemigrations
~~~

### Aplicar Migraciones a la Base de Datos
Aplica los cambios pendientes a la estructura de la base de datos.
#### Linux o MacOS
~~~
python3 manage.py migrate
~~~
#### Windows
~~~
py manage.py migrate
~~~

### Crear un Superusuario
Crea un usuario con acceso total al panel de administración de Django (`/admin`).
#### Linux o MacOS
~~~
python3 manage.py createsuperuser
~~~
#### Windows
~~~
py manage.py createsuperuser
~~~

---

## **Configuración Inicial del Proyecto**

Después de crear el superusuario, debes realizar estos pasos para que los permisos del sitio funcionen correctamente.

1.  Inicia el servidor y entra a `http://127.0.0.1:8000/admin`.
2.  Inicia sesión con tu superusuario.
3.  Ve a la sección **"Grupos"** y crea dos grupos con los siguientes nombres exactos:
    -   `Administradores`
    -   `Clientes`
4.  Ve a la sección **"Usuarios"**, selecciona tu superusuario y asígnalo al grupo `Administradores`.

---

## **Gestión de Dependencias**

### Actualizar `requirements.txt`
Después de instalar una nueva librería con `pip`, actualiza el archivo de requerimientos.
#### Linux o MacOS
~~~
pip3 freeze > requirements.txt
~~~
#### Windows
~~~
pip freeze > requirements.txt
~~~

### Desactivar el Entorno Virtual
Cuando termines de trabajar, puedes desactivar el entorno.
~~~
deactivate
~~~