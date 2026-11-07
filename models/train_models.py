
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

from models.bayes_model import train_bayes_model, predict_message
from models.ml_model import train_ml_model, predict_ml_message


def train_all_models():
    data = pd.read_csv("data/messages.csv")

    messages = data["message"].astype(str)
    labels = data["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        messages,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels
    )

    bayes = train_bayes_model(X_train, y_train)
    logistic = train_ml_model(X_train, y_train)

    bayes_predictions = [predict_message(bayes, msg)["category"] for msg in X_test]
    logistic_predictions = [
        predict_ml_message(logistic, msg)["category"] for msg in X_test
    ]

    results = {
        "Naive Bayes": {
            "accuracy": accuracy_score(y_test, bayes_predictions),
            "f1": f1_score(y_test, bayes_predictions, average="macro")
        },
        "Logistic Regression": {
            "accuracy": accuracy_score(y_test, logistic_predictions),
            "f1": f1_score(y_test, logistic_predictions, average="macro")
        }
    }

    return bayes, logistic, results
