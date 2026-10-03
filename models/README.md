# Modelo final local

El notebook guarda `clasificador-solicitudes.joblib`: un diccionario con el pipeline completo de preparación y Random Forest, el umbral 0,5, la clase positiva 1 y la lista ordenada de columnas de entrada. El artefacto se genera al ejecutar el cierre y está excluido de Git. La [configuración de cierre](../reports/evaluacion_final.json) conserva parámetros, versiones y evaluación.

El modelo recibe los 16 atributos originales definidos en `columnas_entrada`, sin `Ind_ID`, `label` ni `Mobile_phone`. Las unidades y dominios se describen en el [diccionario](../docs/Diccionario-datos.md). Se admiten las ausencias tratadas en el proyecto; una columna requerida ausente debe corregirse. Las categorías no vistas se codifican sin activar ninguna categoría aprendida. Esto permite transformar entradas, pero no acredita fiabilidad ante datos fuera de distribución.

Desde la raíz del repositorio y con las [dependencias](../requirements.txt) instaladas:

```python
import joblib
import pandas as pd
from src.evaluacion import clasificar_puntuaciones

ficha = joblib.load("models/clasificador-solicitudes.joblib")
nuevos = pd.read_csv("nuevas_solicitudes.csv")
X_nuevos = nuevos.loc[:, ficha["columnas_entrada"]]
modelo = ficha["modelo"]
posicion = list(modelo.classes_).index(ficha["clase_positiva"])
puntuacion = modelo.predict_proba(X_nuevos)[:, posicion]
prediccion = clasificar_puntuaciones(puntuacion, ficha["umbral"])
resultado = nuevos.assign(Puntuacion_rechazo=puntuacion, Prediccion=prediccion)
```

`nuevas_solicitudes.csv` representa un archivo de entrada que debe aportar quien utilice el modelo; no se incluye como fuente real adicional. Las salidas son 0 = aprobación histórica y 1 = rechazo histórico; la puntuación no es una probabilidad de impago calibrada. No se recomienda conceder o denegar crédito automáticamente con este artefacto.

El módulo `src/preparacion.py` debe estar disponible al cargar: forma parte del pipeline. Cargar solo artefactos de confianza en un entorno compatible. La entrega es un análisis reproducible de portfolio, sin servicio en producción.
