# Memoria del proyecto: clasificación de solicitudes de tarjeta

## Objetivo y datos

### Planteamiento

El proyecto estudia la clasificación de solicitudes de tarjeta a partir de atributos personales, laborales y financieros. El contexto de admisión de crédito exige considerar tanto las solicitudes problemáticas aceptadas como las solicitudes adecuadas rechazadas. Sin embargo, los datos disponibles identifican aprobación y rechazo históricos, no impago observado. Por ello, la tarea técnica se limita a clasificar `label`, con el rechazo como clase positiva, sin equiparar una decisión histórica a una medida de solvencia.

El criterio de comparación es F1, acompañado de recall, precisión, ROC-AUC y matrices de confusión. La elección concreta se apoyará también en estabilidad y explicabilidad. Los costes de error, la capacidad de revisión y una mejora mínima útil no están acreditados. El diseño de evaluación descrito más adelante se fija antes de entrenar modelos; sus resultados tendrán alcance interno sobre un conjunto público ya examinado.

### Fuentes y carga

La sección **Fuentes y carga** importa las dos tablas de Kaggle y muestra sus dimensiones. `Credit_card.csv` aporta 1.548 registros y 18 columnas; `Credit_card_label.csv`, 1.548 registros y 2 columnas. La clave `Ind_ID` se lee como texto para utilizarla como identificador. Que ambas tablas tengan el mismo número de filas no garantiza que sus claves coincidan; por eso se comprueba su correspondencia antes de analizar los registros conjuntos. Los archivos originales se conservan sin cambios y su procedencia se recoge en el [inventario](../data/inventario_fuentes.json).

### Correspondencia entre tablas

En **Correspondencia entre tablas** se comprueba que las claves estén informadas y sean únicas en cada archivo. La unión externa validada uno a uno permite detectar tanto pérdidas como multiplicaciones de filas. Los 1.548 identificadores tienen correspondencia en ambas tablas; no quedan claves exclusivas de una fuente. El resultado contiene 19 columnas: identificador, 17 atributos candidatos y etiqueta. La unicidad de la clave no demuestra que todos los registros correspondan a personas diferentes. La vista de las cinco primeras filas de la tabla unida muestra atributos y etiqueta juntos, sin exponer el identificador.

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

No se eliminan filas ni se sustituyen etiquetas: una coincidencia completa no confirma identidad personal ni demuestra qué decisión sería errónea. Las diferencias podrían depender de información ausente, de cambios no fechados o de errores cuya causa no se puede establecer. Como medida conservadora, todas las filas de un perfil permanecen juntas al separar muestras. Esto evita compartir perfiles exactos entre entrenamiento y evaluación, pero no identifica personas con atributos distintos.

### Campos para modelar

Se excluye `Mobile_phone` por constancia y quedan 16 atributos candidatos. Se conservan los 1.548 registros. `Ind_ID` mantiene la alineación entre entradas y respuesta; el grupo de perfil solo controla el reparto. Ninguno entra como predictor. Los datos originales y la definición del perfil conservan el móvil.

La disponibilidad temporal y la pertinencia de los demás campos siguen pendientes de acreditación. Mantenerlos como candidatos no significa que se haya decidido una selección definitiva ni que su uso sea adecuado para una política real de crédito.

### Reglas de evaluación

Se fija F1 medio no ponderado entre cinco folds como criterio principal, con rechazo como clase positiva y umbral inicial 0,5. Se acompañará de dispersión entre folds, recall, precisión, ROC-AUC con puntuaciones y matrices de confusión. Las referencias serán predecir la clase mayoritaria del entrenamiento y predecir siempre rechazo; todavía no se han evaluado.

Dentro de 0,01 de F1 del mejor resultado se priorizarán logística, árbol y bosque, en ese orden. Dentro de una familia se preferirá menor dispersión y después mayor F1 medio. Es una regla práctica para limitar complejidad ante diferencias pequeñas, no una prueba de equivalencia estadística ni un coste de negocio. El ajuste de umbral, si se desarrolla, utilizará únicamente datos de desarrollo.

### Reserva y validación por perfiles

Se utiliza validación cruzada estratificada por grupos. Primero se reserva un bloque de cinco como test, con semilla 42; después se crean cinco folds en desarrollo, con semilla 43. Se mantiene el orden de la fuente para que la reproducción no dependa del orden resultante de la unión de tablas.

El reparto contiene 1.238 registros y 1.102 perfiles en desarrollo, con 140 rechazos; el test contiene 310 registros y 275 perfiles, con 35 rechazos. Cada validación tiene 247 o 248 registros y 28 rechazos. Se comprueba que los grupos no se compartan entre muestras, que cada registro de desarrollo valide una sola vez y que todos los entrenamientos y validaciones contengan ambas clases.

La exploración siguiente utilizará los 990 registros del entrenamiento del primer fold, con 112 rechazos. Los tratamientos aprendidos se ajustarán de nuevo en cada entrenamiento al comparar candidatos. Las decisiones manuales que nazcan del análisis exploratorio pueden influir en la validación de desarrollo; un pipeline no convierte esa validación en una comprobación externa.

### Conservación de las particiones y alcance

El [registro de evaluación](../evaluacion/README.md) conserva configuración, huellas de las fuentes y resúmenes agregados. La asignación por identificador, uso y fold se genera localmente y se comprueba en las ejecuciones posteriores para impedir un cambio inadvertido del reparto.

El conjunto público ya ha sido examinado, por lo que los resultados futuros tendrán alcance de evaluación interna. No hay cronología para simular predicciones futuras, identidades personales verificadas ni una muestra externa. El número reducido de rechazos también limita la precisión con la que podrán interpretarse diferencias pequeñas.

El bloque deja definidos los controles de calidad y el diseño de comparación, antes de aprender tratamientos o entrenar modelos. La siguiente sección explora entrenamiento y justifica la preparación numérica y las agrupaciones categóricas por su significado.

## Exploración y preparación

### Variables y representaciones para explorar

La exploración utiliza los 990 registros del entrenamiento del primer fold, con 112 rechazos. Las muestras originales y sus asignaciones permanecen intactas. Los días de nacimiento y empleo se convierten en años aproximados, dividiendo por 365,25 y respetando la referencia temporal del archivo; no se utiliza la fecha de ejecución.

Se distinguen cinco cantidades, ocho categorías nominales y los indicadores binarios. El código positivo de empleo se separa en un indicador: sus 159 registros no aportan una duración laboral interpretable y quedan fuera de los gráficos de antigüedad. Las representaciones se calculan en copias mediante funciones que no utilizan la respuesta.

### Distribuciones, extremos y relaciones numéricas

Los histogramas y frecuencias muestran un ingreso con cola derecha, edades entre 21,10 y 67,52 años y concentraciones en hogares pequeños. El límite exploratorio IQR del ingreso es 380.925; hay 50 registros por encima y el máximo alcanza 1.575.000. Un registro tiene 14 hijos y 15 miembros de familia. Se revisan ejemplos junto a su contexto, sin encontrar evidencia que permita declararlos errores. La preparación inicial conserva esos valores; el límite IQR no se aplica como recorte.

La antigüedad mediana interpretable es 5,74 años en aprobaciones y 3,18 en rechazos, con solapamiento entre clases. El gráfico de ingresos por etiqueta utiliza una escala logarítmica solo para visualizar; la entrada no se transforma. La correlación de Spearman entre hijos y miembros de familia es 0,823. Se conservan ambas cantidades inicialmente: compartir información no demuestra que una sea prescindible para todos los modelos.

Estas asociaciones describen decisiones históricas en entrenamiento. No prueban causalidad ni anticipan la utilidad predictiva de una transformación. Los recortes, logaritmos o reducciones de entradas siguen siendo posibles mejoras por contrastar.

### Categorías y agrupaciones con significado

Se calculan frecuencias, número de rechazos y tasas para todas las categorías y los tres indicadores de contacto. Los gráficos se centran en ocupación, educación y vivienda; el [resumen completo](../reports/resumen_categorias_entrenamiento.csv) conserva los demás niveles. La tasa del 100 % de `IT staff` procede de solo dos registros, lo que ilustra el escaso respaldo de algunas categorías.

Se adoptan agrupaciones semánticas, sin utilizar las tasas para decidir las fusiones. Ocupación pasa de 18 niveles informados a seis familias: administración y gestión (126), técnicas y profesionales (73), producción y transporte (228), ventas (84), servicios de apoyo (55) y personal general (119). `Core staff` se mantiene separado por su significado impreciso. Las familias no suponen equivalencia salarial ni una jerarquía de solvencia.

Educación pasa de cinco niveles a secundaria (688), superior completa (261) y superior incompleta (41). Se preserva la diferencia entre estudios superiores completados e incompletos, aunque se pierde detalle dentro de secundaria y entre grados superiores. La codificación posterior es nominal, sin imponer una relación de riesgo ordenada.

Vivienda pasa de seis niveles a casa o apartamento (884), con familiares (53), alquiler declarado (12) e institucional o colectiva (41). Esta última categoría reúne vivienda municipal, vinculada al trabajo y cooperativa; es una simplificación amplia cuya utilidad sigue pendiente de validación. No se interpreta toda modalidad minoritaria como alquiler ni casa/apartamento como propiedad. Las doce observaciones de alquiler permanecen separadas porque su significado es explícito.

Las [correspondencias y justificaciones](Agrupaciones-categoricas.md) documentan también la información que se pierde. El estado civil, el tipo de ingreso, las tenencias y los contactos se conservan. Las tasas similares de los teléfonos en esta exploración no bastan por sí solas para descartar una posible contribución conjunta. Agrupar reduce fragmentación; todavía no demuestra una mejora predictiva.

### Ausencias y decisiones de tratamiento

En entrenamiento faltan dos géneros, 18 ingresos, 16 nacimientos y 305 ocupaciones. Entre los ingresos ausentes hay siete rechazos (38,89 %), frente al 10,80 % entre los informados. Se incorpora un indicador de ausencia como hipótesis de representación, sin atribuir ocultación ni considerar demostrada su utilidad con tan pocos registros.

Ingreso y edad se imputan con medianas de entrenamiento: 162.000 y 42,401 años, respectivamente. La mediana evita que los ingresos extremos desplacen el valor de referencia; no supone que las cantidades desconocidas sean cero o pertenezcan al cuartil inferior. En esta muestra no se necesitan imputaciones de hijos ni miembros de familia.

Las categorías desconocidas se representan con `__AUSENTE__`, sin asignar una profesión o género supuestos. De las 305 ocupaciones ausentes, 159 acompañan al código positivo de empleo y 146 no. El indicador de ese código permite distinguir ambos contextos aun compartiendo la categoría de ausencia.

Para los 159 códigos especiales se utiliza una duración cero de soporte, acompañada del indicador. Ese cero permite el cálculo del modelo y no se presenta como antigüedad observada ni experiencia laboral total. Una duración desconocida sin ese código recibiría la mediana del entrenamiento; este segundo caso no aparece entre las ausencias actuales.

### Preparación reutilizable

El pipeline conecta representaciones, reglas fijas, imputación, codificación y escalado. Las funciones y correspondencias están en [preparacion.py](../src/preparacion.py); la construcción del pipeline permanece visible en el notebook. Las categorías se codifican con one-hot y los cinco indicadores binarios permanecen en 0/1. El escalado numérico queda preparado para logística y se podrá desactivar para árboles.

El ajuste realizado es un diagnóstico sobre el primer entrenamiento. Al comparar modelos se ajustará una copia nueva del pipeline en cada fold; no se enviará a validación una tabla preparada previamente con todo desarrollo. Las decisiones manuales del análisis exploratorio siguen formando parte del desarrollo y no convierten sus puntuaciones en una evaluación externa.

### Comprobación del resultado y cierre

La preparación produce 40 columnas numéricas y conserva las 990 filas con sus índices alineados. Se imputan los 18 ingresos y las 16 edades; los valores numéricos informados permanecen intactos antes del escalado, salvo la conversión de unidades y el tratamiento explícito del código de empleo. Los gráficos antes y después permiten observar el efecto de la imputación sin confundir los valores añadidos con observaciones reales.

Un ejemplo sintético combina una ocupación nueva con ingreso ausente. La preparación mantiene las columnas, activa el indicador de ausencia y codifica la ocupación desconocida con ceros en su bloque, sin reajustar estadísticas. Los [resúmenes de entrenamiento](../reports/README.md) conservan agrupaciones y medianas.

No se modifican las particiones tras agrupar: coincidencias creadas por la simplificación no demuestran duplicidad de los registros originales. Las agrupaciones y el indicador de ingreso quedan implementados como preparación inicial, con su aportación predictiva pendiente de contraste. El siguiente bloque evaluará las referencias y los modelos sobre las particiones acordadas.
