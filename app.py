from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import pandas as pd
import numpy as np
import json
import os
import plotly
import plotly.express as px
import plotly.graph_objects as go
from werkzeug.utils import secure_filename

from utils.data_processor import process_data, get_data_summary
from utils.visualizations import create_visualization

# Создание экземпляра Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ваш_секретный_ключ'  # Для работы flash-сообщений
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'json'}

# Проверка наличия директории для загрузки файлов
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Функция для проверки разрешенных расширений файлов
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Загрузка примера данных для демонстрации
SAMPLE_DATA_PATH = os.path.join('static', 'sample_data', 'students.csv')

# Функция для загрузки данных из файла
def load_data(file_path):
    if file_path.endswith('.csv'):
        try:
            # Пробуем загрузить с кодировкой UTF-8 с BOM (для Windows)
            return pd.read_csv(file_path, encoding='utf-8-sig')
        except UnicodeDecodeError:
            # Если не получилось, пробуем другие кодировки
            try:
                return pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                return pd.read_csv(file_path, encoding='cp1251')
    elif file_path.endswith('.json'):
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
            return pd.json_normalize(data)
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return pd.json_normalize(data)
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='cp1251') as f:
                    data = json.load(f)
                return pd.json_normalize(data)
    return None

# Функция для проверки наличия и генерации тестовых данных
def ensure_sample_data_exists():
    """Проверяет наличие тестовых данных и генерирует их при необходимости"""
    if not os.path.exists(SAMPLE_DATA_PATH):
        try:
            logger.info("Генерация тестовых данных...")
            # Импортируем модуль генерации данных
            import sys
            sys.path.append('.')
            from utils.generate_sample_data import generate_student_data, convert_to_csv_format, save_data
            
            # Генерация данных
            students_data = generate_student_data(50)
            csv_data = convert_to_csv_format(students_data)
            
            # Сохранение данных
            save_data(students_data, csv_data)
            
            logger.info(f"Тестовые данные успешно сгенерированы и сохранены в {SAMPLE_DATA_PATH}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при генерации тестовых данных: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    return True

# Проверка наличия тестовых данных при запуске приложения
ensure_sample_data_exists()

# Маршрут для главной страницы
@app.route('/')
def index():
    # Проверяем наличие тестовых данных
    if not os.path.exists(SAMPLE_DATA_PATH):
        if ensure_sample_data_exists():
            flash('Тестовые данные были автоматически сгенерированы', 'info')
        else:
            flash('Не удалось найти или сгенерировать тестовые данные. Это может повлиять на работу демо-режима.', 'warning')
    
    return render_template('index.html')

# Маршрут для загрузки данных
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Проверка наличия файла в запросе
        if 'file' not in request.files:
            flash('Файл не выбран', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Если пользователь не выбрал файл
        if file.filename == '':
            flash('Файл не выбран', 'error')
            return redirect(request.url)
        
        # Если файл существует и имеет допустимое расширение
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Перенаправление на страницу визуализации
            return redirect(url_for('visualization', filename=filename))
        else:
            flash('Недопустимый формат файла. Разрешены только .csv и .json', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')

# Маршрут для выбора и создания визуализаций
@app.route('/visualization/<filename>', methods=['GET', 'POST'])
def visualization(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Проверка существования файла
    if not os.path.exists(file_path):
        flash('Файл не найден', 'error')
        return redirect(url_for('upload'))
    
    try:
        # Загрузка данных
        data = load_data(file_path)
        
        # Получение сводки данных для отображения
        data_summary = get_data_summary(data)
        
        # Получение списка колонок для выбора
        columns = list(data.columns)
        
        if request.method == 'POST':
            # Получение параметров для визуализации
            viz_type = request.form.get('viz_type', 'bar')
            x_column = request.form.get('x_column')
            y_column = request.form.get('y_column')
            color_column = request.form.get('color_column', None)
            
            print(f"Доступные колонки: {columns}")
            print(f"Тип данных: {type(data)}")
            print(f"Выбранные параметры: x={x_column}, y={y_column}, color={color_column}")
            
            # Создание визуализации
            fig = create_visualization(data, viz_type, x_column, y_column, color_column)
            
            # Преобразование графика в JSON для передачи на клиент
            graph_json = plotly.io.to_json(fig)
            
            # Проверка, что graph_json - это строка
            if not isinstance(graph_json, str):
                # Если это не строка, преобразуем объект в JSON-строку
                import json
                graph_json = json.dumps(graph_json)
            
            return render_template('visualization.html', 
                                  filename=filename,
                                  columns=columns,
                                  data_summary=data_summary,
                                  graph_json=graph_json,
                                  selected_viz=viz_type,
                                  selected_x=x_column,
                                  selected_y=y_column,
                                  selected_color=color_column)
        
        # По умолчанию при GET запросе
        return render_template('visualization.html',
                              filename=filename,
                              columns=columns,
                              data_summary=data_summary)
    
    except Exception as e:
        flash(f'Ошибка при обработке файла: {str(e)}', 'error')
        return redirect(url_for('upload'))

# Маршрут для API - получения данных в формате JSON
@app.route('/api/data/<filename>')
def api_data(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'Файл не найден'}), 404
    
    try:
        data = load_data(file_path)
        return jsonify(data.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Маршрут для API - получения сводки данных
@app.route('/api/summary/<filename>')
def api_summary(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'Файл не найден'}), 404
    
    try:
        data = load_data(file_path)
        summary = get_data_summary(data)
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Демонстрационный маршрут для показа примера визуализации
@app.route('/demo')
def demo():
    try:
        # Загрузка примера данных
        if os.path.exists(SAMPLE_DATA_PATH):
            data = load_data(SAMPLE_DATA_PATH)
            
            # Создание некоторых визуализаций для демонстрации
            viz_types = ['bar', 'line', 'scatter', 'histogram', 'box', 'heatmap']
            graphs = {}
            
            # Для каждого типа графика создаем визуализацию
            for viz_type in viz_types:
                try:
                    if viz_type == 'bar':
                        # Средние оценки по предметам
                        fig = create_visualization(
                            data, 
                            viz_type, 
                            'предмет', 
                            'оценка', 
                            None, 
                            agg_func='mean'
                        )
                    elif viz_type == 'line':
                        # Средняя посещаемость по предметам
                        fig = create_visualization(
                            data, 
                            viz_type, 
                            'предмет', 
                            'посещаемость', 
                            None, 
                            agg_func='mean'
                        )
                    elif viz_type == 'scatter':
                        # Связь между оценкой и посещаемостью
                        fig = create_visualization(
                            data, 
                            viz_type, 
                            'посещаемость', 
                            'оценка', 
                            'курс'
                        )
                    elif viz_type == 'histogram':
                        # Распределение оценок
                        fig = create_visualization(
                            data, 
                            viz_type, 
                            'оценка', 
                            None, 
                            None
                        )
                    elif viz_type == 'box':
                        # Распределение оценок по предметам
                        fig = create_visualization(
                            data, 
                            viz_type, 
                            'предмет', 
                            'оценка', 
                            None
                        )
                    elif viz_type == 'heatmap':
                        # Тепловая карта средних оценок по предметам и курсам
                        pivot_data = pd.pivot_table(
                            data, 
                            values='оценка', 
                            index=['курс'], 
                            columns=['предмет'], 
                            aggfunc='mean'
                        )
                        fig = go.Figure(data=go.Heatmap(
                            z=pivot_data.values,
                            x=pivot_data.columns,
                            y=pivot_data.index,
                            colorscale='Viridis'
                        ))
                        fig.update_layout(
                            title='Средние оценки по предметам и курсам',
                            xaxis_title='Предмет',
                            yaxis_title='Курс'
                        )
                    
                    # Всегда преобразуем фигуру в строку JSON
                    import json
                    # Сначала конвертируем фигуру в JSON, если она еще не в этом формате
                    fig_json = plotly.io.to_json(fig)
                    # Проверяем, что получили строку, а не объект
                    if not isinstance(fig_json, str):
                        fig_json = json.dumps(fig_json)
                    
                    # Далее проверим, что JSON валидный, попробовав его распарсить и снова сериализовать
                    # Это гарантирует, что мы отправим в шаблон валидный JSON
                    try:
                        json.loads(fig_json)  # Проверка валидности JSON
                        graphs[viz_type] = fig_json
                    except json.JSONDecodeError:
                        # Если не можем распарсить, значит, это не валидный JSON
                        # Преобразуем объект напрямую
                        graphs[viz_type] = json.dumps({"data": [], "layout": {"title": "Ошибка генерации графика"}})
                        print(f"Ошибка при сериализации графика {viz_type}")
                
                except Exception as e:
                    # В случае ошибки при создании конкретного графика, создаем пустой график с сообщением об ошибке
                    print(f"Ошибка при создании графика {viz_type}: {str(e)}")
                    graphs[viz_type] = json.dumps({"data": [], "layout": {"title": f"Ошибка: {str(e)}"}})
            
            return render_template('demo.html', graphs=graphs)
        else:
            flash('Пример данных не найден', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Ошибка при загрузке демонстрации: {str(e)}', 'error')
        return redirect(url_for('index'))

# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)