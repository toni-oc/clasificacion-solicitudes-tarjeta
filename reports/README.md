# Resultados del análisis y la evaluación

Los cuatro informes de la tabla siguiente se regeneran al ejecutar la sección «Exploración y preparación» del [notebook](../notebooks/clasificacion-solicitudes-tarjeta.ipynb). Utilizan únicamente los 990 registros del entrenamiento del primer fold. Son resúmenes descriptivos, no resultados predictivos ni análisis de test.

| Archivo | Contenido |
|---|---|
| [resumen_categorias_entrenamiento.csv](resumen_categorias_entrenamiento.csv) | Frecuencias, rechazos y tasas de todas las categorías originales, incluidos contactos y ausencias. Un nivel vacío en el CSV representa ausencia. |
| [agrupaciones_categoricas.csv](agrupaciones_categoricas.csv) | Correspondencia entre niveles originales y grupos definidos por significado. |
| [resumen_agrupaciones_entrenamiento.csv](resumen_agrupaciones_entrenamiento.csv) | Frecuencias y tasas tras agrupar, incluida la ausencia explícita. |
| [imputacion_entrenamiento.csv](imputacion_entrenamiento.csv) | Ausencias antes y después del imputador y medianas aprendidas en este entrenamiento. |

La [justificación de las agrupaciones](../docs/Agrupaciones-categoricas.md) explica la información que se conserva y la que se simplifica. Las tasas de grupos pequeños tienen poco respaldo y no se utilizan para elegir las fusiones. Las imputaciones se vuelven a aprender dentro de cada fold al evaluar modelos. Estos cuatro informes no contienen identificadores individuales.

## Comparación inicial de modelos

Los siguientes informes se regeneran en la sección «Comparación inicial de modelos». Utilizan los cinco folds de los **1.238 registros de desarrollo**, con reparto aleatorio estratificado por cliente, umbral 0,5 y preparación ajustada dentro de cada entrenamiento. Los tres modelos utilizan clases ponderadas (`balanced`), con pesos aprendidos por entrenamiento; las métricas no aplican esos pesos. No incluyen una evaluación de test.

| Archivo | Contenido |
|---|---|
| [modelos_iniciales_por_fold.csv](modelos_iniciales_por_fold.csv) | 15 ajustes: tres modelos, cada uno en cinco folds. Métricas de validación y F1 de entrenamiento. |
| [comparacion_inicial.csv](comparacion_inicial.csv) | Media no ponderada entre folds de cada métrica y desviación muestral del F1. La desviación no es un intervalo de confianza. |
| [errores_validacion_inicial.csv](errores_validacion_inicial.csv) | Recuentos agregados por candidato: TN, FP, FN y TP; clase positiva 1, rechazo registrado. |
| [configuracion_modelos_iniciales.json](configuracion_modelos_iniciales.json) | Parámetros de los estimadores, umbral, preparación y candidato provisional; sin reajuste final ni test evaluado. |

`predicciones_cv_inicial.csv` se conserva **solo en local**, excluido de Git: contiene identificador, candidato, fold, etiqueta registrada, puntuación y predicción. Cada registro aparece una vez por candidato. El notebook muestra la tabla principal de métricas en porcentaje tras entrenar, seguida de una tabla de F1 de entrenamiento y validación, un gráfico de variación entre folds y las tres matrices de confusión. Los recuentos se conservan en CSV sin repetirlos en otra tabla del notebook. Las matrices se calculan con esas predicciones de validación; el F1 obtenido al agregarlas no sustituye al F1 medio por fold utilizado para comparar.

La precisión se muestra como 0 por convenio si no hay predicciones positivas; los recuentos permiten reconocer ese caso. Las puntuaciones no se presentan como probabilidades de impago ni como probabilidades calibradas. La elección provisional conserva una configuración, no un modelo final ni el mejor ajuste de un fold.

## Contrastes de preparación

La sección «Contrastes de preparación» compara cuatro alternativas con la preparación actual en logística y Random Forest: P99 de ingreso y familia; ambos recortes sin hijos; logaritmo del ingreso; y los cuatro tratamientos. Se reutilizan diez resultados por fold de la comparación inicial y se calculan cuarenta ajustes nuevos. Se conservan las filas de desarrollo, los folds, los parámetros y el umbral 0,5.

Los percentiles se aprenden dentro de cada entrenamiento; familia utiliza interpolación `higher` para elegir un valor observado. El logaritmo se aplica después del recorte cuando se combinan. Los CSV originales no se modifican y test no se utiliza para ajustar esas decisiones.

| Archivo | Contenido |
|---|---|
| [preparaciones_por_fold.csv](preparaciones_por_fold.csv) | 50 filas: diez combinaciones de modelo/preparación en cinco folds; incluye las dos referencias iniciales reutilizadas. |
| [comparacion_preparaciones.csv](comparacion_preparaciones.csv) | Medias de métricas, dispersión de F1 y cambio frente a la preparación actual. Métricas y Delta_F1 en escala 0–1; el notebook multiplica por 100. |
| [diferencias_preparaciones_por_fold.csv](diferencias_preparaciones_por_fold.csv) | 40 diferencias emparejadas de los ocho candidatos nuevos frente a su referencia; Cambio_F1 en puntos porcentuales. |
| [configuracion_preparaciones.json](configuracion_preparaciones.json) | Tratamientos, percentiles, orden, criterio, parámetros de referencia y preparación elegida. |

`predicciones_cv_variantes.csv` contiene las **9.904 predicciones** de los ocho candidatos, con identificadores. Está excluido de Git y se conserva solo en local. Las predicciones de las dos preparaciones actuales ya constan en el archivo inicial.

Se conserva la preparación actual de ambos modelos: las ventajas máximas de F1 (0,68 puntos en logística y 0,30 en el bosque) no alcanzan el punto porcentual exigido para cambiarla. Los resultados corresponden a selección en desarrollo, no a optimización de hiperparámetros, reajuste final o evaluación de test. Las plantillas elegidas no están entrenadas para entregar.

## Búsqueda y comparación de Random Forest

La búsqueda de «Optimización y evaluación final» compara 36 configuraciones en los cinco folds de desarrollo, sin reajuste automático ni test durante esa búsqueda. Mantiene 100 árboles y semilla 42, y utiliza la misma regla de F1 que la comparación inicial, con clase positiva para puntuaciones mayores o iguales a 0,5. Se reutilizan las métricas iniciales y se evalúa la configuración elegida en cinco ajustes adicionales para completar el diagnóstico.

| Archivo | Contenido |
|---|---|
| [busqueda_random_forest.csv](busqueda_random_forest.csv) | 36 filas con parámetros, métricas de entrenamiento y validación por fold, medias, dispersiones y tiempos. Los campos vacíos de parámetros representan `None`, según la rejilla del JSON. |
| [bosque_ajustado_por_fold.csv](bosque_ajustado_por_fold.csv) | Cinco resultados del bosque elegido, con F1 de entrenamiento y todas las métricas de validación. |
| [comparacion_desarrollo.csv](comparacion_desarrollo.csv) | Cuatro candidatos: logística, árbol, bosque inicial y ajustado; métricas medias y dispersión muestral de F1. |
| [diferencias_bosque_ajustado.csv](diferencias_bosque_ajustado.csv) | F1 inicial, ajustado y diferencia, emparejados por fold. Escala 0–1; el notebook los muestra multiplicados por 100. |
| [errores_bosques_desarrollo.csv](errores_bosques_desarrollo.csv) | Matrices agregadas de ambos bosques: TN, FP, FN y TP. |
| [configuracion_busqueda.json](configuracion_busqueda.json) | Rejilla, criterio, parámetros del máximo y de la elección, regla del umbral y estado sin reajuste final ni test. |

`Desv_F1` se calcula con `ddof=1` para conservar el criterio muestral del proyecto. Los campos `std_test_score` y `std_train_score` originales de GridSearchCV usan `ddof=0`; no son intervalos de confianza. Las métricas se conservan en escala 0–1. El campo `params` del CSV es descriptivo; el JSON conserva los tipos de los parámetros.

`predicciones_cv_bosque_ajustado.csv` contiene 1.238 predicciones individuales de validación y permanece solo en local, excluido de Git. No contiene predicciones de test. Las métricas de búsqueda y la reevaluación en sus mismos folds son resultados de desarrollo usados para seleccionar, no una comprobación independiente.

La propuesta es el bosque con `max_features=0.5`, ponderación, profundidad sin límite y hoja mínima 1: F1 53,18 %, recall 48,57 %, precisión 58,87 %, AUC 73,66 % y accuracy 90,31 %. Detecta cinco rechazos más que la referencia y genera diez falsas alertas adicionales. Esta es la propuesta de desarrollo; el cierre con umbral fijado en 0,5 figura a continuación.


## Evaluación final

Los cuatro pipelines se reajustan exclusivamente con 1.238 clientes de desarrollo y se evalúan sobre el mismo test de 310 clientes. La elección principal y el umbral 0,5 se registran antes de calcular predicciones. Las métricas están en escala 0–1; los costes son euros hipotéticos para la muestra, no euros observados.

| Archivo | Contenido |
|---|---|
| [decisiones_pretest.json](decisiones_pretest.json) | Elección y parámetros de los cuatro candidatos, regla del umbral, fuentes, reparto, escenarios y selección de ejemplos, registrados antes de test. |
| [metricas_test.csv](metricas_test.csv) | F1, precisión, recall, ROC-AUC con puntuaciones y accuracy de los cuatro candidatos. |
| [errores_test.csv](errores_test.csv) | TN, FP, FN y TP de cada candidato sobre 310 clientes. |
| [importancias_bosque_final.csv](importancias_bosque_final.csv) | Importancias por impureza sobre las entradas preparadas, calculadas con el modelo aprendido en desarrollo; no causalidad ni explicación individual. |
| [costes_hipoteticos_test.csv](costes_hipoteticos_test.csv) | Supuestos de coste FP/FN y sus totales para los cuatro modelos. |
| [evaluacion_final.json](evaluacion_final.json) | Decisiones previas, versiones, reajuste realizado, métricas, errores y límite de la entrega. |

El elegido obtiene F1 54,84 % y AUC 86,05 %, con 17 TP, 18 FN, 10 FP y 265 TN. El bosque inicial obtiene mejor F1 (61,02 %) y menos FP/FN; la mejora de selección no se confirma en test. No se modifica la elección ni se vuelven a ajustar parámetros con esos resultados.

`predicciones_test.csv` (1.240 filas: 310 por candidato) y `casos_test.csv` (cinco ejemplos) permanecen locales y excluidos de Git. El [modelo final](../models/README.md) también se genera localmente. Los JSON de las fases iniciales conservan el estado de esas fases; `evaluacion_final.json` describe el cierre. Los informes de diagnóstico o desarrollo no pasan a ser informes de test.


Los JSON originales conservan también la previsión de un diagnóstico por segmentos que quedó fuera de la presentación final. Ese informe no forma parte de esta entrega ni se regenera con el notebook actual; no intervino en la selección ni modifica las métricas globales.
