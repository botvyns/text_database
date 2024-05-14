from find_words import find_by_lemma, find_by_wordform, user_input

user_input_prompt = """Введіть три параметри для пошуку слів:
1. Слово малими літерами
2. L -> пошук за лемою АБО F -> пошук за словоформою
3. Назва тексту (базою даних) : first_text.db АБО second_text.db
"""

user_input_str = input(user_input_prompt).strip()

# Check if user input is empty
if not user_input_str:
    print("Не введено жодного параметра. Будь ласка, введіть усі три параметри.")
    exit()

# Split user input
user_input_list = user_input_str.split()

# Check if user input contains exactly three parameters
if len(user_input_list) != 3:
    print("Неправильна кількість параметрів. Будь ласка, введіть три параметри.")
    exit()

word, word_type, database = user_input_list

# Check if word type is valid
if word_type.upper() not in ['F', 'L']:
    print("Неправильно вказаний тип слова для пошуку. Використовуйте 'F' для словоформи або 'L' для леми.")
    exit()

search_results = user_input(word.lower(), word_type.upper(), database)
for result in search_results:
    print(result)