"""
models.py
Machine Learning and Deep Learning model definitions, training routines,
and evaluation suites for 1-to-3 day ahead rainfall prediction.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional, List
import joblib

# Scikit-learn
from sklearn.multioutput import MultiOutputRegressor, MultiOutputClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report
)

# Gradient Boosters (graceful import)
try:
    import lightgbm as lgb
    HAS_LGBM = True
except ImportError:
    HAS_LGBM = False

try:
    import xgboost as xgb
    HAS_XGB = True
except ImportError:
    HAS_XGB = False


class MultiDayRainModelSuite:
    """
    Manages multi-day (Day +1, Day +2, Day +3) regression and classification models.
    """
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.models_reg: Dict[str, Any] = {}
        self.models_clf: Dict[str, Any] = {}
        self.feature_names: List[str] = []
        
    def initialize_models(self):
        """Initializes baseline and gradient boosted models for regression and classification."""
        # 1. Regression Models (predicting mm of rainfall for Day 1, Day 2, Day 3)
        self.models_reg['Ridge Baseline'] = MultiOutputRegressor(
            Ridge(alpha=1.0, random_state=self.random_state)
        )
        
        self.models_reg['Random Forest'] = MultiOutputRegressor(
            RandomForestRegressor(n_estimators=100, max_depth=12, random_state=self.random_state, n_jobs=-1)
        )
        
        if HAS_LGBM:
            self.models_reg['LightGBM'] = MultiOutputRegressor(
                lgb.LGBMRegressor(
                    n_estimators=150,
                    learning_rate=0.05,
                    max_depth=6,
                    num_leaves=31,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    random_state=self.random_state,
                    verbose=-1
                )
            )
            
        if HAS_XGB:
            self.models_reg['XGBoost'] = MultiOutputRegressor(
                xgb.XGBRegressor(
                    n_estimators=150,
                    learning_rate=0.05,
                    max_depth=5,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    random_state=self.random_state
                )
            )
            
        # 2. Binary Classification Models (predicting Rain Yes/No on Day 1, Day 2, Day 3)
        self.models_clf['Logistic Baseline'] = MultiOutputClassifier(
            LogisticRegression(max_iter=1000, random_state=self.random_state)
        )
        
        self.models_clf['Random Forest Clf'] = MultiOutputClassifier(
            RandomForestClassifier(n_estimators=100, max_depth=10, random_state=self.random_state, n_jobs=-1)
        )
        
        if HAS_LGBM:
            self.models_clf['LightGBM Clf'] = MultiOutputClassifier(
                lgb.LGBMClassifier(
                    n_estimators=150,
                    learning_rate=0.05,
                    max_depth=5,
                    num_leaves=31,
                    random_state=self.random_state,
                    verbose=-1
                )
            )
            
        if HAS_XGB:
            self.models_clf['XGBoost Clf'] = MultiOutputClassifier(
                xgb.XGBClassifier(
                    n_estimators=150,
                    learning_rate=0.05,
                    max_depth=5,
                    random_state=self.random_state
                )
            )

    def train_all_models(self, X_train: pd.DataFrame, y_train_reg: pd.DataFrame, y_train_clf: pd.DataFrame):
        """Fits all initialized regression and classification models."""
        self.feature_names = list(X_train.columns)
        self.initialize_models()
        
        print(f"--- Training {len(self.models_reg)} Regression Models on {X_train.shape[0]} samples ---")
        for name, model in self.models_reg.items():
            print(f"Training Regressor: {name}...")
            model.fit(X_train, y_train_reg)
            
        print(f"\n--- Training {len(self.models_clf)} Classification Models ---")
        for name, model in self.models_clf.items():
            print(f"Training Classifier: {name}...")
            model.fit(X_train, y_train_clf)
            
        print("Training complete!")

    def evaluate_regression(self, X_test: pd.DataFrame, y_test_reg: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates MAE, RMSE, R2, and Normalized RMSE for each horizon (Day 1, 2, 3) across all models.
        """
        results = []
        horizons = ['Day +1 (0-24h)', 'Day +2 (25-48h)', 'Day +3 (49-72h)']
        
        for name, model in self.models_reg.items():
            preds = model.predict(X_test)
            preds = np.clip(preds, 0, None)  # Rainfall cannot be negative
            
            for i, h in enumerate(horizons):
                y_true = y_test_reg.iloc[:, i].values
                y_pred = preds[:, i]
                
                mae = mean_absolute_error(y_true, y_pred)
                rmse = np.sqrt(mean_squared_error(y_true, y_pred))
                r2 = r2_score(y_true, y_pred)
                
                results.append({
                    'Model': name,
                    'Horizon': h,
                    'MAE (mm)': round(mae, 3),
                    'RMSE (mm)': round(rmse, 3),
                    'R2 Score': round(r2, 4)
                })
                
        return pd.DataFrame(results)

    def evaluate_classification(self, X_test: pd.DataFrame, y_test_clf: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates Accuracy, Precision, Recall, F1-Score, and ROC-AUC for rain occurrence.
        """
        results = []
        horizons = ['Day +1 (0-24h)', 'Day +2 (25-48h)', 'Day +3 (49-72h)']
        
        for name, model in self.models_clf.items():
            preds = model.predict(X_test)
            
            for i, h in enumerate(horizons):
                y_true = y_test_clf.iloc[:, i].values
                y_pred = preds[:, i]
                
                acc = accuracy_score(y_true, y_pred)
                prec = precision_score(y_true, y_pred, zero_division=0)
                rec = recall_score(y_true, y_pred, zero_division=0)
                f1 = f1_score(y_true, y_pred, zero_division=0)
                
                try:
                    # Probabilities if available
                    proba = model.predict_proba(X_test)[i][:, 1]
                    auc = roc_auc_score(y_true, proba)
                except Exception:
                    auc = np.nan
                    
                results.append({
                    'Model': name,
                    'Horizon': h,
                    'Accuracy': round(acc, 4),
                    'Precision': round(prec, 4),
                    'Recall': round(rec, 4),
                    'F1-Score': round(f1, 4),
                    'ROC-AUC': round(auc, 4) if not np.isnan(auc) else 'N/A'
                })
                
        return pd.DataFrame(results)

    def save_best_models(self, reg_model_name: str = 'LightGBM', clf_model_name: str = 'LightGBM Clf', filepath_prefix: str = 'rain_model'):
        """Saves best performing models and feature metadata to disk using joblib."""
        if reg_model_name not in self.models_reg:
            reg_model_name = list(self.models_reg.keys())[0]
        if clf_model_name not in self.models_clf:
            clf_model_name = list(self.models_clf.keys())[0]
            
        bundle = {
            'regressor_name': reg_model_name,
            'classifier_name': clf_model_name,
            'regressor': self.models_reg[reg_model_name],
            'classifier': self.models_clf[clf_model_name],
            'feature_names': self.feature_names
        }
        
        save_path = f"{filepath_prefix}_bundle.joblib"
        joblib.dump(bundle, save_path)
        print(f"Models successfully saved to: {save_path}")
        return save_path
