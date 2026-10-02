# Resultados descriptivos de entrenamiento

Estos archivos se regeneran al ejecutar la sección «Exploración y preparación» del [notebook](../notebooks/01-analisis-y-modelado.ipynb). Utilizan únicamente los 990 registros del entrenamiento del primer fold. Son resúmenes descriptivos, no resultados predictivos ni análisis de test.

| Archivo | Contenido |
|---|---|
| [resumen_categorias_entrenamiento.csv](resumen_categorias_entrenamiento.csv) | Frecuencias, rechazos y tasas de todas las categorías originales, incluidos contactos y ausencias. Un nivel vacío en el CSV representa ausencia. |
| [agrupaciones_categoricas.csv](agrupaciones_categoricas.csv) | Correspondencia entre niveles originales y grupos definidos por significado. |
| [resumen_agrupaciones_entrenamiento.csv](resumen_agrupaciones_entrenamiento.csv) | Frecuencias y tasas tras agrupar, incluida la ausencia explícita. |
| [imputacion_entrenamiento.csv](imputacion_entrenamiento.csv) | Ausencias antes y después del imputador y medianas aprendidas en este entrenamiento. |

La [justificación de las agrupaciones](../docs/Agrupaciones-categoricas.md) explica la información que se conserva y la que se simplifica. Las tasas de grupos pequeños tienen poco respaldo y no se utilizan para elegir las fusiones. Las imputaciones se volverán a aprender dentro de cada fold al evaluar modelos. Ningún archivo contiene identificadores individuales.
