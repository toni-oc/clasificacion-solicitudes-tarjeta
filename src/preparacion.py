"""Reglas de preparación y transformaciones opcionales del modelo."""

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class LimitarExtremos(TransformerMixin, BaseEstimator):
    """Aprende límites de ingreso y familia; conserva filas y ausencias."""

    def __init__(self, cuantil=0.99):
        self.cuantil = cuantil

    def fit(self, X, y=None):
        if not 0 < self.cuantil <= 1:
            raise ValueError("El cuantil debe estar entre 0 y 1, excluido 0.")
        self.limites_ = X[["Annual_income", "Family_Members"]].quantile(self.cuantil)
        # Un tamaño familiar discreto se limita a un valor observado, sin fracciones.
        self.limites_["Family_Members"] = X["Family_Members"].quantile(
            self.cuantil, interpolation="higher",
        )
        if self.limites_.isna().any():
            raise ValueError("Faltan valores informados para aprender los límites.")
        return self

    def transform(self, X):
        check_is_fitted(self, "limites_")
        salida = X.copy()
        columnas = self.limites_.index
        salida[columnas] = salida[columnas].clip(upper=self.limites_, axis="columns")
        return salida


def transformar_ingreso_log(X):
    """Sustituye la representación del ingreso por log(1 + ingreso), sin imputar."""
    if X["Annual_income"].dropna().lt(0).any():
        raise ValueError("La transformación requiere ingresos no negativos.")
    salida = X.copy()
    salida["Annual_income"] = np.log1p(salida["Annual_income"])
    return salida


NUMERICAS = ["Annual_income", "CHILDREN", "Family_Members", "Edad_anios", "Antiguedad_anios"]
CATEGORICAS = [
    "GENDER", "Car_Owner", "Propert_Owner", "Type_Income", "EDUCATION",
    "Marital_status", "Housing_type", "Type_Occupation",
]
BINARIAS = ["Work_Phone", "Phone", "EMAIL_ID", "Codigo_empleo_positivo", "Ingreso_ausente"]

# Se conservan niveles amplios o ambiguos que no requieren una fusión forzada.
GRUPOS = {
    "Type_Occupation": {
        "Administracion_y_gestion": ["Accountants", "HR staff", "Managers", "Secretaries"],
        "Tecnicas_y_profesionales": ["High skill tech staff", "IT staff", "Medicine staff"],
        "Produccion_y_transporte": ["Laborers", "Low-skill Laborers", "Drivers"],
        "Ventas": ["Sales staff", "Realty agents"],
        "Servicios_de_apoyo": [
            "Cleaning staff", "Cooking staff", "Private service staff", "Security staff",
            "Waiters/barmen staff",
        ],
        "Personal_general": ["Core staff"],
    },
    "EDUCATION": {
        "Superior_completa": ["Academic degree", "Higher education"],
        "Superior_incompleta": ["Incomplete higher"],
        "Secundaria": ["Lower secondary", "Secondary / secondary special"],
    },
    "Housing_type": {
        "Casa_o_apartamento": ["House / apartment"],
        "Con_familiares": ["With parents"],
        "Alquiler_declarado": ["Rented apartment"],
        "Institucional_o_colectiva": ["Municipal apartment", "Office apartment", "Co-op apartment"],
    },
}
MAPEOS = {
    campo: {nivel: grupo for grupo, niveles in grupos.items() for nivel in niveles}
    for campo, grupos in GRUPOS.items()
}


def representar_variables(X):
    """Convierte días relativos en años sin atribuir duración al código positivo."""
    salida = X.copy()
    salida["Edad_anios"] = -salida.pop("Birthday_count") / 365.25
    dias_empleo = salida.pop("Employed_days")
    salida["Codigo_empleo_positivo"] = dias_empleo.gt(0).astype(int)
    salida["Antiguedad_anios"] = -dias_empleo.where(dias_empleo.le(0)) / 365.25
    salida["Ingreso_ausente"] = salida["Annual_income"].isna().astype(int)
    return salida


def agrupar_categorias(X):
    """Agrupa niveles informados y conserva las ausencias para tratarlas después."""
    salida = X.copy()
    for campo, mapeo in MAPEOS.items():
        originales = salida[campo]
        agrupados = originales.map(mapeo)
        salida[campo] = agrupados.mask(originales.notna() & agrupados.isna(), "__NO_RECONOCIDA__")
    return salida


def aplicar_reglas(X):
    """Agrupa y representa ausencias y códigos sin estadísticas del conjunto."""
    salida = agrupar_categorias(X)
    for campo in CATEGORICAS:
        salida[campo] = salida[campo].fillna("__AUSENTE__").astype(str)

    # Cero es soporte de cálculo, no experiencia laboral conocida; el indicador lo distingue.
    especial = salida["Codigo_empleo_positivo"].eq(1)
    salida.loc[especial, "Antiguedad_anios"] = 0.0
    # Deja las otras ausencias numéricas compatibles con el imputador del pipeline.
    salida[NUMERICAS] = salida[NUMERICAS].astype(float)
    return salida
