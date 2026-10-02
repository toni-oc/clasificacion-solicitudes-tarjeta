# Resultados del análisis y la evaluación

Estos archivos se regeneran al ejecutar la sección «Exploración y preparación» del [notebook](../notebooks/01-analisis-y-modelado.ipynb). Utilizan únicamente los 990 registros del entrenamiento del primer fold. Son resúmenes descriptivos, no resultados predictivos ni análisis de test.

| Archivo | Contenido |
|---|---|
| [resumen_categorias_entrenamiento.csv](resumen_categorias_entrenamiento.csv) | Frecuencias, rechazos y tasas de todas las categorías originales, incluidos contactos y ausencias. Un nivel vacío en el CSV representa ausencia. |
| [agrupaciones_categoricas.csv](agrupaciones_categoricas.csv) | Correspondencia entre niveles originales y grupos definidos por significado. |
| [resumen_agrupaciones_entrenamiento.csv](resumen_agrupaciones_entrenamiento.csv) | Frecuencias y tasas tras agrupar, incluida la ausencia explícita. |
| [imputacion_entrenamiento.csv](imputacion_entrenamiento.csv) | Ausencias antes y después del imputador y medianas aprendidas en este entrenamiento. |

La [justificación de las agrupaciones](../docs/Agrupaciones-categoricas.md) explica la información que se conserva y la que se simplifica. Las tasas de grupos pequeños tienen poco respaldo y no se utilizan para elegir las fusiones. Las imputaciones se vuelven a aprender dentro de cada fold al evaluar modelos. Estos cuatro informes no contienen identificadores individuales.

## Comparación inicial de modelos

Los siguientes informes se regeneran en la sección «Comparación inicial de modelos». Utilizan los cinco folds de los **1.238 registros de desarrollo**, con umbral 0,5 y la preparación ajustada dentro de cada entrenamiento. No incluyen una evaluación de test.

| Archivo | Contenido |
|---|---|
| [modelos_iniciales_por_fold.csv](modelos_iniciales_por_fold.csv) | 25 ajustes: dos referencias y tres modelos, cada uno en cinco folds. Métricas de validación y F1 de entrenamiento. |
| [comparacion_inicial.csv](comparacion_inicial.csv) | Media no ponderada entre folds de cada métrica y desviación muestral del F1. La desviación no es un intervalo de confianza. |
| [errores_validacion_inicial.csv](errores_validacion_inicial.csv) | Recuentos agregados por candidato: TN, FP, FN y TP; clase positiva 1, rechazo registrado. |
| [configuracion_modelos_iniciales.json](configuracion_modelos_iniciales.json) | Parámetros de los estimadores, umbral, preparación y candidato provisional; sin reajuste final ni test evaluado. |

`predicciones_cv_inicial.csv` se conserva **solo en local**, excluido de Git: contiene identificador, candidato, fold, etiqueta registrada, puntuación y predicción. Cada registro aparece una vez por candidato. Las matrices se calculan con esas predicciones de validación; el F1 obtenido al agregarlas no sustituye al F1 medio por fold utilizado para comparar.

La precisión se muestra como 0 por convenio si no hay predicciones positivas; los recuentos permiten reconocer ese caso. Las puntuaciones no se presentan como probabilidades de impago ni como probabilidades calibradas. La elección provisional conserva una configuración, no un modelo final ni el mejor ajuste de un fold.
