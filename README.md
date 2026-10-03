# Clasificación de solicitudes de tarjeta de crédito

Simulación del análisis de solicitudes de tarjeta en un departamento de admisión de crédito. Se comparan regresión logística, árbol de decisión y Random Forest, interpretando los datos y los errores en su contexto de negocio.

El proyecto está terminado. La evaluación final muestra tanto el rendimiento obtenido como una conclusión relevante: el ajuste de hiperparámetros mejoró ligeramente la validación, pero **no superó al bosque inicial en F1 de test**.

[Ver notebook](notebooks/clasificacion-solicitudes-tarjeta.ipynb) · [Resultados](#resultados) · [Cómo ejecutarlo](#ejecución) · [Datos y descarga](data/README.md)

## Problema y datos

En admisión de crédito, aceptar una operación problemática puede generar pérdidas y rechazar una solicitud adecuada puede suponer perder negocio. El análisis compara la capacidad de los modelos para distinguir solicitudes, considerando tanto la detección de rechazos como las falsas alertas sobre aprobaciones.

Los datos proceden de [Credit card Details Binary Classification Problem, publicado por Rohit Udageri en Kaggle](https://www.kaggle.com/datasets/rohitudageri/credit-card-details). Se unen dos archivos por `Ind_ID`:

| Archivo | Contenido |
|---|---|
| `Credit_card.csv` | Identificador y atributos personales, laborales y financieros. |
| `Credit_card_label.csv` | Identificador y decisión registrada: **0 = aprobación; 1 = rechazo**. |

Hay **1.548 clientes identificados**, con **175 rechazos (11,30 %)**. La fuente define `Ind_ID` como identificador de cliente y sus valores son únicos. Se utiliza para unir y comprobar las tablas, sin incluirlo como predictor. Las coincidencias de atributos entre identificadores distintos se conservan.

El objetivo técnico es clasificar la **decisión histórica**, con el rechazo como clase positiva. La etiqueta no registra impagos ni demuestra que la decisión original fuera correcta. Por ello, el proyecto no acredita capacidad para anticipar morosidad ni establece una política de concesión. El [diccionario de datos](docs/Diccionario-datos.md) recoge el significado y los límites de cada campo.

## Criterios de negocio y preparación

| Cuestión | Decisión aplicada y motivo |
|---|---|
| Ausencias y situación laboral | Se distingue el código especial de empleo de una antigüedad real. Una ocupación ausente no se interpreta automáticamente como desempleo u ocultación. Las categorías ausentes se representan explícitamente y se conserva el contexto laboral. |
| Ingresos, edad y extremos | Se convierten los días relativos en años y se imputan ingreso y edad con medianas de entrenamiento. La rareza no basta para borrar registros: se conservan los extremos y se contrastan recortes y transformaciones. El ingreso registrado no se interpreta como ingreso total del hogar. |
| Categorías poco frecuentes | Se agrupan ocupación, educación y vivienda por significados compatibles, sin equiparar categorías solo por tener pocos casos ni atribuirles la misma solvencia. Las [agrupaciones](docs/Agrupaciones-categoricas.md) documentan la simplificación; no se ha aislado su ventaja frente a las categorías originales. |
| Desbalance y errores | Los modelos iniciales ponderan las clases durante el entrenamiento. Se valoran F1, recall y precisión de los rechazos; la accuracy queda como complemento. Las métricas no se ponderan y los pesos no representan costes bancarios. |
| Explicabilidad y pertinencia | Se comparan modelos de distinta complejidad y se muestran importancias del bosque. Estas describen el ajuste, sin explicar cada rechazo, demostrar causalidad o acreditar equidad y pertinencia del uso de atributos personales. |
| Consecuencias económicas | Se presentan escenarios de coste de falsos rechazos y rechazos omitidos. Los importes son hipotéticos: no representan pérdidas por impago, ahorros observados ni una capacidad real de revisión. |

La preparación reúne conversiones, indicadores, imputación y codificación dentro de un pipeline. Las cantidades se escalan para logística; los árboles trabajan sin ese escalado. Cada ajuste aprende sus estadísticas únicamente con el entrenamiento correspondiente.

## Comparación y selección

Se reservan **310 registros para test (20 %)**. Los **1.238 de desarrollo** se comparan mediante cinco particiones de validación cruzada estratificada, comunes a todos los candidatos. Se separan identificadores de cliente, permitiendo atributos coincidentes; las semillas quedan fijadas sin buscarlas por sus resultados. El [diseño de evaluación](evaluacion/README.md) detalla el reparto.

La selección utiliza el **F1 medio de la clase rechazo**, con umbral **0,5**, acompañado de dispersión, precisión, recall, ROC-AUC y matrices de confusión. Dentro de un punto porcentual del mejor F1 se prioriza logística, árbol y bosque, en ese orden; dentro de una familia, menor dispersión y después mayor F1. Es una regla práctica de comparación, no una prueba de equivalencia ni un criterio de rentabilidad.

El recorrido del notebook mantiene seis secciones:

1. **Objetivo y datos:** carga, unión de las tablas e interpretación de la etiqueta.
2. **Calidad y evaluación:** códigos, ausencias, perfiles coincidentes y particiones.
3. **Exploración y preparación:** distribuciones, relaciones y tratamientos justificados.
4. **Comparación inicial de modelos:** métricas, brecha entre entrenamiento y validación y errores.
5. **Contrastes de preparación:** cuatro combinaciones de recorte al P99 de ingreso y familia, exclusión de hijos y logaritmo del ingreso. Ninguna alcanza la mejora mínima de un punto de F1; se conserva la preparación inicial.
6. **Optimización y evaluación final:** Grid Search de 36 configuraciones de Random Forest, elección en desarrollo y evaluación de los cuatro candidatos en test, seguida de interpretación y conclusiones.

El bosque ajustado se selecciona por su F1 de desarrollo: **53,18 % frente a 52,04 %** del inicial. Mantiene 100 árboles, profundidad sin límite, una observación mínima por hoja, `max_features=0.5` y clases ponderadas. Se fijan modelo y umbral antes de test y se reajustan los cuatro pipelines con todo desarrollo. La búsqueda no garantiza una mejora fuera de esas particiones.

## Resultados

**Evaluación sobre los mismos 310 clientes de test**, con 35 rechazos y umbral 0,5. Las métricas se muestran en porcentaje; ROC-AUC utiliza las puntuaciones, no las clases predichas.

| Modelo | F1 | Precisión | Recall | ROC-AUC | Accuracy |
|---|---:|---:|---:|---:|---:|
| Logística | 26,28 % | 17,65 % | 51,43 % | 68,70 % | 67,42 % |
| Árbol | 25,86 % | 18,52 % | 42,86 % | 64,97 % | 72,26 % |
| Random Forest | 61,02 % | 75,00 % | 51,43 % | 84,88 % | 92,58 % |
| Random Forest ajustado | 54,84 % | 62,96 % | 48,57 % | 86,05 % | 90,97 % |

El ajustado, elegido en desarrollo, detecta **17 de 35 rechazos**, omite 18 y genera 10 falsos rechazos. El bosque inicial detecta 18, omite 17 y genera 6 falsas alertas. La ventaja del ajustado en validación **no se confirma en F1 de test**, aunque obtiene mayor ROC-AUC. Se informa de este resultado conservando la selección previa, sin utilizar test para volver a elegir un ganador.

El notebook completa la lectura con matrices de confusión, tres escenarios económicos hipotéticos y cinco ejemplos tomados por posición, sin elegirlos por acierto. Los cinco resultan ser aprobaciones; ilustran la salida del modelo y no sustituyen el balance completo de errores. Las [métricas finales](reports/metricas_test.csv), los [recuentos de errores](reports/errores_test.csv) y la [configuración de cierre](reports/evaluacion_final.json) conservan la evidencia.

## Alcance y límites

- El conjunto público ya se había examinado antes de fijar el protocolo. El cierre es una **evaluación interna**, no una validación externa o completamente inédita; el test reservado no interviene en la selección posterior.
- Faltan fechas, muestreo documentado, regla de aprobación y momento de disponibilidad de los atributos. Tampoco hay costes reales ni evidencia de impacto económico.
- Solo hay 35 rechazos en test: un caso cambia el recall en 2,86 puntos. La brecha entre entrenamiento y validación del bosque sigue siendo amplia; no se considera resuelto el sobreajuste.
- Las agrupaciones y otros supuestos de representación no se han contrastado individualmente en su totalidad. Los resultados no acreditan un óptimo global ni generalización a otro banco o población.

**La entrega es un análisis reproducible, sin recomendar aprobación o rechazo automáticos.** Una investigación posterior necesitaría evidencia independiente para justificar mejoras; este test ya consultado no constituye una reserva desconocida.

## Archivos del proyecto

| Ruta | Función |
|---|---|
| [notebooks/clasificacion-solicitudes-tarjeta.ipynb](notebooks/clasificacion-solicitudes-tarjeta.ipynb) | Recorrido completo: código, visualizaciones, decisiones y conclusiones. |
| `docs/` | [Diccionario de datos](docs/Diccionario-datos.md) y [criterios de agrupación](docs/Agrupaciones-categoricas.md). |
| [data/README.md](data/README.md) | Descarga y colocación de los CSV; el [inventario](data/inventario_fuentes.json) identifica los archivos utilizados. |
| `src/` | Funciones de [preparación](src/preparacion.py) y [evaluación](src/evaluacion.py) utilizadas por el notebook. |
| [evaluacion/](evaluacion/README.md) | Configuración y resúmenes de las particiones. |
| [reports/](reports/README.md) | Métricas, diagnósticos y configuraciones guardadas. |
| [models/](models/README.md) | Instrucciones del pipeline entrenado, generado localmente al ejecutar el cierre. |
| [requirements.txt](requirements.txt) | Versiones de las dependencias utilizadas. |

Los CSV originales se descargan en `data/raw/`. Los datos, las asignaciones individuales, las predicciones por cliente y los modelos entrenados están excluidos de Git; se generan o conservan localmente. El notebook sí contiene vistas acotadas de datos y cinco ejemplos, sin mostrar el identificador.

## Ejecución

Entorno utilizado: **Python 3.13.2**. Desde la raíz del repositorio, crear un entorno:

```bash
python -m venv .venv
```

Instalar las dependencias en Windows:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

En macOS/Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

1. Descargar `Credit_card.csv` y `Credit_card_label.csv` desde [Kaggle](https://www.kaggle.com/datasets/rohitudageri/credit-card-details) y colocarlos en `data/raw/`. Las [instrucciones de datos](data/README.md) detallan la descarga y sus límites.
2. Abrir el notebook con VS Code y soporte Jupyter, o con un entorno Jupyter compatible. Seleccionar como kernel el Python de `.venv`.
3. Reiniciar el kernel y ejecutar todas las celdas en orden. El directorio de trabajo debe ser la raíz del repositorio o `notebooks/`; las rutas se resuelven dentro del proyecto, sin carpetas personales.
4. Consultar los resultados en el notebook y en `reports/`. El cierre guarda también el pipeline en `models/clasificador-solicitudes.joblib`; su [guía de uso](models/README.md) explica cómo cargarlo sin entrenar de nuevo.

La ejecución escribe los informes locales y el modelo; conserva los CSV de entrada y comprueba las particiones si ya existen. Repetirla verifica reproducibilidad, sin convertir el test en una nueva evaluación independiente. La ejecución completa se ha comprobado en Windows con las versiones indicadas; no se ha verificado en macOS/Linux.

## Procedencia

El planteamiento del proyecto parte de una práctica del módulo de clasificación del curso "**De 0 a Data Scientist: Python, Machine Learning y Negocio"**, de **Jorge C. Rella**. Se presenta como una simulación analítica, sin atribuir resultados a una implantación bancaria real ni incorporar los materiales originales del curso.

Los datos los publica Rohit Udageri en Kaggle. La [documentación de datos](data/README.md) conserva la consulta de licencia, procedencia y limitaciones de la fuente.
