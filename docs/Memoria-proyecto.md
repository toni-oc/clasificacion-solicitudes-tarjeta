# Memoria del proyecto: clasificación de solicitudes de tarjeta

## Objetivo y datos

### Planteamiento

El proyecto estudia la clasificación de solicitudes de tarjeta a partir de atributos personales, laborales y financieros. El contexto de admisión de crédito exige considerar tanto las solicitudes problemáticas aceptadas como las solicitudes adecuadas rechazadas. Sin embargo, los datos disponibles identifican aprobación y rechazo históricos, no impago observado. Por ello, la tarea técnica se limita a clasificar `label`, con el rechazo como clase positiva, sin equiparar una decisión histórica a una medida de solvencia.

El criterio de comparación es F1, acompañado de recall, precisión, ROC-AUC y matrices de confusión. La elección concreta se apoyará también en estabilidad y explicabilidad. Los costes de error, la capacidad de revisión y una mejora mínima útil no están acreditados. El diseño de evaluación descrito más adelante se fija antes de entrenar modelos; sus resultados tendrán alcance interno sobre un conjunto público ya examinado.

### Fuentes y carga

La sección **Fuentes y carga** importa las dos tablas de Kaggle y muestra sus dimensiones. `Credit_card.csv` aporta 1.548 registros y 18 columnas; `Credit_card_label.csv`, 1.548 registros y 2 columnas. La clave `Ind_ID` se lee como texto para utilizarla como identificador. Que ambas tablas tengan el mismo número de filas no garantiza que sus claves coincidan; por eso se comprueba su correspondencia antes de analizar los registros conjuntos. Los archivos originales se conservan sin cambios y su procedencia se recoge en el [inventario](../data/inventario_fuentes.json).

### Correspondencia entre tablas

En **Correspondencia entre tablas** se comprueba que las claves estén informadas y sean únicas en cada archivo. La unión externa validada uno a uno permite detectar tanto pérdidas como multiplicaciones de filas. Los 1.548 identificadores tienen correspondencia en ambas tablas; no quedan claves exclusivas de una fuente. El resultado contiene 19 columnas: identificador, 17 atributos candidatos y etiqueta. La fuente define `Ind_ID` como identificador de cliente (`Client ID`). Se adopta una observación por cliente identificado, sin varias filas asociadas al mismo cliente según esa clave. Esta interpretación sigue la documentación y no equivale a verificar externamente la identidad de las personas. La vista de las cinco primeras filas de la tabla unida muestra atributos y etiqueta juntos, sin exponer el identificador.

### Primera lectura de los registros

**Primera lectura de los registros** resume tipos leídos, ausencias y número de valores distintos. Se localizan ausencias en género, ingreso anual, fecha relativa de nacimiento y ocupación. Esta última reúne 488 ausencias (31,52 %); su volumen aconseja estudiar el contexto laboral antes de decidir una imputación, sin atribuir todavía una causa.

`Mobile_phone` presenta un único valor, 1, sin ausencias en las 1.548 observaciones. Por tanto, no distingue solicitudes en esta muestra y se identifica como prescindible para modelar. Su exclusión de las entradas se aplica después, en **Campos para modelar**, conservando la tabla original.

El [diccionario](Diccionario-datos.md) distingue cantidades, códigos, categorías y límites de interpretación. Los días relativos carecen de fecha de referencia y la moneda del ingreso no está documentada. Esta inspección no aplica imputaciones ni conversiones.

### Etiqueta y entradas candidatas

**Etiqueta y entradas candidatas** comprueba que la respuesta esté informada y pertenezca a los valores 0 y 1. Hay 1.373 aprobaciones (88,70 %) y 175 rechazos (11,30 %). Este desbalance justifica acompañar la exactitud con métricas de la clase positiva; no determina por sí solo una ponderación ni un umbral.

En este primer momento se separan `X`, con 17 entradas candidatas, `y`, con la etiqueta, y los identificadores de control. La sección siguiente revisa esos campos y define las particiones. La preparación posterior incluirá agrupaciones categóricas con significados compatibles; sus correspondencias y frecuencias se justificarán sobre entrenamiento.

## Calidad y evaluación

### Códigos y coherencia básica

Se comprueban los dominios de género, tenencia de automóvil y propiedad, y los indicadores de teléfono y correo. Los valores informados pertenecen a los dominios esperados. No se detectan infinitos, ingresos negativos, recuentos negativos o fraccionarios, nacimientos con desplazamiento no negativo ni inicios de empleo anteriores al nacimiento en las comprobaciones realizadas.

La relación entre hijos y miembros de familia señala dos registros con un hijo y un miembro de familia. Sin una definición más precisa del hogar ni información de procedencia, no se puede resolver esa discrepancia. Se conservan y se registra la limitación. Esta revisión no impone límites estadísticos ni interpreta como errores los extremos plausibles, que se estudiarán en entrenamiento.

### Empleo y ausencia de ocupación

El único valor positivo de `Employed_days` es 365243. Aparece en 261 registros con `Type_Income = Pensioner`, todos sin ocupación informada. Su sentido es el de un código especial, no una antigüedad laboral real. La asociación observada tampoco permite equiparar todas las situaciones de pensionista a desempleo.

Quedan otras 227 ausencias de ocupación en registros con días de empleo no positivos. Representar las 488 ausencias sin conservar ese contexto ocultaría situaciones diferentes. En este diagnóstico se registra la distinción; su representación se implementa después, en la preparación.

### Perfiles repetidos y etiquetas distintas

Los 17 atributos originales, excluyendo identificador y etiqueta, forman 1.377 perfiles distintos. Se consideran iguales las ausencias en un mismo campo. Hay 150 perfiles repetidos, que reúnen 321 registros; 9 perfiles, con 22 registros, contienen tanto aprobaciones como rechazos.

Se comprueba además que cada grupo contiene tantos identificadores distintos como registros. Las coincidencias corresponden a clientes diferentes según la clave disponible, no a varias observaciones del mismo cliente identificado. Se conservan filas y etiquetas; las discrepancias no demuestran cuál de las decisiones sería errónea ni que las coincidencias se deban necesariamente al azar.

Si hubiera observaciones reiteradas de un cliente, habría que estudiar su dependencia y agrupar por ese cliente al evaluar entidades nuevas. Aquí se opta por reparto aleatorio de clientes identificados. Agrupar por atributos impondría evaluar solo perfiles exactos nunca vistos, una restricción adicional que no exige el objetivo. La coincidencia de perfiles queda como diagnóstico y no acredita por sí sola independencia o dependencia entre las personas.

### Campos para modelar

Se excluye `Mobile_phone` por constancia y quedan 16 atributos candidatos. Se conservan los 1.548 registros. `Ind_ID` mantiene la alineación entre entradas y respuesta; el grupo de perfil solo describe coincidencias y no condiciona el reparto. Ninguno entra como predictor. Los datos originales y la definición del perfil conservan el móvil.

La disponibilidad temporal y la pertinencia de los demás campos siguen pendientes de acreditación. Mantenerlos como candidatos no significa que se haya decidido una selección definitiva ni que su uso sea adecuado para una política real de crédito.

### Reglas de evaluación

Se fija F1 medio no ponderado entre cinco folds como criterio principal, con rechazo como clase positiva y umbral inicial 0,5. Se acompañará de dispersión entre folds, recall, precisión, ROC-AUC con puntuaciones y matrices de confusión. Las referencias serán predecir la clase mayoritaria del entrenamiento y predecir siempre rechazo; se calculan en la comparación inicial de modelos.

Dentro de 0,01 de F1 del mejor resultado se priorizarán logística, árbol y bosque, en ese orden. Dentro de una familia se preferirá menor dispersión y después mayor F1 medio. Es una regla práctica para limitar complejidad ante diferencias pequeñas, no una prueba de equivalencia estadística ni un coste de negocio. El ajuste de umbral, si se desarrolla, utilizará únicamente datos de desarrollo.

### Reserva y validación por clientes

Se reserva aleatoriamente el 20 % con `train_test_split`, estratificando por la etiqueta y fijando semilla 42. Dentro de desarrollo se crean cinco folds con `StratifiedKFold`, mezcla aleatoria y semilla 43. Se conserva el orden de entrada de la fuente y el devuelto por el reparto. No se buscan semillas según el resultado de los modelos.

Hay 1.238 registros de desarrollo y 310 de test, con 140 y 35 rechazos. Cada validación tiene 247 o 248 registros y 28 rechazos. Se comprueban identificadores separados, cobertura de cada registro de desarrollo una sola vez y ambas clases en todos los entrenamientos y validaciones. Pueden existir atributos iguales en muestras diferentes, sin compartir el identificador de cliente.

La exploración utiliza los 990 registros del entrenamiento del primer fold, con 112 rechazos. Los tratamientos y los pesos de clase se vuelven a ajustar con cada entrenamiento al comparar modelos. Las decisiones manuales nacidas de la exploración pueden influir en la validación de desarrollo; el pipeline no elimina esa adaptación.

### Conservación de las particiones y alcance

El [registro de evaluación](../evaluacion/README.md) conserva configuración, huellas de las fuentes y resúmenes agregados. La asignación por identificador, uso y fold se genera localmente y se comprueba en las ejecuciones posteriores para impedir un cambio inadvertido del reparto.

El protocolo se revisó después de análisis previos del conjunto. La nueva reserva puede contener registros utilizados anteriormente: entrenar desde cero evita reutilizar ajustes, pero no borra el conocimiento adquirido. El test actual queda apartado de la selección posterior, todavía sin evaluar; sus resultados tendrán alcance de evaluación interna, no de prueba completamente inédita. La falta de cronología, de un método documentado de muestreo y de una muestra externa limita la generalización, y el reducido número de rechazos aconseja cautela ante diferencias pequeñas.

El bloque deja definidos los controles de calidad y el diseño de comparación, antes de aprender tratamientos o entrenar modelos. La siguiente sección explora entrenamiento y justifica la preparación numérica y las agrupaciones categóricas por su significado.

## Exploración y preparación

### Variables y representaciones para explorar

La exploración utiliza los 990 registros del entrenamiento del primer fold, con 112 rechazos. Los días de nacimiento y empleo se convierten en años aproximados mediante 365,25 días por año, sin utilizar la fecha de ejecución. Las cinco cantidades, ocho categorías nominales y cinco indicadores se preparan en copias mediante funciones que no utilizan la respuesta.

El código positivo de empleo se representa por separado. Sus 166 registros no aportan antigüedad interpretable y quedan fuera de los gráficos de duración; no se convierten en cientos de años de empleo.

### Distribuciones, extremos y relaciones numéricas

Los histogramas muestran un ingreso con cola derecha y concentración en recuentos familiares pequeños. Hay 42 ingresos por encima del límite exploratorio IQR de 380.250, incluidos dos de 1.575.000. Aparece también un registro de 14 hijos y 15 miembros de familia. Se revisa su contexto y se conservan: la rareza no confirma un error ni demuestra que su eliminación mejore un modelo.

El P99 del ingreso sería 495.000 y limitaría nueve registros. No se aplica; se reserva como contraste separado y su límite se aprenderá dentro de cada entrenamiento. Tampoco se fijan topes arbitrarios para hijos o familia.

Los boxplots presentan medianas y solapamientos. La antigüedad mediana interpretable es 5,68 años en aprobaciones y 3,90 en rechazos; la edad, 42,09 y 47,27. El ingreso mediano es 166.500 y 157.500, respectivamente. Las cajas representan los percentiles 25–75, no el número de observaciones; cada gráfico incluye su tamaño disponible. El eje logarítmico del ingreso sirve solo para visualizar.

Estas asociaciones no prueban causalidad ni justifican pesos manuales. El Spearman entre hijos y tamaño familiar es 0,814; motiva estudiar redundancia, sin asumir que los campos sean intercambiables.

### Relación entre familia, hijos y estado civil

Se explora `Family_Members − CHILDREN`, sin incorporarlo al pipeline. Vale 1 en 267 registros y 2 en 721, con tasas de rechazo del 12,36 % y 10,68 %. Los ingresos medianos son 168.750 y 162.000 sobre 262 y 712 valores informados. No se observa menor ingreso registrado en el primer grupo, pero tampoco se conocen los ingresos totales del hogar ni el número de perceptores.

La diferencia está ligada al estado civil: separados y viudos aparecen con diferencia 1; casi todos los casados, con diferencia 2. Entre solteros aparecen ambas y un caso con diferencia 0. Los dos registros con diferencia 0 son las alertas de un hijo y un miembro de familia, uno casado y otro soltero. Ambos tienen rechazo; dos observaciones no permiten atribuir riesgo a esa discrepancia ni corregirla sin información adicional.

Se mantienen las dos cantidades y el estado civil. Queda propuesto contrastar una variante sin `CHILDREN`, por separado del P99 y frente al mismo modelo y particiones. No se ha comprobado aún su utilidad predictiva.

### Categorías y agrupaciones con significado

Se calculan frecuencias, rechazos y tasas de las categorías y contactos. Los gráficos se centran en ocupación, educación y vivienda; el [resumen completo](../reports/resumen_categorias_entrenamiento.csv) conserva todos los niveles. `IT staff` tiene dos registros y ambos son rechazos, un respaldo insuficiente para generalizar esa tasa a la ocupación.

Ocupación pasa de 18 niveles a seis familias semánticas: administración y gestión (119), técnicas y profesionales (68), producción y transporte (254), ventas (78), servicios de apoyo (51) y personal general (110). `Core staff` permanece separado por su significado impreciso. Las tasas de rechazo no determinan las fusiones ni las familias implican igualdad salarial o de solvencia.

Educación pasa de cinco niveles a secundaria (684), superior completa (264) y superior incompleta (42). Vivienda pasa de seis niveles a casa o apartamento (879), con familiares (55), alquiler declarado (18) e institucional o colectiva (38). Se mantiene el alquiler separado por significado; la categoría institucional reúne modalidades diferentes y su pérdida de detalle deberá valorarse.

Las [correspondencias y justificaciones](Agrupaciones-categoricas.md) explican las simplificaciones. El estado civil, tipo de ingreso, tenencias y contactos se conservan. Reducir categorías está implementado, pero su ventaja frente a mantenerlas separadas aún no se ha contrastado.

### Ausencias y decisiones de tratamiento

Faltan seis géneros, 14 ingresos, 20 nacimientos y 310 ocupaciones. Entre los ingresos ausentes hay cinco rechazos (35,71 %), frente al 10,96 % entre los informados. Se incluye un indicador de ausencia como hipótesis, sin atribuir ocultación. Las tasas de grupos pequeños, como los cinco rechazos entre seis géneros ausentes, se interpretan con cautela.

Ingreso y edad se imputan con medianas aprendidas en entrenamiento: 162.000 y 42,337 años. La mediana limita la influencia de ingresos extremos sobre la referencia de imputación, sin atribuir cero o un ingreso bajo a un dato desconocido. No se requieren imputaciones de hijos ni tamaño familiar.

Las categorías ausentes reciben `__AUSENTE__`. De las 310 ocupaciones ausentes, 166 acompañan al código positivo de empleo y 144 no. El indicador mantiene diferenciados ambos contextos. Para el código positivo se utiliza duración cero de soporte junto a ese indicador, sin interpretarla como antigüedad observada o experiencia total. Una duración desconocida sin ese código recibiría la mediana del entrenamiento.

### Preparación reutilizable

El pipeline conecta representaciones, reglas fijas, imputación, one-hot y escalado. Las correspondencias están en [preparacion.py](../src/preparacion.py); su construcción permanece visible en el notebook. Los indicadores binarios conservan 0/1. Se escalan cantidades para logística y se desactiva ese paso para árbol y bosque.

La preparación de diagnóstico se ajusta solo con el primer entrenamiento. La comparación posterior clona y vuelve a ajustar todo el pipeline por fold; no utiliza una tabla previamente preparada con todo desarrollo.

### Comprobación del resultado y cierre

Se conservan las 990 filas y se producen 40 columnas numéricas. Se imputan 14 ingresos y 20 edades, manteniendo los valores informados antes del escalado y las conversiones explícitas. Los gráficos antes y después muestran el efecto de la imputación.

Un ejemplo sintético combina ocupación nueva e ingreso ausente. Mantiene las columnas, activa el indicador y codifica la ocupación desconocida con ceros en su bloque, sin reajustar estadísticas. Los [informes](../reports/README.md) conservan frecuencias y medianas. Las coincidencias creadas por agrupar categorías no cambian la unidad de cliente ni las particiones. Los extremos y las dos cantidades familiares permanecen en la preparación inicial.

## Comparación inicial de modelos

### Condiciones de comparación

Se utilizan los 1.238 registros de desarrollo y los cinco folds aleatorios y estratificados ya fijados. Cada cliente se valida una vez, con umbral 0,5. El criterio principal es el F1 medio no ponderado entre folds de la clase rechazo. Los 310 registros de test no se utilizan para entrenar, comparar modelos o interpretar sus errores.

### Referencias y modelos candidatos

La referencia mayoritaria predice la clase más frecuente del entrenamiento y la segunda predice siempre rechazo. Contextualizan accuracy y recall elevados que pueden alcanzarse sin aprender relaciones entre atributos.

Los tres modelos usan `class_weight="balanced"`: cada entrenamiento calcula pesos inversos a la frecuencia de sus clases, de modo que la suma de pesos de ambas clases sea igual. No se duplican filas, no se altera la prevalencia de validación y las métricas se calculan sin aplicar esos pesos. Es una decisión inicial ante el desbalance, no una garantía de mejora ni una estimación de costes bancarios.

La logística utiliza la regularización L2 predeterminada con C=1, solver `lbfgs` y escalado numérico. Se permite un máximo de 2.000 iteraciones para converger. El árbol y el bosque mantienen profundidad máxima no limitada y mínimo una observación por hoja; Random Forest utiliza sus 100 árboles predeterminados y selección de atributos por raíz cuadrada. Se fija semilla 42 en ambos estimadores y no se escalan sus cantidades. Son referencias iniciales sin búsqueda de hiperparámetros: limitar su crecimiento se estudiará a partir de su generalización.

### Entrenamiento y validación comunes

La [rutina de evaluación](../src/evaluacion.py) clona y ajusta cada candidato en cada fold. Imputación, codificación, escalado y pesos de clase se aprenden exclusivamente con ese entrenamiento. Se realizan 25 ajustes y se guarda una predicción de validación por cliente y candidato, comprobando cobertura, alineación e identificadores separados. Las plantillas permanecen sin ajustar; no se selecciona el modelo de un fold ni se reajusta todavía con todo desarrollo.

### Resultados y estabilidad

Las métricas son medias entre folds. La desviación del F1 es muestral, no un intervalo de confianza. Se registra precisión cero por convenio si un candidato no predice rechazos.

| Candidato | F1 validación | Desv. F1 | Precisión | Recall | ROC-AUC | Accuracy | F1 entrenamiento |
|---|---:|---:|---:|---:|---:|---:|---:|
| Mayoritaria | 0,000 | 0,000 | 0,000 | 0,000 | 0,500 | 0,887 | 0,000 |
| Siempre rechazo | 0,203 | 0,000 | 0,113 | 1,000 | 0,500 | 0,113 | 0,203 |
| Logística | 0,242 | 0,064 | 0,159 | 0,507 | 0,612 | 0,643 | 0,297 |
| Árbol | 0,408 | 0,042 | 0,392 | 0,429 | 0,671 | 0,859 | 0,973 |
| Random Forest | 0,520 | 0,115 | 0,630 | 0,450 | 0,743 | 0,907 | 0,971 |

Los tres modelos superan por F1 medio la referencia de siempre rechazo (0,203). La mayoría obtiene 88,69 % de accuracy sin detectar rechazos, por lo que esa cifra aislada sería insuficiente. El bosque encabeza F1 y ROC-AUC; logística detecta más rechazos, a costa de muchas más falsas alertas.

El F1 del bosque varía de 0,381 a 0,681 entre folds. Su F1 de entrenamiento es 0,971 frente a 0,520 en validación; en el árbol son 0,973 y 0,408. Las brechas justifican estudiar regularización y estabilidad. La logística presenta 0,297 y 0,242: los límites de los candidatos no responden todos al mismo patrón.

### Lectura de los errores

Las predicciones de validación reúnen 1.098 aprobaciones y 140 rechazos, sin que cada cliente haya participado en el entrenamiento que lo evalúa. Logística detecta 71 rechazos y produce 373 falsos rechazos; árbol detecta 60 y produce 94; bosque detecta 63 y produce 38. Quedan sin detectar 69, 80 y 77 rechazos, respectivamente.

El bosque ofrece el mejor equilibrio inicial por F1, pero deja muchos rechazos sin detectar. La logística alcanza mayor recall con más aprobaciones clasificadas como rechazo. No se conocen los costes necesarios para convertir ese intercambio en una decisión bancaria. Las métricas de las matrices agregadas pueden diferir de las medias por fold; ninguna de ellas mide impagos o pérdidas observados.

### Elección provisional y siguientes mejoras

Random Forest queda como candidato provisional. Los demás modelos están a más de 0,01 de su F1 medio, por lo que la preferencia por una familia más sencilla no cambia la elección. Superar las referencias no acredita utilidad para una política de crédito ni superioridad estadística definitiva.

La siguiente fase estudiará ajustes acotados de complejidad y contrastará por separado el P99 del ingreso y la exclusión de `CHILDREN`. Un eventual ajuste de umbral utilizará solo desarrollo. La ponderación ya forma parte de la comparación inicial; no se han ejecutado estas mejoras, reajustado el modelo final ni evaluado test.

Se conservan [configuraciones, métricas por fold y errores agregados](../reports/README.md). El reparto y las configuraciones se han revisado conjuntamente; estos resultados describen el protocolo vigente y no aíslan el efecto causal de cada cambio. El conocimiento previo del conjunto mantiene el alcance de evaluación interna.
