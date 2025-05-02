# Pildora PBI vs ST

Este repositorio contiene el código de python empleado en la Píldora **PowerBI VS StreamLit**, presentada por *Álvaro Puig Bieger* y *David Fdez. Suárez*.

## Comandos necesarios

### Instalación de paquetes

Se requiere tener pip y python instalados en el entorno local o en un entorno virtual como Conda.

Todos los paquetes usados en la app, pueden ser instalados con el siguiente comando:

> pip install -r requirements.txt

### Ejecución de la app

Si se lanza desde el entorno local, sin entornos virtuales:

> streamlit run app.py

Si se emplea un entorno virtual como Conda, dependiendo de la configuración de este, puede que Windows no sea capaz de encontrar la ruta del paquete de Stremlit instalado. En cuyo caso puede usarse el siguiente comando:

> python -m streamlit run app.py
