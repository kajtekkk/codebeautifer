#Importy i konfiguracja 

import os
import shutil
import subprocess
from openai import OpenAI
from dotenv import load_dotenv

#Ładowanie  zmiennych środowiskowych i inicjalizacja OpenAI 

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(f"[DEBUG] API Key loaded: {api_key}")  # <- dodaj to
client = OpenAI(api_key=api_key)


# Pliki
INPUT_FILE = "my_code.py"
CLEAN_FILE = "my_code_clean.py"
COMMENTED_FILE = "my_code_commented.py"

#Formatowanie Kodu przy użyciu black #
def run_black(input_file, output_file):
    shutil.copyfile(input_file, output_file)
    try:
        subprocess.run(["black", output_file], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("⚠️  [black] Nie udało się sformatować kodu – prawdopodobnie błąd składniowy.")

#Funkcje pomocnicze odczytu i zapisu plików 

def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

#Prompt engineering ;) odpytywanie AI o feedback 

def ask_openai_for_feedback(code):
    prompt = (
        "Oceń poniższy kod Python. "
        "Dodaj komentarze wyjaśniające błędy składniowe, literówki, złe praktyki oraz sugestie optymalizacji. "
        "Wstaw komentarze bezpośrednio do kodu – linia po linii. "
        "Następnie podsumuj sugestie w osobnym bloku na końcu.\n\n"
        f"{code}\n"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return response.choices[0].message.content.strip()

#Logiczna stona aplikacji

def main():
    print("[1] Formatowanie kodu...")
    run_black(INPUT_FILE, CLEAN_FILE)

    print("[2] Wysyłanie kodu do AI...")
    original_code = read_file(INPUT_FILE)
    full_comment_with_suggestions = ask_openai_for_feedback(original_code)

    print("[3] Zapisywanie pliku z komentarzami i sugestiami...")
    write_file(COMMENTED_FILE, full_comment_with_suggestions)

    print("[✅] Gotowe! Wygenerowano:")
    print(f"- {CLEAN_FILE}")
    print(f"- {COMMENTED_FILE}")


#Uruchomienie skryptu
if __name__ == "__main__":
    main()


###
