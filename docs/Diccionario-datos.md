# Diccionario de datos

Definiciones resumidas de la [fuente de Kaggle](https://www.kaggle.com/datasets/rohitudageri/credit-card-details), contrastadas con las cabeceras de los CSV. Los nombres conservan la escritura original. El tipo leído por pandas no determina por sí solo el tipo conceptual ni el tratamiento.

| Campo | Significado y unidad o dominio | Papel inicial |
|---|---|---|
| `Ind_ID` | Identificador de cliente según la fuente; no acredita identidad única de una persona. | Unión y control; excluido como predictor. |
| `GENDER` | Género registrado; categorías de la fuente. | Candidato sujeto a revisión de pertinencia. |
| `Car_Owner` | Tenencia de automóvil. | Categoría candidata. |
| `Propert_Owner` | Tenencia de propiedad. | Categoría candidata. |
| `CHILDREN` | Número de hijos. | Recuento candidato. |
| `Annual_income` | Ingreso anual; moneda no especificada. | Cantidad candidata. |
| `Type_Income` | Tipo o fuente de ingresos. | Categoría candidata. |
| `EDUCATION` | Nivel educativo. | Agrupado en secundaria, superior incompleta y superior completa; codificación nominal. |
| `Marital_status` | Estado civil. | Categoría candidata, sujeta a pertinencia. |
| `Housing_type` | Situación o tipo de vivienda. | Cuatro grupos; no se interpreta casa/apartamento como propiedad ni todas las otras modalidades como alquiler. |
| `Birthday_count` | Días hacia atrás desde una referencia no fechada hasta el nacimiento. | Representado mediante edad aproximada en años. |
| `Employed_days` | Días hacia atrás hasta el inicio del empleo. La fuente interpreta valores positivos como ausencia de empleo actual. | Duración en años y código positivo por separado; cero de soporte para el estado especial, sin afirmar antigüedad observada. |
| `Mobile_phone` | Indicador de disponibilidad de teléfono móvil. | Excluido como predictor: vale 1 en todos los registros, sin ausencias. Se conserva en la fuente y en la definición del perfil. |
| `Work_Phone` | Indicador de disponibilidad de teléfono laboral. | Categoría binaria candidata. |
| `Phone` | Indicador de disponibilidad de teléfono. | Categoría binaria candidata. |
| `EMAIL_ID` | Indicador de disponibilidad de correo electrónico; no es la dirección de correo. | Categoría binaria candidata. |
| `Type_Occupation` | Ocupación registrada. | Seis familias de actividad y ausencia explícita; no implica una jerarquía salarial o de solvencia. |
| `Family_Members` | Número de miembros de la familia. | Recuento candidato. |
| `label` | 0 = aprobación registrada; 1 = rechazo registrado. | Objetivo binario; clase positiva 1. |

De los 17 atributos distintos de la clave y la etiqueta, quedan 16 entradas **candidatas** tras excluir el móvil constante; no son una selección definitiva. Ninguno cuenta con una fecha que acredite su disponibilidad antes de la decisión. Una categoría laboral o educativa no prueba solvencia, y el código positivo de empleo no permite concluir por sí solo la situación económica concreta.

La [preparación inicial](Agrupaciones-categoricas.md) aplica agrupaciones de significado, conversiones a años, categorías ausentes explícitas y medianas aprendidas en entrenamiento. Los extremos se conservan. Su utilidad predictiva y una selección posterior de entradas siguen pendientes de comparación.

## Representaciones derivadas

| Campo | Definición y tratamiento |
|---|---|
| `Edad_anios` | `-Birthday_count / 365.25`; mediana del entrenamiento si falta. No se calcula respecto a la fecha de ejecución. |
| `Antiguedad_anios` | `-Employed_days / 365.25` cuando el valor es no positivo. Para el código positivo, cero de soporte acompañado del indicador; no significa experiencia laboral total igual a cero. Una duración desconocida sin ese código se trataría con la mediana del entrenamiento. |
| `Codigo_empleo_positivo` | 1 si `Employed_days > 0`, 0 en caso contrario. Identifica el código observado, no una condición económica completa. |
| `Ingreso_ausente` | 1 si el ingreso original estaba ausente; se calcula antes de imputar. No implica ocultación ni ingreso cero. |

Los días originales se sustituyen por las representaciones anteriores dentro del pipeline, conservando los CSV y las muestras sin alterar. Antes de codificar quedan cinco cantidades, ocho categorías nominales y cinco indicadores binarios. En el primer entrenamiento generan 40 columnas numéricas, cuyo número puede variar si otros folds aprenden niveles diferentes.
