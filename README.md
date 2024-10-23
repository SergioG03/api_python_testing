# API de Guepardos - Flask REST API

Este proyecto es una API REST construida con Flask que permite gestionar información sobre guepardos. Incluye todas las operaciones CRUD (crear, leer, actualizar y eliminar) con almacenamiento en una base de datos SQLite utilizando SQLAlchemy.

Además, se han implementado múltiples tipos de pruebas, tales como unitarias, de integración, funcionales, de seguridad y de rendimiento, para garantizar la calidad del código.

## Características principales

- CRUD (Crear, Leer, Actualizar, Eliminar) para gestionar guepardos.
- Uso de SQLite como base de datos.
- Pruebas automáticas de distintos tipos para asegurar el correcto funcionamiento.
- Implementación de buenas prácticas de seguridad y rendimiento.

### Rutas API

- `POST /guepardos`: Crear un nuevo guepardo.
- `GET /guepardos`: Obtener todos los guepardos.
- `GET /guepardos/<int:id>`: Obtener un guepardo por su ID.
- `PUT /guepardos/<int:id>`: Actualizar un guepardo por su ID.
- `DELETE /guepardos/<int:id>`: Eliminar un guepardo por su ID.

## Instalación

1. Clona este repositorio:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

3. Ejecuta la aplicación:
    ```bash
    python app.py
    ```

La aplicación estará disponible en `http://127.0.0.1:5000`.

## Apuntes sobre PROJEN y POETRY

Versiones de Node.js y Python: La instalación de Projen requirió una versión compatible de Node.js, y el uso de python en lugar de python3 causó errores debido a la configuración del sistema.
Entorno Virtual: La creación y activación del entorno virtual fueron cruciales, pero requirieron verificar la existencia del archivo activate y asegurarse de que el path estuviera correcto.
Dependencias y Paquetes: La instalación de pip en el entorno virtual fue necesaria para evitar errores durante la configuración de Projen.


