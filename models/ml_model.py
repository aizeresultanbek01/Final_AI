from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def create_ml_model():
    """
    Создаёт модель Logistic Regression
    с TF-IDF векторизацией.
    """

    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=5000
        )),
        ("classifier", LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        ))
    ])

    return model


def train_ml_model(messages, labels):
    """
    Обучает модель на текстовых сообщениях.
    """

    model = create_ml_model()
    model.fit(messages, labels)

    return model


def predict_ml_message(model, message):
    """
    Предсказывает категорию сообщения.
    """

    prediction = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]

    confidence = float(max(probabilities))

    return {
        "category": prediction,
        "confidence": confidence
    }
