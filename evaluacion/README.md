# Diseño de evaluación

La [configuración](configuracion.json) fija fuentes, orden, semillas y reglas de comparación. El [notebook](../notebooks/clasificacion-solicitudes-tarjeta.ipynb) reproduce las particiones con los CSV originales y las versiones de [requirements.txt](../requirements.txt), sin necesitar archivos del curso.

## Unidad y reparto

La fuente define `Ind_ID` como identificador de cliente y sus 1.548 valores son únicos. Se adopta una fila por cliente identificado. Los perfiles coincidentes tienen claves diferentes: se conservan como diagnóstico, sin forzarlos a permanecer en una misma muestra. Esta interpretación sigue la documentación; no demuestra independencia estadística completa ni verifica externamente identidades o el proceso de construcción del conjunto.

Si hubiera varias observaciones del mismo cliente, habría que estudiar su dependencia y separar por cliente para evaluar clientes nuevos. Separar por una combinación de atributos impondría otra condición: evaluar únicamente perfiles exactos no vistos. Esa restricción no es el objetivo de este reparto.

Se conserva el orden de `Ind_ID` en `Credit_card.csv`. `train_test_split` reserva el 20 % de las filas para test, con `stratify=y` y semilla 42; después `StratifiedKFold` crea cinco folds de desarrollo con mezcla aleatoria y semilla 43. Se mantiene el orden devuelto por el primer reparto. No se seleccionan semillas por las métricas obtenidas.

Hay 1.238 clientes identificados en desarrollo y 310 en test, con 140 y 35 rechazos. Cada validación contiene 247 o 248 registros y 28 rechazos; el entrenamiento correspondiente contiene 990 o 991 registros y 112 rechazos. Los identificadores no se solapan entre muestras, aunque pueden coincidir perfiles de atributos. La estratificación mantiene aproximadamente la frecuencia de clases, sin duplicar ni eliminar observaciones.

## Archivos y comprobaciones

| Archivo | Contenido |
|---|---|
| [configuracion.json](configuracion.json) | Método, semillas, unidad de reparto y criterios de comparación. |
| [resumen_muestras.csv](resumen_muestras.csv) | Tamaños, perfiles descriptivos y distribución de la etiqueta en desarrollo y test. |
| [resumen_folds.csv](resumen_folds.csv) | Tamaños y rechazos en entrenamiento y validación de cada fold. |
| `particiones.csv` | Asignación individual generada localmente; excluida de Git por contener identificadores. |

La asignación registra `Ind_ID`, `grupo_perfil`, `uso`, `orden_en_uso` y `fold_validacion`. `grupo_perfil` es descriptivo y no gobierna el reparto. El fold 0 identifica test; en desarrollo, 1–5 indican cuándo valida cada registro. El entrenamiento de cada fold contiene los demás registros de desarrollo. Si el archivo ya existe, el notebook comprueba su coincidencia, sin sobrescribir un reparto distinto.

Todos los candidatos utilizan las mismas particiones. Las estadísticas de preparación y los pesos `balanced` se aprenden únicamente en el entrenamiento de cada fold. La ponderación afecta al ajuste de los modelos, no al cálculo de las métricas ni a la distribución de validación. Cada cliente de desarrollo recibe una predicción de validación por candidato.

## Alcance

La exploración detallada utiliza el entrenamiento del primer fold. Las decisiones manuales derivadas de ella pueden influir en la validación de desarrollo; un pipeline no elimina esa adaptación.

El protocolo se revisó después de explorar el conjunto y comparar configuraciones. El nuevo reparto puede reservar registros ya utilizados en análisis anteriores: reajustar los modelos desde cero evita reutilizar sus ajustes, pero no borra el conocimiento previo del conjunto. El test se ha evaluado después de fijar la propuesta y reajustar únicamente con desarrollo. Sus resultados y la decisión previa se conservan en los [informes de cierre](../reports/README.md). Sigue siendo una evaluación interna tras revisar el protocolo, no una comprobación completamente inédita, externa o temporal.

Los tamaños y la estratificación no acreditan representatividad de otro banco, periodo o población. La falta de fechas, del método de muestreo y de una política documentada de aprobación permanece como limitación.
