import requests
import json
from random import randint
import psycopg2


# sudo apt install fish
# fish
# virtualenv venv
# source venv/bin/activate.fish
# pip install psycopg2-binary
# pip install requests
# pip freeze > requirements.txt

def generate_person(n=1):
    # Создайте список для хранения информации о людях
    people_list = []
    professions = ["engineer", "teacher", "scientist", "developer", "programmer", "artist", "designer", "nurse", "doctor", "lawyer"]
    
    # Connect к PostgreSQL database
    connection = psycopg2.connect(
        host="localhost",
        user="marselle",
        password="123",
        database="mydb3"
    )
    cursor = connection.cursor()
    
    # Создать таблицу, если она не существует
    cursor.execute("CREATE TABLE users(id SERIAL PRIMARY KEY, login VARCHAR(50), name VARCHAR(50), gender VARCHAR(50),\
        age INT, email VARCHAR(255), city VARCHAR(255), profession VARCHAR(255), phone VARCHAR(255))")
    
    # Отправить n запросов на получение в API
    for i in range(n):
        response = requests.get("https://randomuser.me/api/?nat=ru")
        
        # Проанализируйте ответ JSON
        data = json.loads(response.text)
        
        # Извлеките login
        login = data['results'][0]["login"]["username"]
        
        # Извлеките имя и фамилию из ответа
        first_name = data["results"][0]["name"]["first"]
        last_name = data["results"][0]["name"]["last"]
        
        # Извлеките пол пользователя из ответа
        gender = data["results"][0]["gender"]
        
        # Объедините имя и фамилию
        full_name = first_name + " " + last_name
        
        # Сгенерируйте возраст с помощью randint
        age = randint(18, 80)
        
        # Сгенерировать электронное письмо
        email = data["results"][0]["email"]
        
        # Извлеките город проживание из ответа
        city = data["results"][0]["location"]["city"]
        
        # Генерировать случайную профессию
        profession = professions[randint(0, len(professions)-1)]
        
        # Сгенерировать номер телефона
        phone = data["results"][0]["phone"]
        
        # Вставьте информацию о человеке в таблицу
        cursor.execute("INSERT INTO users (login, name, gender, age, email, city, profession, phone) VALUES \
            (%s, %s, %s, %s, %s, %s, %s, %s)",(login, full_name, gender, age, email, city, profession, phone))
        
        # Зафиксируйте изменения в базе данных
        connection.commit()
        
        # Добавьте информацию о человеке в список на всякий
        people_list.append({
            "login": login,
            "name": full_name,
            "gender": gender,
            "age": age, 
            "email": email, 
            "city": city,
            "profession": profession, 
            "phone": phone
            })
    
    # Закройте курсор и соединение
    cursor.close()
    
    # Закройте connection
    connection.close()
    return people_list

print(generate_person(500))
