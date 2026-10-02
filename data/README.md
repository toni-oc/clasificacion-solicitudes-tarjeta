# Datos

Descargar `Credit_card.csv` y `Credit_card_label.csv` desde [Credit card Details Binary Classification Problem, en Kaggle](https://www.kaggle.com/datasets/rohitudageri/credit-card-details), publicado por Rohit Udageri. Crear `data/raw/` y colocar allí ambos archivos, conservando esos nombres.

| Archivo | Contenido |
|---|---|
| `raw/Credit_card.csv` | Identificador y atributos del solicitante. |
| `raw/Credit_card_label.csv` | Identificador y decisión histórica: 0 = aprobación; 1 = rechazo. |

La fuente define `Ind_ID` como identificador de cliente (`Client ID`). Hay 1.548 identificadores únicos: se trabaja con una observación por cliente identificado. El notebook une las tablas por esa clave, comprueba una relación uno a uno y detiene el recorrido si encuentra claves ausentes, repetidas o sin correspondencia. El [diccionario](../docs/Diccionario-datos.md) detalla los campos.

El [inventario](inventario_fuentes.json) conserva tamaños y SHA-256 de los archivos utilizados. Permite identificar la descarga de referencia; una descarga distinta requiere revisar sus diferencias antes de comparar resultados. Los originales se mantienen intactos y los CSV de esta carpeta están excluidos de Git. El notebook conserva una vista acotada de atributos sin mostrar `Ind_ID`, además de resúmenes agregados.

## Procedencia y límites

Consulta de la [API pública de Kaggle](https://www.kaggle.com/api/v1/datasets/view/rohitudageri/credit-card-details): **2 de octubre de 2026**. La ficha declara `CC0: Public Domain` y versión publicada **1**. La fecha de descarga original no se conoce; la versión declarada por la ficha no prueba por sí sola la versión histórica de los bytes utilizados.

La declaración de licencia corresponde al publicador. No acredita origen bancario, representatividad, consentimiento ni calidad de las decisiones registradas; tampoco se extiende al código o al material del curso. El repositorio no redistribuye los CSV completos.

No se conocen el periodo de las observaciones, la moneda del ingreso, la política de aprobación ni el momento exacto en que se registró cada atributo. `label` no contiene un resultado observado de impago. Estas limitaciones se mantienen al interpretar modelos y errores.
