# CodeBeautifier – Asystent czytelności kodu z automatyczną aktualizacją Git

## Opis projektu

**CodeBeautifier** to narzędzie wspomagające czytelność i jakość kodu w języku Python. Automatycznie analizuje kod źródłowy po jego uruchomieniu, poprawia jego formatowanie i generuje sugestie dotyczące potencjalnych usprawnień. Po zakończeniu działania:

- Tworzona jest wizualnie ulepszona wersja kodu (`clean.py`),
- Generowany jest plik `sugestie_ai.txt` z podpowiedziami dotyczącymi stylu, optymalizacji i możliwych błędów,
- Wszystkie pliki są commitowane i wysyłane do repozytorium Git,
- Zmiany są automatycznie odświeżane w IDE (np. PyCharm).

Nie jest wymagane użycie zewnętrznych narzędzi CI/CD.

## Funkcjonalności

- Automatyczna analiza kodu po uruchomieniu skryptu,
- Poprawa czytelności kodu zgodnie z PEP8,
- Sugestie AI dotyczące stylu, optymalizacji i potencjalnych błędów,
- Automatyczny commit i push do repozytorium Git,
- Automatyczne odświeżenie plików w edytorze (np. PyCharm),
- (Opcjonalnie) możliwość konfiguracji własnych reguł analizy.

## Użyte technologie

-  Technologie 
-Frontend: HTML, CSS, JS, CodeMirror 
-Backend: Python + Flask 
-AI: OpenAI GPT-4 
-Hosting: Render.com 
-Inne: dotenv, subprocess
- Bilioteki Python:  flask – obsługa backendu i tras HTTP 
-  subprocess – uruchamianie kodu użytkownika 
- openai – integracja z GPT-4 
- os – operacje systemowe i ścieżki 
- traceback – wyłapywanie i analiza błędów 
- dotenv – odczyt klucza API z pliku .env 
- io – obsługa strumieni danych (raporty) 
- datetime – znacznik czasu dla raportów 
 
## Struktura plików

-  backend.py 
- static/index.html 
- .env 
-  requirements.txt
## Wymagania

- Python 3.8+
- Zainstalowane biblioteki: `black`, `flake8`, `openai`, `gitpython`, itp.
- Konto OpenAI z kluczem API (do generowania sugestii AI)
- Skonfigurowane repozytorium Git

## Uruchomienie

1. Skonfiguruj środowisko Python i zainstaluj wymagane biblioteki.
2. Upewnij się, że masz poprawnie skonfigurowane repozytorium Git.
3. Uruchom `beautify.py` zamiast bezpośredniego uruchamiania swojego skryptu.
4. Sprawdź wyniki w `my_code_clean.py` oraz `sugestie_ai.txt`.

## Cel edukacyjny

Projekt pozwala studentom na:

- Zastosowanie praktycznych narzędzi do analizy kodu,
- Integrację AI w codziennej pracy programistycznej,
- Poznanie automatyzacji z użyciem Git i narzędzi CLI,
- Wdrażanie dobrych praktyk w zakresie jakości i stylu kodu.

## Autorzy

Grupa projektowa **3J**:
- Kajetan Szymczak (95522)
- Mariusz Szmondrowski (96591)
- Adrian Mikołajczyk (96192)
- Jan Kulinski (95402)


Link Do Strony 
https://codebeautifer.onrender.com
https://github.com/kajtekkk/codebeautifer
