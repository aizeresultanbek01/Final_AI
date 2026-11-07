class MessageAgent:
    """Агент для предварительного анализа подозрительных сообщений."""

    FRAUD_KEYWORDS = [
        "переведите деньги",
        "подтвердите карту",
        "ваш аккаунт заблокирован",
        "получите выигрыш",
        "срочно перейдите по ссылке",
        "код из sms",
        "ваш счет заблокирован"
    ]

    SPAM_KEYWORDS = [
        "выиграй приз",
        "бесплатный подарок",
        "скидка 90%",
        "вы выиграли",
        "акция только сегодня"
    ]

    def analyze(self, message):
        if not isinstance(message, str) or not message.strip():
            return {
                "category": "unknown",
                "confidence": 0.0,
                "reason": "Сообщение пустое или некорректное"
            }

        text = message.lower()

        fraud_found = [
            word for word in self.FRAUD_KEYWORDS if word in text
        ]

        spam_found = [
            word for word in self.SPAM_KEYWORDS if word in text
        ]

        if fraud_found:
            return {
                "category": "fraud",
                "confidence": 0.8,
                "reason": "Обнаружены подозрительные фразы: "
                          + ", ".join(fraud_found)
            }

        if spam_found:
            return {
                "category": "spam",
                "confidence": 0.8,
                "reason": "Обнаружены рекламные фразы: "
                          + ", ".join(spam_found)
            }

        return {
            "category": "safe",
            "confidence": 0.6,
            "reason": "Подозрительные фразы не обнаружены"
        }


if __name__ == "__main__":
    agent = MessageAgent()

    test_message = "Ваш аккаунт заблокирован, подтвердите карту"

    result = agent.analyze(test_message)
    print(result)
  
