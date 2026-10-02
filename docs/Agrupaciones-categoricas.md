# Agrupaciones categóricas

Las reglas se definen tras revisar el entrenamiento del primer fold. Reducen la fragmentación de categorías por significado, sin utilizar la tasa de rechazo como criterio de fusión. Son una representación inicial cuya utilidad predictiva aún no está validada; no constituyen una clasificación acreditada de riesgo, ingresos o solvencia.

Las correspondencias exactas se muestran en el [notebook](../notebooks/01-analisis-y-modelado.ipynb) y en [agrupaciones_categoricas.csv](../reports/agrupaciones_categoricas.csv). El código reutilizable está en [preparacion.py](../src/preparacion.py).

## Ocupación

| Grupo | Criterio y límite de interpretación | Registros de entrenamiento |
|---|---|---:|
| Administración y gestión | Contabilidad, recursos humanos, dirección y secretaría: funciones de gestión y soporte administrativo. No se supone la misma responsabilidad o remuneración. | 126 |
| Técnicas y profesionales | Personal técnico cualificado, informático y sanitario. Comparten el componente especializado, aunque difieren en sector y actividad. | 73 |
| Producción y transporte | Trabajo operativo, tareas manuales y conducción. No implica igual cualificación o estabilidad contractual. | 228 |
| Ventas | Personal comercial y agentes inmobiliarios. Se agrupan por su actividad de venta, no por el valor de sus operaciones. | 84 |
| Servicios de apoyo | Limpieza, cocina, servicio privado, seguridad y atención en restauración. Es una familia amplia de servicios; se pierde detalle del sector. | 55 |
| Personal general | Se conserva `Core staff` separado porque su denominación es imprecisa y tiene respaldo suficiente para no forzar una interpretación. | 119 |

Las 18 ocupaciones informadas se representan en seis grupos. Los 305 registros sin ocupación conservan `__AUSENTE__`; el indicador del código positivo de empleo permite distinguir 159 de esos registros de los otros 146. No se asigna una profesión ni se identifica automáticamente a todos como desempleados.

## Educación

- **Superior completa (261):** `Academic degree` y `Higher education`. Comparten formación superior completada, aunque se pierde el detalle del grado.
- **Superior incompleta (41):** se mantiene separada para conservar la diferencia entre estudios iniciados y completados.
- **Secundaria (688):** reúne `Lower secondary` y `Secondary / secondary special`. La agrupación conserva una familia educativa amplia, pero pierde diferencias de nivel y especialización.

Se usa codificación nominal. Las agrupaciones no introducen una escala numérica de riesgo ni obligan a que la relación con el rechazo sea creciente o decreciente.

## Vivienda

- **Casa o apartamento (884):** conserva la denominación original; no confirma propiedad.
- **Con familiares (53):** conserva `With parents`; no permite inferir alquiler ni dependencia económica.
- **Alquiler declarado (12):** se mantiene separado porque su significado es explícito.
- **Institucional o colectiva (41):** reúne vivienda municipal, vinculada al trabajo y cooperativa. El vínculo público, laboral o colectivo justifica una categoría amplia, aunque las condiciones de tenencia y financiación sean distintas.

La última agrupación es una simplificación con incertidumbre semántica, que podrá revisarse si pierde información útil. No se denomina alquiler a modalidades cuyo régimen de tenencia no está acreditado. Tampoco se impone un tamaño mínimo común: las doce observaciones de alquiler conservan su categoría.

## Ausencias, niveles nuevos y comparación pendiente

Una categoría ausente se representa como `__AUSENTE__`. En las variables agrupadas, un valor informado que no figure en el diccionario se marca como `__NO_RECONOCIDA__`; no se confunde con una ausencia. El codificador ignora niveles no aprendidos, dejándolos con ceros en el bloque correspondiente. Se verifica este comportamiento mediante un ejemplo sintético de ocupación nueva.

Las frecuencias completas están en el [resumen original](../reports/resumen_categorias_entrenamiento.csv) y el [resumen agrupado](../reports/resumen_agrupaciones_entrenamiento.csv). Las coincidencias que pueda crear esta simplificación no demuestran que los registros originales fueran duplicados. Se mantienen las particiones originales por perfiles; no se reagrupan muestras después de transformar.

La comparación predictiva posterior deberá valorar el intercambio entre menor fragmentación y pérdida de detalle. Los tamaños o tasas descriptivas de estos grupos no demuestran por sí solos una mejora del modelo.
