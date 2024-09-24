# Backend de Tareas en Python

## Descripción
Una aplicación simple para gestionar tareas utilizando Flask y SQLite.

## Características
- CRUD básico para tareas
- Serialización con Flask-Marshmallow
- Base de datos SQLite

## Tecnologías Usadas
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- Marshmallow-SQLAlchemy

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/jmiguelmangas/python-backend.git

2. Navega al directorio del proyecto:
    ```bash
    cd python-backend

3. Crea y activa un entorno virtual:
    ```bash
    python -m venv venv

    source venv/bin/activate  
    En Windows usa `venv\Scripts\activate`

4. Instala las dependencias:
    ```bash
    pip install -r requirements.txt

## Uso
Ejecuta la aplicación:
    ```bash
    python app.py

Accede a la API en http://127.0.0.1:5000/tasks

## Autenticación JWT

Este proyecto utiliza JSON Web Tokens (JWT) para la autenticación de usuarios. A continuación se describe cómo funciona la autenticación en la API:

### Cómo obtener un token

Para obtener un token, realiza una solicitud `POST` al endpoint `/login` con las credenciales del usuario:

- **URL**: `/login`
- **Método**: POST
- **Cuerpo de la solicitud**:
    ```json
    {
        "username": "tu_usuario",
        "password": "tu_contraseña"
    }
    ```
- **Respuesta**: 
    - Si las credenciales son válidas, recibirás un token en el siguiente formato:
      ```json
      {
          "access_token": "tu_token_aquí"
      }
      ```

### Usar el token

Para acceder a rutas protegidas, incluye el token en el encabezado `Authorization`:

- **Key**: `Authorization`
- **Value**: `Bearer tu_token_aquí`

## Configuración del Entorno

Para ejecutar la aplicación, necesitarás configurar la variable de entorno `SECRET_KEY`. 

1. Crea un archivo `.env` en la raíz del proyecto.
2. Añade la siguiente línea, reemplazando `tu_clave_secreta` por tu propia clave:

### Manejo de Errores

Se implementó un manejo de errores básico para la API. Cuando ocurren errores, la API devolverá un código de estado HTTP apropiado junto con un mensaje descriptivo.

Ejemplos de errores comunes:
- **404 Not Found**: Si la ruta no existe.
- **422 Unprocessable Entity**: Si los datos enviados en la solicitud no son válidos.

## Contribuciones
Si deseas contribuir al proyecto, por favor abre un pull request o contacta al autor.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.