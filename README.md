# Clasificación de solicitudes de tarjeta

Análisis de solicitudes de tarjeta de crédito mediante modelos de clasificación, con atención a la interpretación de los datos, los errores de predicción y la claridad del procedimiento. Proyecto de portfolio desarrollado a partir de la práctica de clasificación del curso JYTS.

**Estado:** objetivo, datos, calidad, preparación y comparación inicial implementados. Se evalúan dos referencias y tres modelos en cinco folds de desarrollo. Con clases ponderadas y umbral 0,5, Random Forest encabeza el F1 medio (0,520). El proyecto continúa en mejora, sin modelo final ni evaluación de test.

[Notebook](notebooks/01-analisis-y-modelado.ipynb) · [Memoria](docs/Memoria-proyecto.md) · [Datos y descarga](data/README.md)

## Problema y alcance

En admisión de crédito, aceptar una operación problemática puede producir pérdidas, mientras que rechazar una solicitud adecuada puede reducir ingresos y oportunidades. El proyecto estudia qué información aportan los atributos personales, laborales y financieros al análisis de solicitudes y cómo comparar modelos considerando ambos tipos de error.

La fuente disponible registra **decisiones históricas**, no impagos observados: `label = 0` significa aprobación y `label = 1`, rechazo. El objetivo técnico es clasificar esa decisión registrada, con el rechazo como clase positiva. Una predicción positiva señala semejanza con solicitudes rechazadas; no demuestra insolvencia ni que el rechazo original fuera correcto.

La unidad de análisis es el cliente identificado por `Ind_ID`, definido como `Client ID` en la fuente. Los 1.548 identificadores son únicos: hay una observación por cliente identificado y la clave se usa para unir y controlar, sin entrar al modelo. Clientes con claves diferentes pueden compartir atributos; esa coincidencia no se trata como duplicación del mismo cliente. No se conocen la cronología, el muestreo o la regla de decisión original. El análisis no establece una política automática de concesión ni demuestra capacidad para anticipar impagos futuros.

## Decisiones que guían el análisis

| Cuestión | Criterio de trabajo |
|---|---|
| Ausencias y situación laboral | Interpretar códigos y contextos antes de imputar. Una ausencia no demuestra ocultación ni desempleo. Los tratamientos estadísticos se ajustarán con entrenamiento. |
| Categorías poco frecuentes | Agrupaciones de ocupación, educación y vivienda documentadas por significado y cobertura en entrenamiento. Su mejora predictiva está pendiente de comparación. No se impone un mínimo común de registros. |
| Variables numéricas | Distinguir códigos especiales, errores y extremos plausibles. Contrastar límites o transformaciones cuando estén justificados, sin fijar de antemano medias, medianas o percentiles. |
| Desbalance y capacidad de revisión | Comparar detección de rechazos y falsas alertas sobre aprobaciones. La accuracy será descriptiva y no decidirá el ganador. La capacidad real de revisión se desconoce. |
| Explicabilidad y pertinencia | Examinar reglas, contribución de variables y errores relevantes. Las asociaciones no prueban causalidad, equidad o legitimidad de uso de atributos personales. |
| Consecuencias económicas | Explorar escenarios explícitos de coste de errores. Serán supuestos de decisión, no pérdidas por impago ni ahorros bancarios observados. |

## Evaluación y resultado esperado

Se reserva aleatoriamente el **20 % para test** (310 registros) y se comparan candidatos mediante **cinco folds aleatorios y estratificados** en los 1.238 registros de desarrollo. Se separan los identificadores de cliente, sin agrupar por atributos coincidentes. La estratificación mantiene aproximadamente la proporción de clases; semillas 42 y 43 fijan el reparto sin buscar una semilla favorable. La exploración inicial utiliza las 990 filas del entrenamiento del primer fold.

El criterio principal es el **F1 medio no ponderado entre folds de la clase rechazo**, acompañado de su dispersión, recall, precisión, ROC-AUC calculado con puntuaciones y matrices de confusión. El umbral inicial es **0,5**. Se incluyen dos referencias —clase mayoritaria del entrenamiento y siempre rechazo—, regresión logística, árbol de decisión y Random Forest. Todos comparten las mismas particiones y cada preparación se ajusta dentro de su entrenamiento. Los tres modelos usan `class_weight="balanced"`, calculado por entrenamiento; las métricas se calculan sin ponderar observaciones. Se parte de la complejidad predeterminada: logística L2 con C=1, árbol sin profundidad máxima y bosque de 100 árboles, con mínimo una observación por hoja en ambos tipos de árbol. La ponderación no equivale a costes de negocio ni garantiza una mejora universal.

Entre candidatos situados a no más de **0,01 de F1** del mejor, se priorizarán logística, árbol y bosque, en ese orden. Dentro de una familia se preferirá menor dispersión entre folds y, después, mayor F1 medio. Esta regla limita la complejidad por diferencias pequeñas; no demuestra equivalencia estadística ni establece una mejora mínima útil para un banco. La explicación y las limitaciones de los candidatos se documentarán junto a la elección.

Se compararán pocas mejoras justificadas, incluidas alternativas a las agrupaciones iniciales, transformaciones o variables derivadas y una búsqueda de hiperparámetros que permita bosques de distintas capacidades. Los resultados de validación orientarán la elección; la evaluación de cierre no se utilizará para cambiarla. La ganancia mínima útil y los costes reales no están establecidos.

El conjunto público ya ha sido examinado durante el desarrollo. Repartirlo de nuevo no crea una prueba independiente: las métricas se presentarán como **evaluación interna**, con validación en datos nuevos pendiente. El [registro de evaluación](evaluacion/README.md) conserva el procedimiento, la configuración y los tamaños de las muestras. Los ajustes de umbral, si se realizan, se decidirán solo en desarrollo.

La entrega prevista incluirá una tabla comparativa, interpretación de errores, justificación del modelo elegido, escenarios de coste y cinco ejemplos de evaluación seleccionados con una regla explícita. Esos ejemplos ilustrarán predicciones, no una implantación en producción.

## Preparación inicial

La exploración conserva los extremos sin error confirmado y las dos cantidades familiares como referencia inicial. Quedan propuestos dos contrastes separados: limitar el ingreso al P99 aprendido en entrenamiento y excluir el número de hijos conservando el tamaño familiar y el estado civil. La diferencia familia–hijos se explora, pero no se añade al modelo. Estas variantes todavía no se han aplicado ni evaluado predictivamente.

Se convierten los días relativos en años, se separa el código especial de empleo y se añade un indicador de ingreso ausente. Se agrupan ocupaciones en seis familias, educación en tres niveles y vivienda en cuatro modalidades; las [correspondencias y sus límites](docs/Agrupaciones-categoricas.md) explican qué información se simplifica.

Las categorías ausentes se representan explícitamente. Ingreso y edad se imputan con medianas aprendidas en entrenamiento. Para el código especial de empleo se utiliza duración cero como soporte de cálculo junto con su indicador, sin presentarlo como antigüedad observada. El pipeline reúne estas reglas, la codificación nominal y el escalado para logística. Los indicadores binarios permanecen en 0/1; para árboles se desactiva el escalado.

La preparación produce 40 columnas en el entrenamiento inspeccionado y acepta una categoría futura no conocida. Esa tabla preparada sirve para diagnóstico; la comparación ajusta una copia nueva del pipeline en cada fold a partir de las entradas originales.

## Resultados iniciales de desarrollo

Medias de cinco folds, clase positiva rechazo y umbral 0,5; no son resultados de test:

| Candidato | F1 medio | Desv. F1 | Precisión | Recall | ROC-AUC | Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| Mayoritaria | 0,000 | 0,000 | 0,000 | 0,000 | 0,500 | 0,887 |
| Siempre rechazo | 0,203 | 0,000 | 0,113 | 1,000 | 0,500 | 0,113 |
| Logística | 0,242 | 0,064 | 0,159 | 0,507 | 0,612 | 0,643 |
| Árbol | 0,408 | 0,042 | 0,392 | 0,429 | 0,671 | 0,859 |
| Random Forest | 0,520 | 0,115 | 0,630 | 0,450 | 0,743 | 0,907 |

Random Forest queda como candidato provisional por su F1: detecta 63 de los 140 rechazos y genera 38 falsos rechazos. La logística detecta 71, pero genera 373 falsas alertas; el árbol detecta 60 y genera 94. Los tres superan por F1 medio la referencia de siempre rechazo, sin que ello demuestre utilidad bancaria.

El bosque presenta F1 de entrenamiento 0,971 frente a 0,520 en validación; el árbol también muestra una brecha amplia. El siguiente bloque estudiará ajustes acotados de complejidad y los contrastes pendientes de P99 y exclusión de `CHILDREN`, sin seleccionar por test. Los [resultados por fold y errores](reports/README.md) y la [memoria](docs/Memoria-proyecto.md) desarrollan la interpretación. No hay modelo final ni evaluación de test.

## Recorrido y archivos

El notebook se desarrollará en seis secciones: **objetivo y datos; calidad y evaluación; exploración y preparación; comparación inicial de modelos; mejoras seleccionadas; evaluación e interpretación**.

| Ruta | Contenido actual |
|---|---|
| [notebooks/01-analisis-y-modelado.ipynb](notebooks/01-analisis-y-modelado.ipynb) | Cuatro secciones ejecutadas, hasta comparación inicial de modelos. Mejoras y cierre pendientes. |
| [docs/Memoria-proyecto.md](docs/Memoria-proyecto.md) | Decisiones y conclusiones del recorrido implementado. |
| [docs/Diccionario-datos.md](docs/Diccionario-datos.md) | Significado, papel y límites de los campos. |
| [docs/Agrupaciones-categoricas.md](docs/Agrupaciones-categoricas.md) | Criterios semánticos, cobertura y límites de las agrupaciones iniciales. |
| [src/preparacion.py](src/preparacion.py) | Conversiones, indicadores y agrupaciones reutilizables, sin estadísticas aprendidas fuera del pipeline. |
| [src/evaluacion.py](src/evaluacion.py) | Rutina común que clona, entrena y evalúa candidatos en los folds fijados. |
| [reports/README.md](reports/README.md) | Diagnóstico de entrenamiento y comparación de modelos: métricas, errores agregados y configuraciones. |
| [data/README.md](data/README.md) e [inventario](data/inventario_fuentes.json) | Obtención y huellas de los archivos utilizados. Los CSV se conservan localmente en `data/raw/` y están excluidos de Git. |
| [evaluacion/README.md](evaluacion/README.md) | Configuración y resúmenes de las particiones. La asignación individual se genera localmente y queda excluida de Git. |
| [requirements.txt](requirements.txt) | Dependencias de la sección implementada. Se ampliarán cuando el código las necesite. |

Los ejemplos de predicción y los artefactos de modelos se incorporarán cuando se desarrollen esas fases.

## Ejecución

Entorno utilizado: **Python 3.13.2**. Desde la raíz del repositorio:

```bash
python -m venv .venv
```

En Windows:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

En macOS/Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

1. Descargar los dos CSV y situarlos en `data/raw/`, siguiendo las [instrucciones de datos](data/README.md).
2. Abrir el notebook en VS Code con soporte Jupyter, o en un entorno Jupyter compatible, y seleccionar el Python del entorno creado.
3. Reiniciar el kernel y ejecutar las celdas en orden. La carga admite como directorio de trabajo la raíz del repositorio o `notebooks/`.

La ejecución de las cuatro secciones implementadas se comprueba en Windows; no se ha comprobado otra plataforma. No se necesitan cuentas bancarias, claves de API ni acceso al curso para ejecutar el código con los CSV descargados.

## Fuente

Datos: [Credit card Details Binary Classification Problem](https://www.kaggle.com/datasets/rohitudageri/credit-card-details), de Rohit Udageri. La ficha declara CC0; la procedencia y los límites se recogen en [datos](data/README.md). El planteamiento procede de la práctica P09 del curso JYTS; el repositorio contiene el desarrollo del proyecto, sin incorporar los materiales originales del curso.
