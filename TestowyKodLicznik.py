def count_file_stats(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Plik nie został znaleziony.")
        return
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return
    
    num_lines = len(lines)
    num_words = sum(len(line.split()) for line in lines)
    num_chars = sum(len(line) for line in lines)

