from flaml import AutoML
import pandas as pd

# 0. prepare
print("\nPredict income using FLAML AutoML ")

# 1. load data
print("\nLoading data into memory ")
train_file = pd.read_csv("/Users/tamasmakos/dev/survey_methods_room/train.csv")
# Split data into train and test sets
train_X = train_file.drop(['target'], axis=1)
train_y = train_file['target']

# 2. Initialize an AutoML instance
print("\nCreating a FLAML object ")

automl = AutoML()
automl_settings = {
  "time_budget": 60,  # in seconds
  "metric": 'r2',
  "task": 'regression',
  "log_file_name": "house_price.log"
}

# 3. find and train model
print("\nFinding best model ")
automl.fit(X_train=train_X, y_train=train_y,
  **automl_settings)
print("Done ")

# 4. show best model found
best_model = automl.model.estimator
print("\nBest model: ")
print(best_model)


print("\nEnd FLAML")