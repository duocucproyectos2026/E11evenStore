🛒 E11even Store

Tienda de venta de videojuegos.

☛ Instalación

🛠 Clona el repositorio:

		📌 git clone https://github.com/Denissedz101/E11even-Store.git
		📌 cd e11even-store

🛠 Crea un entorno virtual e instálalo:

		📌 python -m venv env
		📌 # En Windows activalo -->  env\Scripts\activate
		
🛠 luego instala:
	
		📌 pip install oracledb 
		📌 pip install django
		📌 pip install djangorestframework django-widget-tweaks

👥 Datos conexion a la Base de datos

	➡️ Se uso un contenedor en Docker puerto 1521:1521
	
			'ENGINE': 'django.db.backends.oracle',
			'NAME': '127.0.0.1:1521/freepdb1',
			'USER': 'system',
			'PASSWORD': 'Oracle123'

	➡️ La base de datos se conecto a traves de Oracle sql developer.
	➡️ Recuerda modificar este acceso desde settings.py --> DATABASES

🛠 haz la migración > Desde la terminal vscode:

		📌 python manage.py makemigrations
		📌 python manage.py migrate

🔎 Ejecutamos el servidor local:

		📌 python manage.py runserver 8001
		📌 Abre tu navegador en http://127.0.0.1:8001/




