# Memoria del proyecto: clasificación de solicitudes de tarjeta

## Objetivo y datos

### Planteamiento

El proyecto estudia la clasificación de solicitudes de tarjeta a partir de atributos personales, laborales y financieros. El contexto de admisión de crédito exige considerar tanto las solicitudes problemáticas aceptadas como las solicitudes adecuadas rechazadas. Sin embargo, los datos disponibles identifican aprobación y rechazo históricos, no impago observado. Por ello, la tarea técnica se limita a clasificar `label`, con el rechazo como clase positiva, sin equiparar una decisión histórica a una medida de solvencia.

El criterio inicial de comparación es F1, acompañado de recall, precisión, ROC-AUC y matrices de confusión. La elección concreta se apoyará también en estabilidad y explicabilidad. Los costes de error, la capacidad de revisión y una mejora mínima útil no están acreditados. El diseño de evaluación se desarrollará antes de entrenar modelos; sus resultados tendrán alcance interno sobre un conjunto público ya examinado.

### Fuentes y carga

La sección **Fuentes y carga** importa las dos tablas de Kaggle y muestra sus dimensiones. `Credit_card.csv` aporta 1.548 registros y 18 columnas; `Credit_card_label.csv`, 1.548 registros y 2 columnas. La clave `Ind_ID` se lee como texto para utilizarla como identificador. Los archivos originales se conservan sin cambios y su procedencia se recoge en el [inventario](../data/inventario_fuentes.json).

### Correspondencia entre tablas

En **Correspondencia entre tablas** se comprueba que las claves estén informadas y sean únicas en cada archivo. La unión externa validada uno a uno permite detectar tanto pérdidas como multiplicaciones de filas. Los 1.548 identificadores tienen correspondencia en ambas tablas; no quedan claves exclusivas de una fuente. El resultado contiene 19 columnas: identificador, 17 atributos candidatos y etiqueta. La unicidad de la clave no demuestra que todos los registros correspondan a personas diferentes.

### Primera lectura de los registros

**Primera lectura de los registros** muestra cinco observaciones sin identificador y una tabla conjunta de tipos leídos y ausencias. Se localizan ausencias en género, ingreso anual, fecha relativa de nacimiento y ocupación; esta inspección no les atribuye causas ni aplica tratamientos. El [diccionario](Diccionario-datos.md) distingue cantidades, códigos, categorías y límites de interpretación. Los días relativos carecen de fecha de referencia y la moneda del ingreso no está documentada.

### Etiqueta y entradas candidatas

**Etiqueta y entradas candidatas** comprueba que la respuesta esté informada y pertenezca a los valores 0 y 1. Hay 1.373 aprobaciones (88,70 %) y 175 rechazos (11,30 %). Este desbalance justifica acompañar la exactitud con métricas de la clase positiva; no determina por sí solo una ponderación ni un umbral.

Se separan `X`, con 17 entradas candidatas, `y`, con la etiqueta, y los identificadores de control. Todavía no hay particiones, selección definitiva de variables o tratamientos aprendidos. La siguiente sección abordará calidad y evaluación. La preparación posterior incluirá agrupaciones categóricas con significados compatibles; sus correspondencias y frecuencias se justificarán sobre entrenamiento.
