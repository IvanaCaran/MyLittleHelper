import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 1.4,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    }
]
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings= safety_settings,
  generation_config=generation_config,
)

history = []

print("Bot: Hello, how can I help you?")

while True:
    # Benutzereingabe lesen
    user_input = input("You: ")

    # Chat-Sitzung erstellen und Nachricht senden
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(user_input)

    # Antwort des Modells ausgeben
    model_response = response.text
    print(f"Bot: {model_response}")
    print()

    # Verlauf aktualisieren
    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [model_response]})