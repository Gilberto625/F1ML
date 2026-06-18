# Despliegue del modelo de `Regresion_F1.ipynb`

Este proyecto aplica el flujo visto en clase, pero usando tu libreta de Jupyter como base.

## 1. Que hace cada archivo

- `exportar_modelo_f1.py`: reproduce el entrenamiento principal de la libreta y guarda `f1_laptime_bundle.pkl`.
- `app.py`: carga el modelo exportado y expone una app Flask con la ruta `/predict`.
- `templates/formulario.html`: formulario web para capturar variables y mostrar la prediccion.
- `requirements.txt`: dependencias para Render.
- `Procfile`: comando de arranque con Gunicorn.

## 2. Flujo recomendado

1. Ejecuta tu notebook y valida que el modelo sea el que quieres desplegar.
2. Genera el archivo del modelo:

```bash
python exportar_modelo_f1.py
```

3. Prueba localmente:

```bash
python app.py
```

4. Abre:

```text
http://127.0.0.1:5000/
```

5. Si funciona, sube estos archivos a GitHub y despliega en Render.

## 3. Variables que espera el formulario

- `Driver`
- `LapNumber`
- `Position`
- `Sector1Time`
- `Sector2Time`
- `Sector3Time`
- `MaxSpeed`
- `Compound`

## 4. Observacion importante

El modelo de tu notebook usa `OrdinalEncoder` para `Driver` y `Compound`. Por eso no basta con guardar solo el modelo; tambien hay que guardar el encoder. Eso ya queda resuelto en `f1_laptime_bundle.pkl`.

## 5. Despliegue en Render

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

## 6. Riesgo tecnico actual

El script `exportar_modelo_f1.py` descarga el CSV desde GitHub, igual que tu notebook. Para que el despliegue en Render no dependa de esa descarga, debes subir al repositorio el archivo generado `f1_laptime_bundle.pkl`.
