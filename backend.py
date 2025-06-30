#Importowanie 
from flask import Flask, request, jsonify
import subprocess
import openai
import os
import traceback
from dotenv import load_dotenv

#Ładowanie API
load_dotenv()

#Inicjalizacja aplikacji Flask
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

#Punkt dostepu analizy kodu
@app.route("/analyze", methods=["POST"])
def analyze():
    code = request.json.get("code", "")
    result = ""
    error_trace = ""

    try:
        # Uruchom kod i przechwyć stdout
        result = subprocess.check_output(["python3", "-c", code], stderr=subprocess.STDOUT, timeout=5, text=True)
    except subprocess.CalledProcessError as e:
        error_trace = e.output
    except Exception as e:
        error_trace = str(e) + "\n" + traceback.format_exc()

    # Budujemy prompt z błędem (jeśli był)
    prompt = (
        "Przeanalizuj poniższy kod Pythona. Jeśli zawiera błędy (poniżej), wyjaśnij co jest nie tak i zaproponuj poprawki. "
        "Proszę nie używaj formatowania Markdown (czyli bez ```python)."
        "\n\nKod:\n" + code + ("\n\nBłąd:\n" + error_trace if error_trace else "")
    )



    ai_feedback = "(Brak odpowiedzi AI)"
    try:
#Zapytanie do AI
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        ai_feedback = response.choices[0].message.content.strip()
    except Exception as e:
        ai_feedback = "Błąd AI: " + str(e)

#Zwraca wynik w formacie JSON
    return jsonify({
        "stdout": result,
        "error": error_trace,
        "ai_feedback": ai_feedback
    })

from flask import send_from_directory

#Serwerowanie Strony głownej
@app.route("/")
def index():
    return send_from_directory("static", "index.html")




#Chat
@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json.get("prompt", "")
    prompt += "\n\nOdpowiedz proszę bez formatowania Markdown (bez ```), tylko sam tekst."
    if not prompt.strip():
        return jsonify({"response": "(Brak treści do analizy)"})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"response": f"Błąd AI: {str(e)}"})

#Zmiany
@app.route("/apply_fixes", methods=["POST"])
def apply_fixes():
    code = request.json.get("code", "")
    if not code.strip():
        return jsonify({"fixed_code": "(Brak kodu do poprawienia)"})

    prompt = (
         "Zastosuj poprawki do poniższego kodu Pythona i zwróć tylko poprawiony kod, bez wyjaśnień ani komentarzy. "
         "Proszę nie używaj formatowania Markdown (czyli bez ```python).\n\nKod:\n"
         + code
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        fixed_code = response.choices[0].message.content.strip()
        return jsonify({"fixed_code": fixed_code})
    except Exception as e:
        return jsonify({"fixed_code": f"Błąd AI: {str(e)}"})


#Uruchomienie apki
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
