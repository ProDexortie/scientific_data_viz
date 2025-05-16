import pandas as pd
import numpy as np
import random
import json
import os
from datetime import datetime

# Русские имена и фамилии
first_names = [
    "Александр", "Екатерина", "Михаил", "Анна", "Дмитрий", "Ольга", 
    "Сергей", "Мария", "Иван", "Наталья", "Андрей", "Елена", 
    "Никита", "Татьяна", "Владимир", "Ирина", "Алексей", "Юлия"
]

last_names = [
    "Иванов", "Смирнова", "Кузнецов", "Попова", "Соколов", "Лебедева",
    "Новиков", "Морозова", "Петров", "Волкова", "Захаров", "Павлова",
    "Соловьев", "Семенова", "Михайлов", "Федорова", "Степанов", "Орлова"
]

# Предметы
subjects = [
    "Математика", "Физика", "Информатика", "Русский язык", 
    "Литература", "История", "Биология", "Химия", "География"
]

# Для воспроизводимости результатов
np.random.seed(42)
random.seed(42)

def generate_student_data(num_students=50):
    """Генерирует данные об успеваемости студентов"""
    data = []
    for i in range(1, num_students + 1):
        student_id = i
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        age = random.randint(18, 25)
        course = random.randint(1, 5)
        entry_year = datetime.now().year - course
        
        # Генерация оценок для каждого предмета
        grades = {}
        attendance = {}
        for subject in subjects:
            # Оценки от 2 до 5
            grades[subject] = round(random.uniform(2.0, 5.0), 1)
            # Посещаемость (в процентах)
            attendance[subject] = round(random.uniform(60.0, 100.0), 1)
        
        # Средний балл
        avg_grade = round(sum(grades.values()) / len(grades), 2)
        avg_attendance = round(sum(attendance.values()) / len(attendance), 2)
        
        # Стипендия (если средний балл ≥ 4.5)
        scholarship = avg_grade >= 4.5
        
        student = {
            "id": student_id,
            "имя": first_name,
            "фамилия": last_name,
            "возраст": age,
            "курс": course,
            "год_поступления": entry_year,
            "оценки": grades,
            "посещаемость": attendance,
            "средний_балл": avg_grade,
            "средняя_посещаемость": avg_attendance,
            "стипендия": scholarship
        }
        data.append(student)
    
    return data

def convert_to_csv_format(students_data):
    """Преобразует данные о студентах в плоский формат для CSV"""
    csv_data = []
    for student in students_data:
        for subject in subjects:
            row = {
                "студент_id": student["id"],
                "имя": student["имя"],
                "фамилия": student["фамилия"],
                "возраст": student["возраст"],
                "курс": student["курс"],
                "год_поступления": student["год_поступления"],
                "предмет": subject,
                "оценка": student["оценки"][subject],
                "посещаемость": student["посещаемость"][subject],
                "средний_балл": student["средний_балл"],
                "средняя_посещаемость": student["средняя_посещаемость"],
                "стипендия": student["стипендия"]
            }
            csv_data.append(row)
    return csv_data

def save_data(students_data, csv_data, json_filename='static/sample_data/students.json', csv_filename='static/sample_data/students.csv'):
    """Сохраняет данные в форматах JSON и CSV"""
    # Создание директории, если она не существует
    os.makedirs(os.path.dirname(json_filename), exist_ok=True)
    
    try:
        # Сохранение в формате JSON с явным указанием кодировки UTF-8
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(students_data, f, ensure_ascii=False, indent=2)
        
        # Сохранение в формате CSV с BOM для корректного отображения в Windows
        df = pd.DataFrame(csv_data)
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        
        print(f"Данные сохранены в файлах {json_filename} и {csv_filename}")
    except Exception as e:
        print(f"Ошибка при сохранении данных: {str(e)}")
        
        # Попытка сохранить в другой директории, если возникли проблемы с путями
        alt_json_filename = 'students.json'
        alt_csv_filename = 'students.csv'
        
        with open(alt_json_filename, 'w', encoding='utf-8') as f:
            json.dump(students_data, f, ensure_ascii=False, indent=2)
        
        df = pd.DataFrame(csv_data)
        df.to_csv(alt_csv_filename, index=False, encoding='utf-8-sig')
        
        print(f"Данные сохранены в альтернативные файлы {alt_json_filename} и {alt_csv_filename}")
        print(f"Пожалуйста, переместите эти файлы в папку static/sample_data/ вручную")

def main():
    print("Генерация тестовых данных...")
    # Генерация данных о 50 студентах
    students_data = generate_student_data(50)
    
    # Преобразование в формат CSV
    csv_data = convert_to_csv_format(students_data)
    
    # Сохранение данных
    save_data(students_data, csv_data)
    
    # Вывод статистики
    print(f"Сгенерировано данных о {len(students_data)} студентах")
    print(f"Всего записей в CSV: {len(csv_data)}")

if __name__ == "__main__":
    main()