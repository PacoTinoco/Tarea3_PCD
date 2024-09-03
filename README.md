# Tarea3_PCD

# User Management API

## Descripción

Este proyecto es una API creada con **FastAPI** que permite gestionar usuarios. Proporciona cuatro endpoints para crear, actualizar, obtener y eliminar usuarios de una base de datos. La API utiliza **SQLite** como base de datos y **SQLAlchemy** para manejar las operaciones CRUD.

### Funcionalidades:

1. **Crear un usuario**: Permite crear un nuevo usuario en la base de datos. Si el email ya existe, se retorna un mensaje de error.
2. **Actualizar un usuario**: Permite actualizar la información de un usuario específico utilizando su `id`. Si el `id` no existe, se retorna un mensaje de error.
3. **Obtener información de un usuario**: Permite obtener la información de un usuario específico mediante su `id`. Si el `id` no existe, se retorna un mensaje de error.
4. **Eliminar un usuario**: Permite eliminar la información de un usuario específico mediante su `id`. Si el `id` no existe, se retorna un mensaje de error.

### Estructura del proyecto:

- **`main.py`**: Archivo principal que contiene la implementación de la API.
- **`requirements.txt`**: Archivo que contiene las dependencias necesarias para ejecutar el proyecto.

### Instalación y ejecución

1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_PROYECTO>
