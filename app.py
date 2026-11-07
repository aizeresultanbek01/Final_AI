
import streamlit as st

from models.train_models import train_all_models
from models.bayes_model import predict_message
from models.ml_model import predict_ml_message

st.set_page_config(
    page_title="Qorgau AI",
    page_icon="🛡️",
    layout="centered"
)

st.title("Qorgau AI")
st.subheader("Интеллектуальная защита от мошеннических сообщений")

st.write(
    "Введите подозрительное сообщение. "
    "Две модели машинного обучения проанализируют его."
)

@st.cache_resource
def load_models():
    return train_all_models()

try:
    bayes_model, logistic_model, results = load_models()

    st.success("Модели успешно загружены и обучены.")

    st.divider()

    message = st.text_area(
        "Введите сообщение:",
        placeholder="Например: Ваш аккаунт заблокирован..."
    )

    if st.button("Проверить сообщение"):
        if message.strip():

            bayes_result = predict_message(
                bayes_model, message
            )

            logistic_result = predict_ml_message(
                logistic_model, message
            )

            st.subheader("Результаты анализа")

            col1, col2 = st.columns(2)

            with col1:
                st.write("Naive Bayes")
                st.write("Категория:", bayes_result["category"])
                st.write(
                    "Уверенность:",
                    f'{bayes_result["confidence"] * 100:.1f}%'
                )

            with col2:
                st.write("Logistic Regression")
                st.write("Категория:", logistic_result["category"])
                st.write(
                    "Уверенность:",
                    f'{logistic_result["confidence"] * 100:.1f}%'
                )

            if bayes_result["category"] == logistic_result["category"]:
                st.info("Обе модели определили одинаковую категорию.")
            else:
                st.warning(
                    "Модели не согласны. Рекомендуется "
                    "дополнительно проверить сообщение."
                )

        else:
            st.info("Сначала введите сообщение.")

    st.divider()

    st.subheader("Качество моделей на тестовых данных")

    for model_name, metrics in results.items():
        st.write(model_name)
        st.write(f'Accuracy: {metrics["accuracy"]:.2%}')
        st.write(f'Macro F1: {metrics["f1"]:.2%}')

except Exception as error:
    st.error(f"Не удалось загрузить модели: {error}")

st.caption(
    "Qorgau AI — учебный прототип для анализа сообщений."
)

