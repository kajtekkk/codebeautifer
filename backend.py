from flask import Flask, request, jsonify
import subprocess
import openai
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        "Przeanalizuj poniższy kod Pythona. Jeśli zawiera błędy (poniżej), wyjaśnij co jest nie tak i zaproponuj poprawki."
        "\n\nKod:\n" + code + ("\n\nBłąd:\n" + error_trace if error_trace else "")
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

    return jsonify({
        "stdout": result,
        "error": error_trace,
        "ai_feedback": ai_feedback
    })

from flask import send_from_directory

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
