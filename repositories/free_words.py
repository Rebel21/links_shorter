from faker import Faker

faker = Faker("en_US")


def generate_three_words(number_words: int = 3):
    """
    Функция генерирует уникальную строку из заданного количества слов сллов.

    Уникальность работает только для одного инстанса приложения. в дальнейшем нужно будет придумать механизм
    глобального отслезивания уникальности
    """
    string = faker.unique.sentence(
        nb_words=number_words, variable_nb_words=False).replace(".", "").replace(" ", ".").lower()
    return string


if __name__ == '__main__':
    print(generate_three_words())
    print(generate_three_words(number_words=3))
    print(generate_three_words(number_words=4))
    print(generate_three_words(number_words=5))
