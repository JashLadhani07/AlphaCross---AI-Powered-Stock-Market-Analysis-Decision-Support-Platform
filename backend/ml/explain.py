"""
Explainable AI for AlphaCross's XGBoost crossover predictions.

Trains a lightweight XGBoost classifier on the stock's recent feature
history (same features as ml/model_xgb.py) and uses SHAP TreeExplainer
to attribute the latest prediction to its top contributing factors.

Returns None (never raises) if SHAP/XGBoost fail or data is insufficient,
so callers can degrade gracefully and keep serving the base prediction.
"""

from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

FEATURE_COLS = [
    "EMA_20",
    "EMA_50",
    "EMA_20_slope",
    "EMA_50_slope",
    "RSI",
    "Returns",
    "Volatility",
]

# Human-readable labels for the UI ("Explainable AI" panel)
FEATURE_LABELS = {
    "EMA_20": "EMA 20 level",
    "EMA_50": "EMA 50 level",
    "EMA_20_slope": "EMA 20 momentum (slope)",
    "EMA_50_slope": "EMA 50 momentum (slope)",
    "RSI": "RSI momentum",
    "Returns": "Recent daily returns",
    "Volatility": "Recent volatility",
}


def predict_with_explanation(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """
    Train on `df` (already run through ml.features.calculate_features)
    and explain the latest row's prediction with SHAP.

    Returns:
        {
          "prediction": "BULLISH" | "BEARISH" | "NEUTRAL",
          "confidence": float (0-1),
          "top_factors": [
              {"feature": str, "impact": float, "direction": "positive"|"negative"},
              ...
          ]
        }
        or None if explanation isn't possible (caller should fall back
        to the base rule-based prediction with no explainability panel).
    """
    try:
        import shap  # local import - optional dependency
    except ImportError:
        print("[explain] shap not installed; skipping explainability")
        return None

    if df is None or len(df) < 30:
        return None

    try:
        X = df[FEATURE_COLS].iloc[:-1].values
        y = df["Signal"].iloc[:-1].values  # -1 / 0 / 1, robust vs sparse Target

        unique_classes = np.unique(y)
        if len(unique_classes) < 2:
            return None

        unique_classes = np.unique(y)
        if np.array_equal(unique_classes, [-1, 1]):
            # Binary case
            y_mapped = (y == 1).astype(int)   # -1 -> 0, 1 -> 1
            num_classes = 2
        else:
            # Three-class case (-1,0,1)
            y_mapped = (y + 1).astype(int)
            num_classes = 3

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        params: Dict[str, Any] = dict(
            n_estimators=50,
            max_depth=3,
            learning_rate=0.1,
            random_state=42,
            eval_metric="mlogloss",
            verbosity=0,
        )
        if num_classes >= 3:
            params["objective"] = "multi:softprob"
            params["num_class"] = 3
        else:
            params["objective"] = "binary:logistic"

        model = XGBClassifier(**params)
        model.fit(X_scaled, y_mapped)

        X_latest = df[FEATURE_COLS].iloc[-1:].values
        X_latest_scaled = scaler.transform(X_latest)

        proba = model.predict_proba(X_latest_scaled)[0]
        class_idx = int(np.argmax(proba))
        confidence = float(proba[class_idx])

        explainer = shap.TreeExplainer(model)
        shap_output = explainer.shap_values(X_latest_scaled)

        values = _extract_shap_row(shap_output, class_idx)
        if values is None:
            return None

        factors: List[Dict[str, Any]] = []
        for feat, val in zip(FEATURE_COLS, values):
            factors.append(
                {
                    "feature": FEATURE_LABELS.get(feat, feat),
                    "impact": round(float(val), 4),
                    "direction": "positive" if val >= 0 else "negative",
                }
            )
        factors.sort(key=lambda f: abs(f["impact"]), reverse=True)

        # Map class index back to BULLISH/BEARISH/NEUTRAL.
        # Only reliable when we trained on the full 3-class Signal space;
        # for the 2-class fallback we infer direction from EMA levels.
        if num_classes >= 3:
            label_map = {0: "BEARISH", 1: "NEUTRAL", 2: "BULLISH"}
            prediction_label = label_map.get(class_idx, "NEUTRAL")
        else:
            latest = df.iloc[-1]
            prediction_label = "BULLISH" if latest["EMA_20"] > latest["EMA_50"] else "BEARISH"

        return {
            "prediction": prediction_label,
            "confidence": round(confidence, 4),
            "top_factors": factors[:5],
        }

    except Exception as e:
        print(f"[explain] Failed to compute explanation: {e}")
        return None


def _extract_shap_row(shap_output: Any, class_idx: int) -> Optional[np.ndarray]:
    """
    SHAP's return shape varies by version:
      - list of arrays, one per class: shap_output[class_idx][0]
      - single array (binary): shap_output[0]
      - 3D array (n_samples, n_features, n_classes): shap_output[0][:, class_idx]
    Normalize all of these into a 1D array of per-feature impacts.
    """
    try:
        if isinstance(shap_output, list):
            arr = shap_output[class_idx]
            return np.asarray(arr[0])

        arr = np.asarray(shap_output)
        if arr.ndim == 3:
            # (n_samples, n_features, n_classes)
            return arr[0, :, class_idx]
        if arr.ndim == 2:
            return arr[0]
        return arr
    except Exception as e:
        print(f"[explain] Could not normalize SHAP output shape: {e}")
        return None