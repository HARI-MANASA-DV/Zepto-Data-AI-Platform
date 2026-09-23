# Analytics

This module contains my Titanic dataset analysis and machine learning work.

## EDA

I used the Titanic dataset for exploratory data analysis.

The EDA includes:

* Loading and checking the dataset
* Missing-value analysis
* Data cleaning
* Age and fare analysis
* Survival rate analysis
* Multivariate analysis
* Correlation analysis
* Standardization of age and fare
* Data visualizations

### Data Cleaning

The `deck` column was removed because it had a large number of missing values.

Missing `age` values were filled using the median age.

Rows with missing values in `embarked` and `embark_town` were removed.

The cleaned dataset is saved as:

```text
cleaned_titanic.csv
```

## Machine Learning

For classification, I used:

* Logistic Regression
* Decision Tree
* Random Forest
* Tuned Random Forest

The models were evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC

I also checked class imbalance using:

* Normal Logistic Regression
* Balanced class weights
* SMOTE

For Random Forest, I used `GridSearchCV` to find better hyperparameters and also checked the OOB score.

## Regression

I used Multivariate Linear Regression to predict the `fare` value.

The regression model was evaluated using:

* MAE
* RMSE
* R²
* Adjusted R²

I also created a residual plot to check the model errors.

## Files

```text
01_eda.ipynb
02_modeling.ipynb
titanic.csv
cleaned_titanic.csv
best_pipeline.joblib
classifier_comparison.csv
regression_results.csv
imbalance_comparison.csv
charts/
requirements.txt
```

## Run

Install the required packages:

```bash
pip install -r requirements.txt
```

Open the notebooks in this order:

```text
01_eda.ipynb
02_modeling.ipynb
```

The modeling notebook also saves the trained Random Forest pipeline and tests it again after reloading.
