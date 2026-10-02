"""Comparación binaria en particiones de desarrollo ya fijadas."""

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score


def evaluar_candidatos(candidatos, X, y, particiones, umbral=0.5):
    """Reajusta cada pipeline por fold y devuelve métricas y predicciones de validación.

    Requiere clases 0/1, predict_proba y una validación por registro de desarrollo.
    Los objetos recibidos son plantillas: no se modifican ni se entrega un fold elegido.
    """
    if not X.index.is_unique or not X.index.equals(y.index):
        raise ValueError("Las entradas y etiquetas deben tener índices únicos y alineados.")
    validaciones = np.concatenate([va for _, va in particiones])
    if not np.array_equal(np.sort(validaciones), np.arange(len(X))):
        raise ValueError("Cada registro debe validarse exactamente una vez.")

    resultados, predicciones = [], []
    for nombre, plantilla in candidatos.items():
        for fold, (tr, va) in enumerate(particiones, start=1):
            if np.intersect1d(tr, va).size:
                raise ValueError("Entrenamiento y validación se solapan.")
            ajuste = clone(plantilla).fit(X.iloc[tr], y.iloc[tr])
            if set(ajuste.classes_) != {0, 1}:
                raise ValueError("El entrenamiento debe contener las clases 0 y 1.")
            positiva = list(ajuste.classes_).index(1)
            prob = ajuste.predict_proba(X.iloc[va])[:, positiva]
            if not np.isfinite(prob).all() or ((prob < 0) | (prob > 1)).any():
                raise ValueError("Puntuaciones de validación no válidas.")
            pred = (prob >= umbral).astype(int)
            pred_train = (ajuste.predict_proba(X.iloc[tr])[:, positiva] >= umbral).astype(int)
            real = y.iloc[va]
            resultados.append({
                "Modelo": nombre, "Fold": fold, "N_train": len(tr), "N_valid": len(va),
                "F1_train": f1_score(y.iloc[tr], pred_train, zero_division=0),
                "F1": f1_score(real, pred, zero_division=0),
                "Precision": precision_score(real, pred, zero_division=0),
                "Recall": recall_score(real, pred, zero_division=0),
                "ROC_AUC": roc_auc_score(real, prob),
                "Accuracy": accuracy_score(real, pred),
            })
            predicciones.append(pd.DataFrame({
                "Ind_ID": X.index[va], "Modelo": nombre, "Fold": fold,
                "Real": real.to_numpy(), "Puntuacion_1": prob, "Prediccion": pred,
            }))

    return pd.DataFrame(resultados), pd.concat(predicciones, ignore_index=True)
