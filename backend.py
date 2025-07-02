from flask import Flask, request, jsonify, send_from_directory, send_file
import subprocess
import openai
import os
import traceback
from dotenv import load_dotenv
from io import BytesIO
from datetime import datetime

# Ładowanie API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

# ANALIZA KODU
@app.route("/analyze", methods=["POST"])
def analyze():
    code = request.json.get("code", "")
    result = ""
    error_trace = ""

    try:
        result = subprocess.check_output(["python3", "-c", code], stderr=subprocess.STDOUT, timeout=5, text=True)
    except subprocess.CalledProcessError as e:
        error_trace = e.output
    except Exception as e:
        error_trace = str(e) + "\n" + traceback.format_exc()

    prompt = (
        "Przeanalizuj poniższy kod Pythona. Jeśli zawiera błędy (poniżej), wyjaśnij co jest nie tak i zaproponuj poprawki. "
        "Proszę nie używaj formatowania Markdown (czyli bez ```python).\n\nKod:\n"
        + code + ("\n\nBłąd:\n" + error_trace if error_trace else "")
    )

    ai_feedback = "(Brak odpowiedzi AI)"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        ai_feedback = response.choices[0].message.content.strip()
    except Exception as e:
        ai_feedback = "Błąd AI: " + str(e)

    # Zapis danych do tymczasowej sesji (można potem zapisać do pliku)
    global LAST_ANALYSIS
    LAST_ANALYSIS = {
        "code": code,
        "stdout": result,
        "error": error_trace,
        "ai_feedback": ai_feedback
    }

    return jsonify(LAST_ANALYSIS)

# POBIERZ RAPORT
@app.route("/download_report", methods=["GET"])
def download_report():
    if not LAST_ANALYSIS:
        return "Brak danych do pobrania", 400

    report = (
        f"Raport analizy kodu - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        "\n--- KOD ---\n" + LAST_ANALYSIS["code"] +
        "\n\n--- WYNIK ---\n" + (LAST_ANALYSIS["stdout"] or "[brak wyjścia]") +
        "\n\n--- BŁĘDY ---\n" + (LAST_ANALYSIS["error"] or "[brak błędów]") +
        "\n\n--- FEEDBACK AI ---\n" + (LAST_ANALYSIS["ai_feedback"] or "[brak informacji]")
    )

    file_stream = BytesIO()
    file_stream.write(report.encode("utf-8"))
    file_stream.seek(0)

    return send_file(file_stream, as_attachment=True, download_name="raport.txt", mimetype="text/plain")

# WYSYŁANIE STRONY GŁÓWNEJ
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# OBSŁUGA CZATU
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

# AI – ZASTOSUJ POPRAWKI
@app.route("/apply_fixes", methods=["POST"])
def apply_fixes():
    code = request.json.get("code", "")
    if not code.strip():
        return jsonify({"fixed_code": "(Brak kodu do poprawienia)"})

    prompt = (
        "Zastosuj poprawki do poniższego kodu Pythona i zwróć tylko poprawiony kod, bez wyjaśnień ani komentarzy. "
        "Proszę nie używaj formatowania Markdown (czyli bez ```python).\n\nKod:\n" + code
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

# OBSŁUGA UPLOADU .py
@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files.get("file")
    if uploaded_file and uploaded_file.filename.endswith(".py"):
        code = uploaded_file.read().decode("utf-8")
        return jsonify({"code": code})
    return jsonify({"error": "Nieprawidłowy plik"}), 400

# Tymczasowy storage wyników analizy
LAST_ANALYSIS = {}

# START
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
