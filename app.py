from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os

# Завантажуємо змінні середовища з .env файлу
load_dotenv()

app = Flask(__name__)

# Використовуємо змінну середовища для API ключа
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/generate-dataset', methods=['POST'])
def generate_dataset():
    data = request.json
    number_of_items = data.get('num', 1)  # Отримуємо кількість елементів з запиту

    # Формуємо контекстний запит з динамічною кількістю елементів
    prompt = f"Створіть {number_of_items} елементів датасету для категорії \"Керування контейнерами\" в Docker. Кожен елемент датасету повинен містити \"input\" - команду людською мовою, що описує дію з керування контейнерами в Docker, та \"output\" - відповідну команду Docker CLI, виконану у Bash.\n\nКатегорія: Керування контейнерами\n\nОпис категорії: Категорія \"Керування контейнерами\" охоплює команди Docker CLI, які використовуються для створення, запуску, зупинки, видалення та управління контейнерами Docker. Це включає команди для перегляду стану контейнерів, їх логів, а також виконання команд всередині запущених контейнерів.\n\nІнструкція: Для кожного елементу датасету використовуйте різноманітні сценарії керування контейнерами, такі як створення нового контейнера, запуск існуючого, зупинка, видалення контейнерів, перегляд активних або всіх контейнерів, виконання команд у контейнері, копіювання файлів до та з контейнера, та інспектування контейнерів."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"response": response['choices'][0]['message']['content']})  # Повертаємо текст відповіді
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
