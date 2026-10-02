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
| `EDUCATION` | Nivel educativo. | Categoría con orden conceptual; agrupación pendiente. |
| `Marital_status` | Estado civil. | Categoría candidata, sujeta a pertinencia. |
| `Housing_type` | Situación o tipo de vivienda. | Categoría candidata. |
| `Birthday_count` | Días hacia atrás desde una referencia no fechada hasta el nacimiento. | Candidato para representar edad; transformación pendiente. |
| `Employed_days` | Días hacia atrás hasta el inicio del empleo. La fuente interpreta valores positivos como ausencia de empleo actual. | Revisar códigos y contexto; no tratar automáticamente los positivos como antigüedad. |
| `Mobile_phone` | Indicador de disponibilidad de teléfono móvil. | Excluido como predictor: vale 1 en todos los registros, sin ausencias. Se conserva en la fuente y en la definición del perfil. |
| `Work_Phone` | Indicador de disponibilidad de teléfono laboral. | Categoría binaria candidata. |
| `Phone` | Indicador de disponibilidad de teléfono. | Categoría binaria candidata. |
| `EMAIL_ID` | Indicador de disponibilidad de correo electrónico; no es la dirección de correo. | Categoría binaria candidata. |
| `Type_Occupation` | Ocupación registrada. | Categoría candidata; revisar ausencias y agrupaciones semánticas. |
| `Family_Members` | Número de miembros de la familia. | Recuento candidato. |
| `label` | 0 = aprobación registrada; 1 = rechazo registrado. | Objetivo binario; clase positiva 1. |

De los 17 atributos distintos de la clave y la etiqueta, quedan 16 entradas **candidatas** tras excluir el móvil constante; no son una selección definitiva. Ninguno cuenta con una fecha que acredite su disponibilidad antes de la decisión. Una categoría laboral o educativa no prueba solvencia, y el código positivo de empleo no permite concluir por sí solo la situación económica concreta.

Las agrupaciones se definirán tras explorar el entrenamiento, conservando significados compatibles y separando desconocimiento de situaciones conocidas. No se han aplicado todavía agrupaciones, imputaciones, conversiones de unidades ni recortes.
