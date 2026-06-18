# Análisis estricto de las diapositivas: “Despliegue del modelo de ML”

**Archivo analizado:** `07 Despliegue del modelo de ML.pptx`  
**Total de diapositivas:** 33  
**Autor mostrado en portada:** Dr. Efrén Juárez  
**Tema central:** despliegue de un modelo de Machine Learning usando Python, Flask, joblib, Gunicorn, Git/GitHub y Render.

**Nota técnica de edición:** este archivo conviene mantenerse en codificación UTF-8 para evitar errores de visualización como `AnÃ¡lisis` o `aplicaciÃ³n`.

---

## 1. Lectura general del material

Las diapositivas explican un flujo completo, aunque introductorio, para publicar una aplicación web que consume un modelo de aprendizaje automático. La ruta pedagógica es la siguiente:

1. Preparar un entorno virtual de Python.
2. Instalar dependencias para una app Flask.
3. Entender qué son Flask, Gunicorn y joblib.
4. Crear una app mínima tipo “Hola Mundo”.
5. Preparar un `Procfile` para despliegue.
6. Versionar el proyecto con Git.
7. Subir el código a GitHub.
8. Crear una cuenta y servicio web en Render.
9. Exportar el modelo entrenado a un archivo `.pkl`.
10. Crear una interfaz HTML para enviar datos al backend.
11. Crear un backend Flask que carga el modelo y responde predicciones.
12. Desplegar el clasificador en Render.

La intención del material es práctica: llevar al estudiante desde un modelo entrenado localmente hasta una aplicación web desplegada públicamente.

---

## 2. Análisis estricto del flujo técnico

### Flujo propuesto por las diapositivas

```text
Modelo entrenado
      ↓
Guardar modelo con joblib en archivo .pkl
      ↓
Crear backend Flask
      ↓
Crear formulario HTML en templates/formulario.html
      ↓
Crear endpoint /predict
      ↓
Instalar dependencias
      ↓
Crear requirements.txt
      ↓
Crear Procfile
      ↓
Inicializar Git
      ↓
Subir a GitHub
      ↓
Conectar repositorio con Render
      ↓
Configurar Build Command y Start Command
      ↓
Desplegar servicio web
```

### Evaluación estricta

El flujo es correcto a nivel conceptual, pero requiere varias precisiones para evitar errores reales durante el despliegue:

- Debe existir consistencia entre el nombre del archivo exportado del modelo y el nombre usado al cargarlo en Flask.
- En las diapositivas se guarda el modelo como `modelo_insectos.pkl`, pero después el código carga `model.pkl`. Esto puede romper la app si el archivo no coincide.
- El comando del `Procfile` aparece como `web:gunicorn app:app` en una diapositiva y como `web: gunicorn app:app` en otra. Ambas variantes suelen funcionar, pero conviene usar una sola forma por consistencia. La forma más legible es `web: gunicorn app:app`.
- El uso de `app.run(debug=True)` es aceptable para desarrollo local, pero no debe usarse como mecanismo de producción. En producción la app debe iniciarse con Gunicorn, ya sea desde el `Procfile` o desde el `Start Command` de Render.
- Se usa `git push -u origin master`, pero muchos repositorios modernos usan la rama `main`. El estudiante debe verificar el nombre real de su rama.
- El formulario y el backend trabajan con dos variables: `abdomen` y `antena`. El modelo debe haber sido entrenado con esas mismas columnas y en el mismo orden.
- Se muestra `pip freeze > requirements.txt`, pero si el entorno virtual contiene paquetes innecesarios, el archivo puede quedar inflado. Para clase funciona, pero para producción conviene limpiar dependencias.
- Se muestra un proyecto con `myenv/`; ese directorio debe ignorarse en Git y no debe subirse al repositorio.

---

## 3. Transcripción y análisis por diapositiva

---

## Diapositiva 1 — Portada

### Contenido

**Título:** Despliegue del modelo de ML  
**Autor:** Dr. Efrén Juárez

### Elementos visuales

La portada incluye un diagrama circular típico del ciclo de ciencia de datos / Machine Learning:

- Business Understanding
- Data Understanding
- Data Preparation
- Modeling
- Evaluation
- Deployment
- Data al centro

### Análisis estricto

La diapositiva contextualiza el tema dentro del ciclo completo de Machine Learning. El punto clave es que el despliegue no es una etapa aislada; aparece después de modelado y evaluación. El material se enfoca específicamente en la fase de **Deployment**.

---

## Diapositiva 2 — Creación y configuración de un entorno virtual en Python

### Contenido

**Título:** Creación y Configuración de un Entorno Virtual en Python

La diapositiva muestra un flujo visual con comandos:

```bash
pip install virtualenv
```

Crear entorno virtual llamado `myenv` usando una de estas opciones:

```bash
python -m venv myenv
```

```bash
virtualenv myenv
```

Activar el entorno virtual en Windows:

```bash
myenv\Scripts\activate
```

Instalar dependencias:

```bash
pip install Flask gunicorn
```

Crear `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Cerrar o desactivar el entorno virtual:

```bash
deactivate
```

### Análisis estricto

Esta diapositiva introduce correctamente la necesidad de aislar dependencias con un entorno virtual. El orden recomendado es:

1. Crear entorno.
2. Activarlo.
3. Instalar dependencias.
4. Crear `requirements.txt`.
5. Desactivar al finalizar.

### Observaciones críticas

- Hay un error tipográfico visible: aparece `nstalar Dependencias`, debería decir **Instalar Dependencias**.
- Solo se muestra activación para Windows. Sería conveniente incluir también:

```bash
source myenv/bin/activate
```

para Linux/macOS.

- En esta diapositiva se instala `Flask` y `gunicorn`, pero más adelante también se necesita `joblib`, `pandas` y `scikit-learn` para cargar y ejecutar el modelo.
- Si se usa `pip freeze`, el entorno debe estar limpio para no generar un `requirements.txt` lleno de paquetes innecesarios.

---

## Diapositiva 3 — ¿Qué es Flask?

### Contenido

Flask se define como un microframework de desarrollo web para Python, conocido por su simplicidad, flexibilidad y modularidad. Se explica que, a diferencia de frameworks más grandes, Flask proporciona una base mínima para construir aplicaciones web añadiendo solo los componentes necesarios.

### Análisis estricto

La definición es correcta. Para este proyecto, Flask funciona como el backend que:

- Muestra la página HTML.
- Recibe datos desde el formulario.
- Carga el modelo entrenado.
- Ejecuta la predicción.
- Devuelve una respuesta JSON al navegador.

### Punto clave

Flask no es el modelo de ML ni la plataforma de despliegue. Es la capa web que permite exponer el modelo como aplicación o API.

---

## Diapositiva 4 — Principales características de Flask

### Contenido

Características listadas:

- Ligero y minimalista.
- Modularidad.
- Rutas simples.
- Motor de plantillas Jinja2.
- Desarrollo rápido.
- Extensibilidad.

### Análisis estricto

La diapositiva justifica por qué Flask es adecuado para publicar un modelo de ML pequeño o mediano. Las características más importantes para el proyecto son:

- **Rutas simples:** permiten crear `/` y `/predict`.
- **Jinja2:** permite renderizar `formulario.html` desde la carpeta `templates`.
- **Extensibilidad:** permite integrar bibliotecas como `joblib`, `pandas` y `scikit-learn`.

---

## Diapositiva 5 — Gunicorn

### Contenido

Gunicorn se define como un servidor HTTP para aplicaciones Python basadas en WSGI. Se menciona que se usa para desplegar aplicaciones Flask, Django y otros frameworks.

También se indica que:

- Ejecuta aplicaciones Python en producción.
- Maneja múltiples solicitudes simultáneamente.
- Usa workers.
- Se integra con Flask y Django.
- Se ejecuta con un comando como:

```bash
gunicorn app:app
```

### Análisis estricto

La explicación es correcta. En este proyecto, Gunicorn sustituye al servidor de desarrollo de Flask cuando la app se despliega en Render.

### Punto técnico importante

En el comando:

```bash
gunicorn app:app
```

- El primer `app` se refiere al archivo `app.py`.
- El segundo `app` se refiere a la variable Flask creada dentro del archivo:

```python
app = Flask(__name__)
```

Si el archivo o la variable tienen otro nombre, el comando debe cambiar.

---

## Diapositiva 6 — joblib

### Contenido

joblib se define como una biblioteca de Python para serializar y deserializar objetos. Se menciona que es útil para guardar y cargar modelos de aprendizaje automático, datos y objetos grandes. También ofrece soporte para ejecución en paralelo.

### Análisis estricto

La diapositiva es pertinente porque un modelo de ML entrenado debe persistirse para poder reutilizarse en la app web.

En el proyecto, joblib cumple dos funciones:

1. Guardar el modelo entrenado:

```python
joblib.dump(model, 'model.pkl')
```

2. Cargar el modelo en Flask:

```python
model = joblib.load('model.pkl')
```

### Observación crítica

Los archivos `.pkl` no deben cargarse desde fuentes desconocidas, porque pueden ejecutar contenido malicioso al deserializarse. Solo debe cargarse un modelo generado y controlado por el propio desarrollador.

---

## Diapositiva 7 — Instalar Flask, joblib y gunicorn

### Contenido

```bash
pip install Flask joblib gunicorn
```

### Análisis estricto

El comando instala tres dependencias esenciales:

- `Flask`: backend web.
- `joblib`: guardar/cargar modelo.
- `gunicorn`: servidor de producción.

### Observación crítica

Para el clasificador mostrado después también se usan:

```python
import pandas as pd
```

por lo tanto, también debe instalarse:

```bash
pip install pandas scikit-learn
```

si el modelo fue entrenado con scikit-learn.

---

## Diapositiva 8 — “Hola Mundo” en Flask

### Contenido

La diapositiva muestra un ejemplo básico de Flask.

Código mostrado:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Hola, Mundo!"

if __name__ == '__main__':
    app.run(debug=True)
```

Ejecución:

```bash
python app.py
```

URL para probar:

```text
http://127.0.0.1:5000/
```

Salida esperada:

```text
¡Hola, Mundo!
```

### Análisis estricto

La diapositiva cumple su objetivo: demostrar una app Flask mínima.

### Observaciones críticas

- `debug=True` solo debe usarse en desarrollo local.
- La ruta `/` devuelve texto plano, no HTML.
- Este ejemplo sirve para validar que Flask funciona antes de conectar el modelo.

---

## Diapositiva 9 — ¿Qué es un Procfile?

### Contenido

Un `Procfile` se define como un archivo de texto usado en entornos de despliegue para indicar qué procesos deben ejecutarse. Se menciona Render y Heroku.

Formato general:

```text
<tipo_de_proceso>: <comando>
```

Ejemplo mostrado:

```text
web:gunicorn app:app
```

Comando para crearlo:

```bash
echo web:gunicorn app:app > Procfile
```

### Análisis estricto

El concepto es correcto: Render o Heroku necesitan saber cómo iniciar la app.

### Observación crítica

La forma más legible y consistente es:

```text
web: gunicorn app:app
```

con espacio después de `web:`.

El comando recomendado sería:

```bash
echo "web: gunicorn app:app" > Procfile
```

### Riesgo técnico

Si el archivo no se llama exactamente `Procfile` o está fuera de la raíz del proyecto, Render puede no detectarlo correctamente.

---

## Diapositiva 10 — Git

### Contenido visual

La diapositiva muestra únicamente el logotipo de Git.

### Análisis estricto

Funciona como transición hacia la sección de control de versiones. No aporta contenido técnico textual adicional.

---

## Diapositiva 11 — ¿Qué es Git?

### Contenido

Git se define como un sistema de control de versiones distribuido y de código abierto que permite gestionar y rastrear cambios en el código fuente. Se menciona que fue creado por Linus Torvalds en 2005.

### Análisis estricto

La definición es adecuada. Para este proyecto, Git es necesario porque Render toma el código desde un repositorio, normalmente GitHub.

### Punto clave

Sin Git y GitHub, el flujo mostrado para desplegar en Render no puede completarse como está diseñado.

---

## Diapositiva 12 — Instalación de Git

### Contenido

Se indica instalar Git desde:

```text
https://git-scm.com/
```

Luego seguir las instrucciones del instalador según el sistema operativo.

### Análisis estricto

La instrucción es correcta pero básica. Faltaría mencionar que después de instalar Git conviene verificarlo con:

```bash
git --version
```

---

## Diapositiva 13 — Configuración inicial de Git

### Contenido

Configurar correo:

```bash
git config --global user.email "you@example.com"
```

Configurar nombre:

```bash
git config --global user.name "Your Name"
```

Verificar correo:

```bash
git config --global user.email
```

Verificar nombre:

```bash
git config --global user.name
```

### Análisis estricto

La configuración es correcta. Estos datos se usarán para identificar los commits.

### Observación crítica

El correo idealmente debe coincidir con el correo usado en GitHub, o con un correo verificado en la cuenta de GitHub.

---

## Diapositiva 14 — Crear un archivo .gitignore

### Contenido

Archivo mostrado:

```gitignore
# Ignore virtual environment
myenv/

# Ignore Python cache files
__pycache__/
*.pyc
*.pyo

# Ignore MacOS specific file
.DS_Store

# Ignore environment variables files
.env
.venv
```

### Análisis estricto

El `.gitignore` es correcto para evitar subir archivos innecesarios o sensibles.

### Observaciones críticas

- Es correcto ignorar `myenv/` porque el entorno virtual no debe subirse.
- Es correcto ignorar `.env` porque puede contener secretos.
- No se debe ignorar `requirements.txt`, `app.py`, `templates/`, `Procfile` ni el modelo si se despliega directamente con el repositorio.
- Si el modelo `.pkl` es demasiado pesado, convendría no subirlo a GitHub y usar otro almacenamiento, pero en un proyecto escolar pequeño puede incluirse.

---

## Diapositiva 15 — Inicializar el repositorio Git

### Contenido

La diapositiva indica:

```text
Navega a la carpeta de tu proyecto y ejecuta:
```

```bash
git init
```

### Análisis estricto

El comando es correcto. Debe ejecutarse en la raíz del proyecto, donde estarán archivos como:

```text
app.py
requirements.txt
Procfile
templates/
model.pkl
.gitignore
```

### Observación crítica

Si se ejecuta `git init` dentro de una carpeta equivocada, puede inicializarse un repositorio incompleto o con archivos mal ubicados.

---

## Diapositiva 16 — Añade el archivo .gitignore al repositorio

### Contenido

Comandos mostrados:

```bash
git add .gitignore
```

```bash
git commit -m "Add .gitignore file"
```

### Análisis estricto

La intención es correcta: agregar primero el `.gitignore` para evitar que el entorno virtual y archivos temporales sean incluidos después.

### Observación crítica

Si el entorno virtual ya fue agregado a Git antes de crear `.gitignore`, no basta con ignorarlo; habría que removerlo del índice con:

```bash
git rm -r --cached myenv/
```

---

## Diapositiva 17 — Añadir los archivos restantes

### Contenido

Comandos mostrados:

```bash
git add .
```

```bash
git commit -m "Initial commit"
```

### Análisis estricto

El comando `git add .` agrega todos los archivos no ignorados del proyecto.

### Observación crítica

Antes de ejecutar el commit, debe verificarse que no se va a subir información sensible:

```bash
git status
```

También conviene revisar que sí estén incluidos:

- `app.py`
- `templates/formulario.html`
- `requirements.txt`
- `Procfile`
- `model.pkl` o el archivo `.pkl` usado por la app

---

## Diapositiva 18 — Verificación del repositorio Git

### Contenido

Verificar estado:

```bash
git status
```

Verificar historial de commits:

```bash
git log --name-status
```

### Análisis estricto

La diapositiva es correcta. `git status` permite confirmar si hay archivos pendientes. `git log --name-status` permite revisar historial y archivos modificados por commit.

---

## Diapositiva 19 — Crear un repositorio en GitHub

### Contenido

Se muestra el enlace:

```text
https://github.com/juarezefren/flask3.git
```

También se muestran capturas de GitHub donde se crea un repositorio y se obtiene la URL del repositorio remoto.

### Análisis estricto

La diapositiva enseña el paso de crear un repositorio remoto. Es necesario para conectar Render con GitHub.

### Observaciones críticas

- El enlace mostrado parece ser un ejemplo del docente; cada estudiante debe usar su propio usuario y repositorio.
- Se debe evitar subir credenciales, archivos `.env` o claves privadas.

---

## Diapositiva 20 — Conectar el repositorio local con GitHub

### Contenido

```bash
git remote add origin https://github.com/<USERNAME>/<REPOSITORY>.git
```

```bash
git push -u origin master
```

### Análisis estricto

La instrucción conecta el repositorio local con GitHub y sube los commits.

### Observación crítica

Si la rama principal se llama `main`, el comando correcto sería:

```bash
git push -u origin main
```

También puede ser necesario revisar la rama actual:

```bash
git branch
```

---

## Diapositiva 21 — Portada de sección: Render

### Contenido

**Título:** Render  
**Autor:** Dr. Efrén Juárez

### Análisis estricto

Marca el inicio de la sección de despliegue en la nube.

---

## Diapositiva 22 — ¿Qué es Render?

### Contenido

Render se define como una plataforma de alojamiento en la nube que facilita el despliegue de aplicaciones web, APIs y otros servicios. Se indica que permite centrarse en escribir código en lugar de gestionar infraestructura.

### Análisis estricto

La descripción es adecuada para el nivel del material. En este proyecto, Render aloja la aplicación Flask y ejecuta Gunicorn como servidor de producción.

---

## Diapositiva 23 — Características de Render

### Contenido

Características listadas:

- Despliegue automático: integración con GitHub y GitLab para despliegues automáticos.
- Escalabilidad: entornos ajustables automáticamente según la carga.
- SSL automático: certificados SSL sin configuración manual.
- Bases de datos gestionadas: servicios como PostgreSQL y Redis.
- Soporte multilenguaje: compatible con Flask, Node.js, Ruby on Rails, Django y más.

### Análisis estricto

La diapositiva resume ventajas de Render. Para este proyecto son especialmente relevantes:

- Integración con GitHub.
- Despliegue automático al hacer push.
- SSL automático.
- Soporte para Flask mediante Gunicorn.

### Observación crítica

En servicios gratuitos, Render puede suspender el servicio por inactividad. La propia captura posterior muestra una advertencia sobre posible lentitud al reactivar.

---

## Diapositiva 24 — Crear cuenta en Render

### Contenido

Título con URL:

```text
Crear cuenta en Render
https://render.com
```

La captura muestra la pantalla de registro de Render con opciones de creación de cuenta usando:

- GitHub
- GitLab
- Bitbucket
- Google
- Email y password

### Análisis estricto

Para el flujo de las diapositivas, la opción más conveniente es crear o entrar con GitHub, porque después se conectará un repositorio.

---

## Diapositiva 25 — Crear un nuevo servicio web

### Contenido visual

La diapositiva muestra capturas de Render:

1. Menú **New** con opciones como:
   - Static Site
   - Web Service
   - Private Service
   - Background Worker
   - Cron Job
   - PostgreSQL
   - Redis
   - Blueprint

2. Pantalla **Create a new Web Service**, con opciones para:
   - Build and deploy from a Git repository.
   - Deploy an existing image from a registry.

### Análisis estricto

Para este proyecto debe elegirse **Web Service** y luego **Build and deploy from a Git repository**.

### Observación crítica

No debe elegirse **Static Site**, porque una app Flask necesita ejecutar backend Python.

---

## Diapositiva 26 — Conectar a un repositorio de GitHub

### Contenido visual

La captura muestra:

- Pantalla para conectar un repositorio.
- Botón **Connect Repository**.
- Pantalla de instalación/autorización de Render en GitHub.
- Opciones como permitir acceso a todos los repositorios o solo a repositorios seleccionados.

### Análisis estricto

Este paso autoriza a Render para leer el repositorio de GitHub. Es necesario para que Render pueda desplegar automáticamente el código.

### Observación crítica

Por seguridad, es preferible seleccionar solo el repositorio necesario en lugar de dar acceso a todos los repositorios.

---

## Diapositiva 27 — Finalizando la configuración

### Contenido visual

La diapositiva muestra la configuración final de un servicio web en Render. Se observan campos como:

- Nombre del servicio.
- Región.
- Rama del repositorio.
- Root Directory.
- Runtime: Python 3.
- Build Command.
- Start Command.
- Instance Type.
- Variables de entorno.
- Botón para crear el servicio web.

Comandos visibles o inferidos por la captura:

```bash
pip install -r requirements.txt
```

```bash
gunicorn app:app
```

### Análisis estricto

Esta es una de las diapositivas más importantes para que el despliegue funcione.

### Configuración esperada

- **Runtime:** Python 3
- **Build Command:**

```bash
pip install -r requirements.txt
```

- **Start Command:**

```bash
gunicorn app:app
```

- **Branch:** `master` o `main`, según el repositorio real.
- **Root Directory:** vacío si `app.py`, `requirements.txt` y `Procfile` están en la raíz.

### Observación crítica

Si el proyecto está dentro de una subcarpeta, se debe configurar correctamente el **Root Directory**.

---

## Diapositiva 28 — Servicio web desplegado

### Contenido visual

La diapositiva muestra un servicio desplegado en Render con logs de ejecución. Se observa una URL pública del servicio, botones como **Connect** y **Manual Deploy**, y mensajes de log donde Gunicorn inicia correctamente.

Mensajes técnicos visibles en los logs:

- Build successful.
- Deploying.
- Using Node version 20.12.2.
- Running `gunicorn app:app`.
- Starting gunicorn.
- Listening at `http://0.0.0.0:10000`.

### Análisis estricto

La captura demuestra que el servicio fue desplegado correctamente y que Render está ejecutando Gunicorn.

### Observación crítica

Aunque los logs muestren que Gunicorn inició, todavía debe probarse la URL pública y el formulario de predicción para asegurar que:

- El modelo `.pkl` existe.
- Las dependencias están instaladas.
- El endpoint `/predict` responde.
- El formulario envía correctamente los datos.

---

## Diapositiva 29 — Exportar el modelo entrenado

### Contenido

Se indica que, una vez que el modelo está entrenado, se guarda en un archivo usando joblib.

Código mostrado:

```python
import joblib

# Suponiendo que tu modelo entrenado está en una variable llamada `model`
joblib.dump(model, 'modelo_insectos.pkl')
```

### Análisis estricto

La idea es correcta. El modelo entrenado debe guardarse para poder cargarlo desde la app Flask.

### Observación crítica importante

Aquí el archivo se llama:

```text
modelo_insectos.pkl
```

pero más adelante el backend carga:

```python
model = joblib.load('model.pkl')
```

Esto es inconsistente. Para evitar error, se debe usar el mismo nombre en ambos lugares. Por ejemplo:

```python
joblib.dump(model, 'model.pkl')
```

Y luego:

```python
model = joblib.load('model.pkl')
```

O, si se conserva el nombre en español:

```python
model = joblib.load('modelo_insectos.pkl')
```

---

## Diapositiva 30 — ¿Qué es un archivo .pkl?

### Contenido

Un archivo `.pkl` se define como un archivo que contiene un objeto serializado en Python. Se explica que “pickle” proviene de la biblioteca estándar `pickle`, usada para serializar y deserializar objetos. También se indica que joblib usa un formato similar optimizado para objetos grandes, como matrices y modelos de aprendizaje automático.

### Análisis estricto

La explicación es adecuada. En este proyecto, el `.pkl` contiene el modelo entrenado.

### Observación crítica

Un `.pkl` no es un archivo universal ni seguro por defecto. Depende de Python y de las versiones de bibliotecas usadas al guardar/cargar. Es recomendable mantener consistentes las versiones de `scikit-learn`, `numpy`, `pandas` y `joblib` entre entrenamiento y despliegue.

---

## Diapositiva 31 — Publicar clasificador de insectos: frontend HTML

### Contenido visual

La diapositiva muestra código de `formulario.html` para un clasificador de insectos.

Código reconstruido del contenido mostrado:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Clasificador de Insectos</title>
    <script>
        function clasificarInsecto(event) {
            event.preventDefault();
            const abdomen = document.getElementById('abdomen').value;
            const antena = document.getElementById('antena').value;

            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `abdomen=${abdomen}&antena=${antena}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('resultado').innerText = 'Error: ' + data.error;
                } else {
                    document.getElementById('resultado').innerText = 'El insecto es un/a ' + data.categoria;
                }
            })
            .catch(error => {
                document.getElementById('resultado').innerText = 'Error en la solicitud.';
                console.error('Error:', error);
            });
        }
    </script>
</head>
<body>
    <h1>Clasificador de Insectos</h1>
    <form id="formulario" onsubmit="clasificarInsecto(event)">
        <label for="abdomen">Longitud del Abdomen:</label>
        <input type="text" id="abdomen" name="abdomen"><br><br>

        <label for="antena">Longitud de las Antenas:</label>
        <input type="text" id="antena" name="antena"><br><br>

        <input type="submit" value="Enviar">
    </form>
    <p id="resultado"></p>
</body>
</html>
```

### Análisis estricto

El frontend es funcional y simple. Toma dos valores del usuario:

- Longitud del abdomen.
- Longitud de las antenas.

Luego envía una petición `POST` al endpoint `/predict`.

### Observaciones críticas

- Los inputs deberían ser de tipo `number`, no `text`, para reducir errores:

```html
<input type="number" step="any" id="abdomen" name="abdomen" required>
```

- El cuerpo de la petición no codifica los valores. Una forma más segura sería usar `URLSearchParams`.
- No hay validación visual para campos vacíos o valores no numéricos.
- El diseño es muy básico; funcionalmente sirve para la clase.

---

## Diapositiva 32 — Publicar clasificador de insectos: backend Flask

### Contenido visual

La diapositiva muestra el archivo `app.py`.

Código reconstruido del contenido mostrado:

```python
from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
import logging

app = Flask(__name__)

# Configurar el registro
logging.basicConfig(level=logging.DEBUG)

# Cargar el modelo entrenado
model = joblib.load('model.pkl')
app.logger.debug('Modelo cargado correctamente.')

@app.route('/')
def home():
    return render_template('formulario.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener los datos enviados en el request
        abdomen = float(request.form['abdomen'])
        antena = float(request.form['antena'])

        # Crear un DataFrame con los datos
        data_df = pd.DataFrame([[abdomen, antena]], columns=['abdomen', 'antena'])
        app.logger.debug(f'DataFrame creado: {data_df}')

        # Realizar predicciones
        prediction = model.predict(data_df)
        app.logger.debug(f'Predicción: {prediction[0]}')

        # Devolver las predicciones como respuesta JSON
        return jsonify({'categoria': prediction[0]})

    except Exception as e:
        app.logger.error(f'Error en la predicción: {str(e)}')
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

### Análisis estricto

El backend es coherente con el frontend:

- La ruta `/` renderiza `formulario.html`.
- La ruta `/predict` recibe los datos del formulario.
- Convierte los valores a `float`.
- Crea un `DataFrame` con columnas `abdomen` y `antena`.
- Ejecuta `model.predict(data_df)`.
- Devuelve la categoría predicha en JSON.

### Observaciones críticas

- El archivo cargado es `model.pkl`, pero la diapositiva 29 guardaba `modelo_insectos.pkl`. Debe corregirse.
- `app.run(debug=True)` no debe usarse en producción.
- Si el modelo fue entrenado con columnas en otro orden o con otros nombres, la predicción puede ser incorrecta.
- Si el modelo devuelve tipos de NumPy no serializables, podría requerirse convertir la predicción a `str`:

```python
return jsonify({'categoria': str(prediction[0])})
```

- El `except Exception` captura todo. Para clase está bien, pero en producción se deberían manejar errores específicos.
- El modelo se carga al iniciar la app. Esto es correcto para no cargarlo en cada solicitud.

---

## Diapositiva 33 — Publicar clasificador de insectos: estructura, requirements y Procfile

### Contenido visual

La diapositiva muestra:

1. Una app desplegada con el título **Clasificador de Insectos**.
2. Formulario con:
   - Longitud del Abdomen: `5`
   - Longitud de las Antenas: `7`
   - Botón `Enviar`
   - Resultado: `El insecto es una chicharra`
3. Estructura de archivos del proyecto.
4. Archivo `requirements.txt`.
5. Archivo `Procfile`.

### Estructura de archivos mostrada

```text
myenv/
templates/
  formulario.html
.gitignore
app.py
model.pkl
Procfile
requirements.txt
```

### requirements.txt mostrado

```txt
blinker==1.8.2
click==8.1.7
colorama==0.4.6
Flask==3.0.3
gunicorn==22.0.0
itsdangerous==2.2.0
Jinja2==3.1.4
joblib==1.4.2
logging==0.4.9.6
MarkupSafe==2.1.5
numpy==1.26.4
packaging==24.0
pandas==2.2.2
python-dateutil==2.9.0.post0
pytz==2024.1
scikit-learn==1.5.0
scipy==1.13.1
six==1.16.0
threadpoolctl==3.5.0
tzdata==2024.1
Werkzeug==3.0.3
```

### Procfile mostrado

```text
web: gunicorn app:app
```

### Análisis estricto

Esta diapositiva resume el estado final del proyecto. Muestra que el clasificador ya está publicado y que el formulario devuelve una clasificación.

### Observaciones críticas

- `myenv/` aparece en la estructura, pero no debe subirse a GitHub.
- `model.pkl` sí aparece, lo cual coincide con el código de la diapositiva 32, pero no coincide con el nombre `modelo_insectos.pkl` usado en la diapositiva 29.
- `requirements.txt` incluye `logging==0.4.9.6`. Esto merece revisión porque `logging` forma parte de la biblioteca estándar de Python. Si aparece en `pip freeze`, conviene verificar si se instaló un paquete externo innecesario o si el entorno virtual no estaba lo suficientemente limpio.
- El `Procfile` de esta diapositiva usa la forma más correcta:

```text
web: gunicorn app:app
```

- El resultado “chicharra” demuestra que el flujo formulario → backend → modelo → respuesta funciona.

---

## 4. Lista consolidada de comandos que aparecen en las diapositivas

### Entorno virtual

```bash
pip install virtualenv
python -m venv myenv
virtualenv myenv
myenv\Scripts\activate
pip install Flask gunicorn
pip freeze > requirements.txt
deactivate
```

### Instalación de dependencias principales

```bash
pip install Flask joblib gunicorn
```

### Ejecutar app local

```bash
python app.py
```

### Crear Procfile

```bash
echo "web: gunicorn app:app" > Procfile
```

### Configurar Git

```bash
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
git config --global user.email
git config --global user.name
```

### Inicializar y guardar cambios

```bash
git init
git add .gitignore
git commit -m "Add .gitignore file"
git add .
git commit -m "Initial commit"
git status
git log --name-status
```

### Conectar con GitHub

```bash
git remote add origin https://github.com/<USERNAME>/<REPOSITORY>.git
git push -u origin master
```

Versión alternativa si la rama es `main`:

```bash
git push -u origin main
```

### Exportar modelo

```python
import joblib
joblib.dump(model, 'modelo_insectos.pkl')
```

Versión consistente con el backend mostrado:

```python
import joblib
joblib.dump(model, 'model.pkl')
```

### Cargar modelo en Flask

```python
model = joblib.load('model.pkl')
```

### Render

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
gunicorn app:app
```

---

## 5. Estructura final recomendada del proyecto

```text
proyecto_clasificador/
├── app.py
├── model.pkl
├── Procfile
├── requirements.txt
├── .gitignore
└── templates/
    └── formulario.html
```

### No subir a GitHub

```text
myenv/
__pycache__/
*.pyc
.env
.venv/
```

---

## 6. Versión corregida del Procfile

```text
web: gunicorn app:app
```

---

## 7. Versión corregida mínima de requirements.txt

Una versión más limpia, alineada con el código mostrado, podría ser:

```txt
Flask==3.0.3
gunicorn==22.0.0
joblib==1.4.2
pandas==2.2.2
scikit-learn==1.5.0
numpy==1.26.4
```

Dependiendo del ambiente, `scipy`, `Jinja2`, `Werkzeug`, `click`, `itsdangerous` y `MarkupSafe` se instalarán como dependencias transitivas. Sin embargo, si se usa `pip freeze`, aparecerán explícitamente.

---

## 8. Errores, riesgos e inconsistencias detectadas

### 1. Inconsistencia en el nombre del modelo

En la exportación:

```python
joblib.dump(model, 'modelo_insectos.pkl')
```

En el backend:

```python
model = joblib.load('model.pkl')
```

Debe usarse un solo nombre.

### 2. Procfile inconsistente

Aparece:

```text
web:gunicorn app:app
```

y después:

```text
web: gunicorn app:app
```

Recomendado:

```text
web: gunicorn app:app
```

### 3. Posible problema con rama `master`

Se usa:

```bash
git push -u origin master
```

pero muchos repositorios usan:

```bash
git push -u origin main
```

### 4. Dependencia `logging`

El `requirements.txt` mostrado incluye:

```txt
logging==0.4.9.6
```

Esto puede ser problemático porque `logging` es parte de la biblioteca estándar de Python.

### 5. Uso de `debug=True`

Aparece en ejemplos:

```python
app.run(debug=True)
```

Correcto para desarrollo local, incorrecto como práctica de producción.

### 6. Validación débil en el formulario

Los campos se muestran como `text`, pero deberían ser numéricos.

### 7. Seguridad de `.pkl`

Cargar archivos pickle de fuentes desconocidas es riesgoso. Solo debe usarse el modelo propio.

### 8. Falta explicar versión de Python

Render permite seleccionar o inferir versión de Python. Para evitar conflictos, convendría usar un archivo como `runtime.txt` o especificar la versión según la plataforma.

### 9. Falta una prueba local completa antes de Render

El material muestra “Hola Mundo” y luego despliegue, pero convendría añadir una prueba local del clasificador completo antes de subir a GitHub.

### 10. Legibilidad de código en capturas

Las diapositivas 31 y 32 usan capturas de código. Para estudiar, conviene tener el código como texto copiable.

---

## 9. Checklist final para que el proyecto funcione

Antes de subir a GitHub:

- [ ] El entorno virtual está creado y activado.
- [ ] Las dependencias están instaladas.
- [ ] El modelo está guardado como `model.pkl` o el nombre elegido.
- [ ] `app.py` carga exactamente ese mismo archivo `.pkl`.
- [ ] Existe `templates/formulario.html`.
- [ ] Existe `requirements.txt`.
- [ ] Existe `Procfile`.
- [ ] `.gitignore` ignora `myenv/`, `.env` y `__pycache__/`.
- [ ] `myenv/` no fue subido al repositorio.
- [ ] La app funciona localmente con `python app.py`.
- [ ] La ruta `/` muestra el formulario.
- [ ] La ruta `/predict` responde JSON.
- [ ] El repositorio está en GitHub.
- [ ] Render está conectado al repositorio correcto.
- [ ] Render usa el build command correcto.
- [ ] Render usa el start command correcto.
- [ ] La URL pública carga el formulario.
- [ ] La predicción funciona en producción.

---

## 10. Conclusión estricta

El material enseña correctamente la idea general de desplegar un modelo de Machine Learning con Flask y Render. La secuencia es útil y práctica para estudiantes que están aprendiendo a publicar un modelo entrenado.

Sin embargo, para que el proyecto sea sólido, deben corregirse principalmente estos puntos:

1. Unificar el nombre del modelo `.pkl`.
2. Mantener consistente el arranque con Gunicorn, por ejemplo `web: gunicorn app:app` en `Procfile`.
3. Verificar si la rama de Git es `main` o `master`.
4. No subir el entorno virtual.
5. Revisar dependencias innecesarias o sospechosas como `logging==0.4.9.6`.
6. No usar `debug=True` como práctica de producción.
7. Validar mejor los datos del formulario.
8. Probar la app completa localmente antes del despliegue.

La presentación es funcional como guía introductoria, pero requiere estas correcciones para evitar fallos comunes al desplegar en Render.
