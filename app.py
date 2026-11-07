import streamlit as st
import pandas as pd
from models.training import train_models
from agent.message_agent import MessageAgent

st.set_page_config(page_title="Qorgau AI", page_icon="🛡️", layout="centered")
st.title("Qorgau AI")
st.caption("Қазақша және орысша хабарламаларды алдын ала талдау прототипі")

@st.cache_resource
def get_agent():
    bayes, logistic, metrics = train_models()
    return MessageAgent(bayes, logistic), metrics

try:
    agent, metrics = get_agent()
    message = st.text_area("Тексергіңіз келетін хабарламаны енгізіңіз:", height=140,
                           placeholder="Мысалы: Сіздің картаңыз бұғатталды. Сілтемеге өтіңіз...")
    if st.button("Хабарламаны тексеру", type="primary"):
        if not message.strip():
            st.warning("Алдымен хабарлама енгізіңіз.")
        else:
            result = agent.analyze(message)
            st.subheader("Талдау нәтижесі")
            st.write(f"**Болжамды санат:** {result['label']}")
            st.write(f"**Модель сенімділігі:** {result['confidence']:.1%}")
            st.caption("Бұл — оқу жобасының прототипі. Нәтижеге толық сенуге болмайды.")
            st.write("**Күмәнді сөздер:**", ", ".join(result["suspicious_terms"]) or "Табылмады")
            st.write("**Модельдер болжамы:**")
            st.json(result["model_outputs"])
    with st.expander("Модель метрикалары"):
        st.json(metrics)
except Exception as exc:
    st.error(f"Жобаны іске қосу кезінде қате шықты: {exc}")
    st.info("Терминалда: pip install -r requirements.txt командасын орындаңыз.")
