# Training

This folder contains model training, evaluation, and features' weights.

### Logistic Regression
- Used for binary classification tasks (e.g., predicting occurrence of events)
- Includes handling of class imbalance (`class_weight="balanced"`)
- Evaluated using accuracy, precision, recall, and F1 score

### Linear Regression
- Applied for regression tasks (e.g., predicting continuous outcomes)
- Evaluated using RMSE, MAE, and R² metrics
- Serves as a baseline model for comparison

### Random Forest
- Ensemble model used for classification
- Includes hyperparameter tuning (`n_estimators`, `max_depth`, `min_samples_split`)
- Trained using `TimeSeriesSplit` to preserve temporal order
- Evaluated using classification metrics and additional tools such as ROC and Precision-Recall curves

### XGBoost
- Advanced gradient boosting implementation for high-performance classification.
- Utilizes **SMOTE** (Synthetic Minority Over-sampling Technique) to address class imbalance.
- Features automated hyperparameter optimization using `RandomizedSearchCV`.
- Optimized for CPU execution with `hist` tree method.

### CatBoost
- Gradient boosting library that handles categorical features efficiently.
- Trained on integrated weather and ISW data to provide robust probability estimates.

### K-Nearest Neighbors (KNN)
- Instance-based learning used to analyze local data structures and similarities between regional alarm patterns.

## Purpose
The purpose of this folder is to train and evaluate multiple models, compare their performance, and select the most suitable approach for forecasting tasks. It ensures that models are tested in a time-aware manner and optimized for realistic predictions.
