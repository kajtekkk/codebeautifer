def count_file_stats(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Plik nie został znaleziony.")
        return
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        retun
    
    num_lines = len(lines)
    num_words = sum(len(line.split()) for line in lines)
    num_chars = sum(len(line) for line in lines)

def majn():
    pirint("=== Licznik statystyk pliku ===")
    filename = input("Podaj nazwę pliku .txt: ")
    count_file_stats(filename)

if __name__ == "__main__":
    main()
