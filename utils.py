import random

waiting_phrases = [
    'Хвилинку...',
    'Ще трохи...',
    'Думаю...',
    'Зараз, почекайте будь ласка...',
    'Я все ще думаю...',
    'Скоро буде відповідь...',
    'Зачекайте ще трохи...',
    'І ще трохи...',
]


def get_random_waiting_phrase():
    return f'<i>{random.choice(waiting_phrases)}</i>'
