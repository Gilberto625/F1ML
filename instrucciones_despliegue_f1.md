# Instrucciones de despliegue en Render para el proyecto F1

Esta guía aplica lo visto en clase al proyecto basado en `Regresion_F1.ipynb`, donde el modelo predice `LapTime` usando Flask, `joblib`, GitHub y Render.

## 1. Archivos que deben existir antes de desplegar

En la raíz del proyecto deben estar estos archivos:

- `app.py`
- `exportar_modelo_f1.py`
- `f1_laptime_bundle.pkl`
- `requirements.txt`
- `Procfile`
- `templates/formulario.html`
- `.gitignore`

## 2. Paso previo obligatorio: generar el modelo

Antes de subir el proyecto a Render, debes generar el archivo del modelo:

```bash
python exportar_modelo_f1.py
```

Al terminar, debe existir:

```text
f1_laptime_bundle.pkl
```

Ese archivo debe subirse al repositorio, porque la app Flask lo carga directamente al arrancar.

## 3. Prueba local antes de GitHub

Verifica primero que la app funcione en local:

```bash
python app.py
```

Después abre:

```text
http://127.0.0.1:5000/
```

Debes comprobar lo siguiente:

- La página carga sin errores.
- El formulario se ve correctamente.
- Puedes capturar datos de F1.
- La predicción devuelve un `LapTime` estimado.

## 4. Preparar el repositorio Git

Si todavía no has inicializado Git:

```bash
git init
git add .
git commit -m "Proyecto F1 listo para despliegue en Render"
```

Si ya existe el repositorio, solo confirma que el archivo del modelo también esté incluido:

```bash
git status
```

Revisa especialmente que sí aparezcan:

- `app.py`
- `requirements.txt`
- `Procfile`
- `templates/formulario.html`
- `f1_laptime_bundle.pkl`

## 5. Subir el proyecto a GitHub

Conecta el proyecto con tu repositorio remoto:

```bash
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
```

Sube la rama principal. Puede ser `main` o `master`, según tu repositorio:

```bash
git push -u origin main
```

Si tu rama principal es `master`, entonces usa:

```bash
git push -u origin master
```

## 6. Crear el servicio en Render

1. Entra a `https://render.com`
2. Inicia sesión.
3. Haz clic en `New`.
4. Selecciona `Web Service`.
5. Elige `Build and deploy from a Git repository`.
6. Conecta tu cuenta de GitHub si todavía no está conectada.
7. Selecciona el repositorio de este proyecto.

## 7. Configuración exacta en Render

Cuando Render pida la configuración del servicio, usa estos valores:

- `Name`: un nombre para tu app, por ejemplo `f1-laptime-predictor`
- `Region`: la que prefieras o la más cercana
- `Branch`: `main` o `master`, según tu repo
- `Root Directory`: dejar vacío si el proyecto está en la raíz
- `Runtime`: `Python 3`
- `Build Command`: `pip install -r requirements.txt`
- `Start Command`: `gunicorn app:app`

Si Render detecta automáticamente el `Procfile`, está bien. Aun así, el `Start Command` correcto sigue siendo:

```bash
gunicorn app:app
```

## 8. Archivos usados por el despliegue

### `requirements.txt`

Debe contener al menos:

```txt
Flask==3.0.3
gunicorn==22.0.0
joblib==1.4.2
pandas==2.2.2
scikit-learn==1.5.0
numpy==1.26.4
```

### `Procfile`

Debe contener:

```text
web: gunicorn app:app
```

## 9. Primer despliegue

Después de crear el servicio:

1. Haz clic en `Create Web Service`.
2. Espera a que Render instale dependencias.
3. Espera a que termine el build.
4. Revisa los logs.

Si todo salió bien, Render te dará una URL pública similar a:

```text
https://tu-app.onrender.com
```

## 10. Verificación final en producción

Una vez desplegada la app, verifica:

- La URL pública abre correctamente.
- El formulario carga sin romperse.
- El archivo del modelo sí fue encontrado.
- La predicción responde desde `/predict`.
- El diseño sigue siendo responsivo en móvil y escritorio.

## 11. Errores comunes y cómo corregirlos

### Error 1: no encuentra `f1_laptime_bundle.pkl`

Causa:

- No generaste el archivo.
- No lo subiste a GitHub.
- El archivo no está en la raíz del proyecto.

Solución:

1. Ejecuta:

```bash
python exportar_modelo_f1.py
```

2. Verifica que exista `f1_laptime_bundle.pkl`.
3. Haz `git add .`, `git commit` y `git push`.

### Error 2: Render no inicia la app

Causa posible:

- `Start Command` incorrecto.
- `Procfile` incorrecto.
- `app.py` no está en la raíz.

Solución:

Usa exactamente:

```bash
gunicorn app:app
```

Y confirma que en `app.py` exista:

```python
app = Flask(__name__)
```

### Error 3: faltan dependencias

Causa:

- `requirements.txt` incompleto.

Solución:

Confirma que estén `Flask`, `gunicorn`, `joblib`, `pandas`, `scikit-learn` y `numpy`.

### Error 4: el formulario carga, pero la predicción falla

Causa posible:

- Campos vacíos.
- Valores numéricos inválidos.
- Problemas con el encoder para `Driver` y `Compound`.

Solución:

- Verifica que los datos enviados tengan formato correcto.
- Revisa los logs de Render.
- Confirma que el archivo `f1_laptime_bundle.pkl` fue generado con el mismo flujo del notebook.

## 12. Cómo actualizar la app después

Cada vez que cambies el modelo o el código:

1. Si cambió el entrenamiento, vuelve a generar el modelo:

```bash
python exportar_modelo_f1.py
```

2. Guarda cambios:

```bash
git add .
git commit -m "Actualizacion del modelo o de la app"
git push
```

3. Render hará un nuevo despliegue automático si el repositorio quedó conectado.

## 13. Resumen corto

El flujo correcto para este proyecto es:

1. Entrenar o validar el modelo en `Regresion_F1.ipynb`
2. Exportarlo con `python exportar_modelo_f1.py`
3. Probarlo localmente con `python app.py`
4. Subir todo a GitHub, incluyendo `f1_laptime_bundle.pkl`
5. Crear un `Web Service` en Render
6. Usar:

- `Build Command`: `pip install -r requirements.txt`
- `Start Command`: `gunicorn app:app`

Si esos pasos se cumplen, el despliegue queda alineado con lo visto en clase y aplicado correctamente a tu libreta de Jupyter.
