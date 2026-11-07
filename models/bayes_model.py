from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def create_bayes_model():
    """
    Создаёт модель Naive Bayes
    для классификации сообщений.
    """

    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )),
        ("classifier", MultinomialNB(alpha=0.5))
    ])

    return model


def train_bayes_model(messages, labels):
    """
    Обучает модель на примерах сообщений.
    """

    model = create_bayes_model()
    model.fit(messages, labels)

    return model


def predict_message(model, message):
    """
    Определяет категорию сообщения.
    """

    prediction = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]

    confidence = float(max(probabilities))

    return {
        "category": prediction,
        "confidence": confidence
    }
