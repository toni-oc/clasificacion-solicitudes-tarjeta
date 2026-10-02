# Diseño de evaluación

La [configuración](configuracion.json) fija fuentes, orden, semillas, grupos y reglas de comparación. El [notebook](../notebooks/01-analisis-y-modelado.ipynb) reproduce las particiones con los CSV originales y las versiones de [requirements.txt](../requirements.txt), sin necesitar archivos del curso.

Se conserva el orden de `Ind_ID` en `Credit_card.csv`. Los grupos se forman con los 17 atributos originales, sin identificador ni etiqueta, incluyendo las ausencias como coincidencias. `StratifiedGroupKFold` reserva el primer bloque de cinco para test (semilla 42) y crea cinco folds de desarrollo (semilla 43). La estratificación intenta mantener el reparto de clases sin romper perfiles; los tamaños pueden diferir ligeramente.

| Archivo | Contenido |
|---|---|
| [configuracion.json](configuracion.json) | Definición reproducible del reparto y criterios fijados antes de modelar. |
| [resumen_muestras.csv](resumen_muestras.csv) | Tamaños, perfiles y distribución de la etiqueta en desarrollo y test. |
| [resumen_folds.csv](resumen_folds.csv) | Tamaños y rechazos en entrenamiento y validación de cada fold. |
| `particiones.csv` | Asignación individual generada localmente; excluida de Git por contener identificadores. |

La asignación individual registra `Ind_ID`, `grupo_perfil`, `uso`, `orden_en_uso` y `fold_validacion`. El fold 0 identifica el test; en desarrollo, 1–5 indican cuándo valida cada registro. El entrenamiento de cada fold contiene los demás registros de desarrollo. Si el archivo ya existe, el notebook comprueba su coincidencia antes de continuar, sin sobrescribir un reparto distinto.

La primera exploración se limita al entrenamiento del primer fold. Las decisiones manuales derivadas de esa exploración pueden influir en la validación de desarrollo; ajustar las transformaciones dentro de cada fold no elimina esa adaptación. Además, estos datos públicos ya se han examinado. La reserva de cierre es una evaluación interna y no acredita rendimiento futuro en otro banco, periodo o población.
