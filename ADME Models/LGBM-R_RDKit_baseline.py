"""
LightGBM + RDKit baseline for the repeated-CV comparison.

Pipeline for SMILES -> features -> LightGBM, 
drops into `repeated_cv_metrics(X, y, configs, inner_search=...)` 
X is the array of SMILES strings.
"""

from __future__ import annotations

import warnings

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import VarianceThreshold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

# --------------------------------------------------------------------------- #
# Featurization
# --------------------------------------------------------------------------- #
_FEATURE_CACHE: dict = {}          # (smiles, kind, radius, n_bits) -> np.ndarray
_DESCRIPTOR_NAMES: list | None = None


def _get_descriptor_calculator():
    """Lazily build an RDKit descriptor calculator over the full descriptor list."""
    global _DESCRIPTOR_NAMES
    from rdkit.Chem import Descriptors
    from rdkit.ML.Descriptors.MoleculeDescriptors import MolecularDescriptorCalculator

    if _DESCRIPTOR_NAMES is None:
        _DESCRIPTOR_NAMES = [name for name, _ in Descriptors.descList]
    return MolecularDescriptorCalculator(_DESCRIPTOR_NAMES), _DESCRIPTOR_NAMES


def _morgan_generator(radius: int, n_bits: int):
    """Morgan fingerprint generator using the current RDKit API (with fallback)."""
    try:
        from rdkit.Chem import rdFingerprintGenerator as rfg
        gen = rfg.GetMorganGenerator(radius=radius, fpSize=n_bits)
        return lambda mol: np.array(gen.GetFingerprint(mol), dtype=np.float32)
    except Exception:  # older RDKit
        from rdkit.Chem import AllChem
        from rdkit import DataStructs

        def _fp(mol):
            bv = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
            arr = np.zeros((n_bits,), dtype=np.float32)
            DataStructs.ConvertToNumpyArray(bv, arr)
            return arr

        return _fp


class SmilesToFeatures(BaseEstimator, TransformerMixin):
    """SMILES -> feature matrix (RDKit descriptors, Morgan bits, or both).

    Stateless fit (featurization does not depend on other molecules). Invalid
    SMILES yield NaN descriptor rows / all-zero fingerprint rows and are counted
    in `n_invalid_` after transform; downstream imputation handles the NaNs.
    """

    def __init__(self, kind: str = "descriptors", radius: int = 2, n_bits: int = 2048,
                 cache: bool = True):
        self.kind = kind
        self.radius = radius
        self.n_bits = n_bits
        self.cache = cache

    def fit(self, X, y=None):
        if self.kind not in ("descriptors", "morgan", "both"):
            raise ValueError("kind must be 'descriptors', 'morgan', or 'both'")
        return self

    def _featurize_one(self, smi, calc, n_desc, morgan_fn):
        key = (smi, self.kind, self.radius, self.n_bits)
        if self.cache and key in _FEATURE_CACHE:
            return _FEATURE_CACHE[key], False
        from rdkit import Chem

        mol = Chem.MolFromSmiles(smi) if isinstance(smi, str) else None
        invalid = mol is None
        parts = []
        if self.kind in ("descriptors", "both"):
            if invalid:
                parts.append(np.full(n_desc, np.nan, dtype=np.float32))
            else:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    parts.append(np.asarray(calc.CalcDescriptors(mol), dtype=np.float32))
        if self.kind in ("morgan", "both"):
            parts.append(np.zeros(self.n_bits, np.float32) if invalid else morgan_fn(mol))
        vec = np.concatenate(parts)
        if self.cache:
            _FEATURE_CACHE[key] = vec
        return vec, invalid

    def transform(self, X):
        smiles = np.asarray(X).ravel()
        calc = n_desc = morgan_fn = None
        if self.kind in ("descriptors", "both"):
            calc, names = _get_descriptor_calculator()
            n_desc = len(names)
        if self.kind in ("morgan", "both"):
            morgan_fn = _morgan_generator(self.radius, self.n_bits)

        rows, n_invalid = [], 0
        for smi in smiles:
            vec, invalid = self._featurize_one(smi, calc, n_desc, morgan_fn)
            rows.append(vec)
            n_invalid += int(invalid)
        self.n_invalid_ = n_invalid
        if n_invalid:
            warnings.warn(f"{n_invalid} SMILES could not be parsed by RDKit.")
        return np.vstack(rows)


# --------------------------------------------------------------------------- #
# Numeric preprocessing (fit on train fold only)
# --------------------------------------------------------------------------- #
def _inf_to_nan(X):
    X = np.asarray(X, dtype=np.float64)
    return np.where(np.isfinite(X), X, np.nan)


def _cleaning_steps():
    return [
        ("inf2nan", FunctionTransformer(_inf_to_nan, feature_names_out="one-to-one")),
        ("impute", SimpleImputer(strategy="median")),
        ("varthresh", VarianceThreshold(0.0)),   # drop constant cols (fit on train)
    ]


# --------------------------------------------------------------------------- #
# Baseline + nested-tuning 
# --------------------------------------------------------------------------- #
def make_lgbm_baseline(kind: str = "descriptors", radius: int = 2, n_bits: int = 2048,
                       random_state: int = 0, n_jobs: int = 1, deterministic: bool = True,
                       **lgbm_overrides) -> Pipeline:
    """SMILES -> features -> cleaning -> LightGBM regressor, as a sklearn Pipeline."""
    from lightgbm import LGBMRegressor  # lazy: keep module importable without lightgbm

    params = dict(
        objective="regression_l1",     # optimize MAE directly (matches your metric)
        n_estimators=600,
        learning_rate=0.03,
        num_leaves=31,
        min_child_samples=20,
        subsample=0.8,
        subsample_freq=1,              # subsample only bites when freq > 0
        colsample_bytree=0.8,
        reg_lambda=1.0,
        random_state=random_state,
        n_jobs=n_jobs,
        deterministic=deterministic,
        force_col_wise=True,           # required alongside deterministic
        verbosity=-1,
    )
    params.update(lgbm_overrides)

    steps = [("featurizer", SmilesToFeatures(kind=kind, radius=radius, n_bits=n_bits))]
    steps += _cleaning_steps()
    steps += [("model", LGBMRegressor(**params))]
    return Pipeline(steps)


def default_lgbm_param_distributions() -> dict:
    """Search space for the nested inner tuning. Keys target the 'model' step."""
    from scipy.stats import randint, uniform, loguniform

    return {
        "model__num_leaves": randint(15, 128),
        "model__min_child_samples": randint(5, 60),
        "model__learning_rate": loguniform(5e-3, 2e-1),
        "model__n_estimators": randint(300, 1200),
        "model__subsample": uniform(0.6, 0.4),          # 0.6..1.0
        "model__colsample_bytree": uniform(0.6, 0.4),
        "model__reg_lambda": loguniform(1e-2, 1e2),
    }


def build_inner_search(kind: str = "descriptors", param_distributions: dict | None = None,
                       n_iter: int = 30, cv: int = 3, random_state: int = 0,
                       scoring: str = "neg_mean_absolute_error", n_jobs: int = 1):
    """Return an `inner_search(estimator, X_tr, y_tr) -> fitted best estimator`."""
    from sklearn.model_selection import KFold, RandomizedSearchCV

    dists = param_distributions or default_lgbm_param_distributions()

    def _search(estimator, X_tr, y_tr):
        base = estimator if estimator is not None else make_lgbm_baseline(kind, random_state=random_state)
        rs = RandomizedSearchCV(
            base, dists, n_iter=n_iter,
            cv=KFold(n_splits=cv, shuffle=True, random_state=random_state),
            scoring=scoring, n_jobs=n_jobs, random_state=random_state, refit=True,
        )
        rs.fit(X_tr, y_tr)
        return rs.best_estimator_

    return _search
