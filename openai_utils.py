from config import my_api
import openai

openai.api_key = my_api


async def create_answer(text):  # TODO системне повідомлення
    answer = await __get_gpt_completion(text=text)
    return answer


async def __get_gpt_completion(text):  # TODO системне повідомлення
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},  # TODO налаштувати
            {"role": "user", "content": f"{text}"}
        ]
    )

    answer = completion.choices[0].message
    return answer['content']