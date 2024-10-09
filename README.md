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

## Pruebas

### Pruebas unitarias

Las pruebas unitarias validan el correcto funcionamiento de las funciones y rutas CRUD (Crear, Leer, Actualizar, Eliminar). A continuación te mostramos cómo se obtuvieron las pruebas unitarias utilizando un modelo de lenguaje.

#### Prompt usado para las pruebas unitarias:
```txt
Necesito que hagas todas las pruebas que puedas unitarias dentro de mi código. Dame el código completo funcional.
