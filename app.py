
import streamlit as st

from models.train_models import train_all_models
from models.bayes_model import predict_message
from models.ml_model import predict_ml_message

st.set_page_config(
    page_title="Qorgau AI",
    page_icon="🛡️",
    layout="wide"
)

# DESIGN
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #0B1120;
    color: #F1F5F9;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

header {visibility: hidden;}
footer {visibility: hidden;}

.hero {
    background: linear-gradient(120deg, #142B3B, #102B36);
    border: 1px solid #24505A;
    padding: 35px;
    border-radius: 22px;
    margin-bottom: 28px;
}

.logo {
    color: #4ADEB5;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 4px;
}

.hero h1 {
    color: white;
    font-size: 38px;
    margin: 15px 0 10px 0;
    font-weight: 800;
}

.hero p {
    color: #B5C7D5;
    font-size: 16px;
}

.section-title {
    color: #F1F5F9;
    font-size: 22px;
    font-weight: 700;
    margin: 25px 0 15px;
}

.card {
    background: #151F31;
    border: 1px solid #29394D;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 15px;
}

.card h3 {
    color: #F1F5F9;
    font-size: 17px;
}

.card p {
    color: #AAB9CA;
}

.result {
    background: #112E2B;
    border: 1px solid #286B5B;
    border-radius: 16px;
    padding: 22px;
    margin-top: 20px;
}

.stTextArea textarea {
    background: #151F31 !important;
    color: white !important;
    border: 1px solid #35465B !important;
    border-radius: 12px !important;
}

.stButton button {
    background: #16A085;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 25px;
    font-weight: 700;
    width: 100%;
}

.stButton button:hover {
    background: #0F8C75;
    color: white;
    border: none;
}

div[data-testid="stMetric"] {
    background: #151F31;
    border: 1px solid #29394D;
    padding: 17px;
    border-radius: 13px;
}

div[data-testid="stMetricLabel"] {
    color: #AAB9CA;
}

div[data-testid="stMetricValue"] {
    color: #4ADEB5;
}

hr {
    border-color: #29394D;
}

.footer {
    text-align: center;
    color: #718096;
    font-size: 12px;
    padding: 30px;
}
</style>
""", unsafe_allow_html=True)


# LOAD MODELS
@st.cache_resource
def load_models():
    return train_all_models()


# HEADER
st.markdown("""
<div class="hero">
    <div class="logo">🛡️ QORGAU AI</div>
    <h1>Ваша безопасность начинается здесь</h1>
    <p>
        Интеллектуальная система анализа SMS и сообщений.
        Обнаруживайте потенциальный мошеннический контент
        с помощью машинного обучения.
    </p>
</div>
""", unsafe_allow_html=True)


# MODEL LOADING
try:
    bayes_model, logistic_model, results = load_models()
    st.success("Система активна · Обе модели загружены")

    st.markdown(
        '<div class="section-title">Проверка сообщения</div>',
        unsafe_allow_html=True
    )

    message = st.text_area(
        "Вставьте текст сообщения",
        placeholder="Например: Ваш аккаунт заблокирован. Подтвердите карту...",
        height=150,
        label_visibility="collapsed"
    )

    if st.button("🛡️  ПРОВЕРИТЬ СООБЩЕНИЕ"):
        if message.strip():

            bayes_result = predict_message(
                bayes_model, message
            )

            logistic_result = predict_ml_message(
                logistic_model, message
            )

            labels = {
                "fraud": "Мошенничество",
                "spam": "Спам",
                "safe": "Безопасное сообщение"
            }

            st.markdown(
                '<div class="section-title">Результаты анализа</div>',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    '<div class="card"><h3>🧠 Naive Bayes</h3></div>',
                    unsafe_allow_html=True
                )
                st.metric(
                    "Категория",
                    labels.get(
                        str(bayes_result["category"]),
                        str(bayes_result["category"])
                    )
                )
                st.metric(
                    "Уверенность модели",
                    f'{bayes_result["confidence"] * 100:.1f}%'
                )

            with col2:
                st.markdown(
                    '<div class="card"><h3>⚙️ Logistic Regression</h3></div>',
                    unsafe_allow_html=True
                )
                st.metric(
                    "Категория",
                    labels.get(
                        str(logistic_result["category"]),
                        str(logistic_result["category"])
                    )
                )
                st.metric(
                    "Уверенность модели",
                    f'{logistic_result["confidence"] * 100:.1f}%'
                )

            if bayes_result["category"] == logistic_result["category"]:
                category = labels.get(
                    str(bayes_result["category"]),
                    str(bayes_result["category"])
                )
                st.markdown(
                    f'<div class="result"><h3>✓ Обе модели согласны</h3>'
                    f'<p>Определённая категория: <b>{category}</b></p></div>',
                    unsafe_allow_html=True
                )
            else:
                st.warning(
                    "Модели дали разные результаты. "
                    "Рекомендуется дополнительная проверка."
                )

        else:
            st.warning("Сначала введите сообщение.")

    # MODEL METRICS
    st.markdown("---")
    st.markdown(
        '<div class="section-title">Эффективность моделей</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    for column, (name, metrics) in zip(
        [col1, col2], results.items()
    ):
        with column:
            st.markdown(
                f'<div class="card"><h3>{name}</h3></div>',
                unsafe_allow_html=True
            )
            st.metric("Accuracy", f'{metrics["accuracy"]:.2%}')
            st.metric("Macro F1", f'{metrics["f1"]:.2%}')

except Exception as error:
    st.error(f"Ошибка загрузки моделей: {error}")

# FOOTER
st.markdown("""
<div class="footer">
    QORGAU AI · DIGITAL SECURITY<br>
    Учебный проект по искусственному интеллекту
</div>
""", unsafe_allow_html=True)

