import spacy

nlp = spacy.load("ru_core_news_sm")

RUBRICS = {
    "Спорт": [
        "футбол", "хоккей", "баскетбол", "теннис", "олимпиада",
        "чемпионат", "турнир", "матч", "игра", "спортсмен",
        "тренер", "команда", "победа", "гол", "спорт",
        "атлет", "соревнование", "медаль", "рекорд", "клуб"
    ],
    "Политика": [
        "президент", "правительство", "министр", "парламент", "выборы",
        "закон", "политика", "санкция", "государство", "депутат",
        "голосование", "партия", "дипломатия", "переговоры", "саммит",
        "конституция", "власть", "оппозиция", "реформа", "посол"
    ],
    "Экономика": [
        "экономика", "рубль", "доллар", "инфляция", "бюджет",
        "банк", "кредит", "акция", "биржа", "инвестиция",
        "налог", "цена", "рынок", "производство", "экспорт",
        "импорт", "торговля", "валюта", "ввп", "компания"
    ],
    "Наука и технологии": [
        "наука", "учёный", "исследование", "открытие", "технология",
        "искусственный", "интеллект", "робот", "космос", "спутник",
        "эксперимент", "лаборатория", "физика", "химия", "биология",
        "медицина", "вакцина", "климат", "энергия", "цифровой"
    ],
    "Культура": [
        "театр", "кино", "фильм", "выставка", "музей",
        "концерт", "спектакль", "художник", "режиссёр", "актёр",
        "книга", "литература", "искусство", "фестиваль", "музыка",
        "картина", "галерея", "культура", "писатель", "творчество"
    ],
    "Общество": [
        "образование", "школа", "университет", "здоровье", "больница",
        "пенсия", "зарплата", "демография", "семья", "молодёжь",
        "социальный", "жильё", "транспорт", "экология", "город",
        "регион", "население", "права", "гражданин", "волонтёр"
    ]
}


def read_file(filename):
    """Читает текстовый файл и возвращает его содержимое."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
        return text
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        return None


def tokenize_and_lemmatize(text):
    """Разбивает текст на слова и приводит каждое к начальной форме."""
    doc = nlp(text)
    lemmas = []
    for token in doc:
        if not token.is_punct and not token.is_space:
            lemmas.append(token.lemma_.lower())
    return lemmas


def count_matches(lemmas, rubrics):
    """Считает, сколько ключевых слов каждой рубрики встретилось в тексте."""
    scores = {}
    for rubric_name, keywords in rubrics.items():
        count = 0
        for lemma in lemmas:
            if lemma in keywords:
                count += 1
        scores[rubric_name] = count
    return scores


def classify_news(scores):
    """Возвращает рубрику с наибольшим числом совпадений."""
    best_rubric = max(scores, key=scores.get)
    if scores[best_rubric] == 0:
        return "Не определено"
    return best_rubric


def print_results(text, rubric, scores):
    """Выводит текст новости, рубрику и статистику."""
    print("\n" + "=" * 60)
    print("ТЕКСТ НОВОСТИ:")
    print("=" * 60)
    print(text)
    print("\n" + "=" * 60)
    print(f"РУБРИКА: {rubric}")
    print("=" * 60)
    print("\nСТАТИСТИКА СОВПАДЕНИЙ:")
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for rubric_name, count in sorted_scores:
        bar = "█" * count
        print(f"  {rubric_name:<25} {count:>3} совп.  {bar}")
    print("=" * 60)


def main():
    print("=" * 60)
    print("  ПРОГРАММА ДЛЯ РУБРИКАЦИИ НОВОСТЕЙ")
    print("=" * 60)

    filename = input("\nВведите имя файла с новостью: ").strip()

    text = read_file(filename)
    if text is None:
        return

    lemmas = tokenize_and_lemmatize(text)
    print(f"\nТокенизация выполнена. Найдено токенов: {len(lemmas)}")

    scores = count_matches(lemmas, RUBRICS)
    rubric = classify_news(scores)
    print_results(text, rubric, scores)


if __name__ == "__main__":
    main()
