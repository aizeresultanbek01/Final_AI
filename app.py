import streamlit as st

st.set_page_config(
    page_title="Qorgau AI",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ Qorgau AI")
st.subheader("Интеллектуальная защита от мошеннических сообщений")

st.write(
    "Проверьте подозрительное сообщение "
    "и узнайте, может ли оно быть мошенническим."
)

st.divider()

message = st.text_area(
    "Введите сообщение для проверки:",
    placeholder="Например: Ваш аккаунт заблокирован. Подтвердите карту..."
)

if st.button("Проверить сообщение"):
    if message.strip():
        text = message.lower()

        fraud_words = [
            "переведите деньги",
            "подтвердите карту",
            "код из sms",
            "аккаунт заблокирован"
        ]

        spam_words = [
            "выиграй приз",
            "бесплатный подарок",
            "скидка 90%"
        ]

        if any(word in text for word in fraud_words):
            st.error("⚠️ Обнаружены признаки мошенничества!")

        elif any(word in text for word in spam_words):
            st.warning("📢 Обнаружены признаки спама!")

        else:
            st.success("✅ Подозрительные фразы не обнаружены.")

    else:
        st.info("Сначала введите сообщение.")

st.divider()

st.caption("Qorgau AI — ваш помощник в цифровой безопасности.")
