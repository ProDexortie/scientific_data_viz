import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.data_processor import aggregate_data, pivot_data

def create_visualization(data, viz_type, x_column=None, y_column=None, color_column=None, 
                        agg_func='mean', title=None, x_label=None, y_label=None):
    """
    Создает визуализацию на основе указанных параметров.
    
    Args:
        data (pd.DataFrame): Данные для визуализации.
        viz_type (str): Тип визуализации ('bar', 'line', 'scatter', 'histogram', 'box', 'heatmap', 'pie').
        x_column (str): Колонка для оси X.
        y_column (str): Колонка для оси Y.
        color_column (str): Колонка для цветового кодирования.
        agg_func (str): Функция агрегации для числовых данных.
        title (str): Заголовок графика.
        x_label (str): Подпись оси X.
        y_label (str): Подпись оси Y.
        
    Returns:
        plotly.graph_objects.Figure: Объект графика Plotly.
    """
    try:
        # Проверка наличия данных
        if data is None or data.empty:
            raise ValueError("Данные отсутствуют или пусты")
            
        # Отладочный вывод колонок
        print(f"Доступные колонки в данных: {list(data.columns)}")
        print(f"Выбранные параметры: x={x_column}, y={y_column}, color={color_column}")
        
        # Проверка наличия необходимых колонок
        if viz_type not in ['histogram', 'pie'] and (x_column is None or (y_column is None and viz_type != 'histogram')):
            raise ValueError("Необходимо указать колонки для осей X и Y")
            
        # Проверка колонки X
        if x_column is not None and x_column not in data.columns:
            raise ValueError(f"Колонка {x_column} не найдена в данных. Доступные колонки: {', '.join(data.columns)}")
            
        # Проверка колонки Y
        if y_column is not None and y_column not in data.columns:
            raise ValueError(f"Колонка {y_column} не найдена в данных. Доступные колонки: {', '.join(data.columns)}")
            
        # Проверка и обработка колонки для цветовой группировки
        if color_column is not None:
            # Если выбрано "Без группировки" или пустое значение
            if color_column == "Без группировки" or color_column == "":
                color_column = None
            # Иначе проверяем наличие колонки в данных
            elif color_column not in data.columns:
                raise ValueError(f"Колонка {color_column} не найдена в данных. Доступные колонки: {', '.join(data.columns)}")
        
        # Попытка установить русскую локаль для Plotly
        try:
            import locale
            locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        except locale.Error:
            pass  # Игнорируем ошибку на Windows, если локаль недоступна
        
        # Заголовок по умолчанию
        if title is None:
            title = f"Визуализация {viz_type}"
        
        # Подписи осей по умолчанию
        if x_label is None and x_column is not None:
            x_label = x_column
        if y_label is None and y_column is not None:
            y_label = y_column
        
        # Создание визуализации в зависимости от типа
        if viz_type == 'bar':
            try:
                # ИЗМЕНЕНИЕ: Для столбчатой диаграммы используем исходные данные, если нужна группировка по цвету
                if color_column:
                    fig = px.bar(
                        data, 
                        x=x_column, 
                        y=y_column, 
                        color=color_column,
                        title=title,
                        labels={x_column: x_label, y_column: y_label},
                        template="plotly_white"
                    )
                else:
                    # Если нет группировки по цвету, можно использовать агрегацию
                    if x_column and data[x_column].nunique() > 50:
                        plot_data = aggregate_data(data, x_column, y_column, agg_func)
                    else:
                        plot_data = aggregate_data(data, x_column, y_column, agg_func)
                    
                    fig = px.bar(
                        plot_data, 
                        x=x_column, 
                        y=y_column,
                        title=title,
                        labels={x_column: x_label, y_column: y_label},
                        template="plotly_white"
                    )
            except Exception as e:
                raise ValueError(f"Ошибка при создании столбчатой диаграммы: {str(e)}")
        
        elif viz_type == 'line':
            try:
                # ИЗМЕНЕНИЕ: Для линейного графика используем исходные данные, если нужна группировка по цвету
                if color_column:
                    fig = px.line(
                        data, 
                        x=x_column, 
                        y=y_column, 
                        color=color_column,
                        markers=True,
                        title=title,
                        labels={x_column: x_label, y_column: y_label},
                        template="plotly_white"
                    )
                else:
                    # Если нет группировки по цвету, можно использовать агрегацию
                    if x_column and data[x_column].nunique() > 50:
                        plot_data = aggregate_data(data, x_column, y_column, agg_func)
                    else:
                        plot_data = aggregate_data(data, x_column, y_column, agg_func)
                    
                    fig = px.line(
                        plot_data, 
                        x=x_column, 
                        y=y_column,
                        markers=True,
                        title=title,
                        labels={x_column: x_label, y_column: y_label},
                        template="plotly_white"
                    )
            except Exception as e:
                raise ValueError(f"Ошибка при создании линейного графика: {str(e)}")
        
        elif viz_type == 'scatter':
            try:
                fig = px.scatter(
                    data, 
                    x=x_column, 
                    y=y_column, 
                    color=color_column,
                    size_max=15,
                    opacity=0.7,
                    title=title,
                    labels={x_column: x_label, y_column: y_label},
                    template="plotly_white"
                )
            except Exception as e:
                raise ValueError(f"Ошибка при создании точечной диаграммы: {str(e)}")
        
        elif viz_type == 'histogram':
            try:
                fig = px.histogram(
                    data, 
                    x=x_column,
                    color=color_column,
                    marginal="box",
                    title=title,
                    labels={x_column: x_label},
                    template="plotly_white"
                )
            except Exception as e:
                raise ValueError(f"Ошибка при создании гистограммы: {str(e)}")
        
        elif viz_type == 'box':
            try:
                fig = px.box(
                    data, 
                    x=x_column, 
                    y=y_column, 
                    color=color_column,
                    title=title,
                    labels={x_column: x_label, y_column: y_label},
                    template="plotly_white",
                    points="all"
                )
            except Exception as e:
                raise ValueError(f"Ошибка при создании диаграммы box plot: {str(e)}")
        
        elif viz_type == 'heatmap':
            # Для тепловой карты необходимо создать сводную таблицу
            try:
                # ИЗМЕНЕНИЕ: Обрабатываем случай, когда для тепловой карты нужны все три колонки
                if x_column and y_column and color_column:
                    pivot_table = pivot_data(data, x_column, y_column, color_column, agg_func)
                    
                    fig = go.Figure(data=go.Heatmap(
                        z=pivot_table.values,
                        x=pivot_table.columns,
                        y=pivot_table.index,
                        colorscale='Viridis'
                    ))
                    
                    fig.update_layout(
                        title=title,
                        xaxis_title=y_label,
                        yaxis_title=x_label,
                        template="plotly_white"
                    )
                else:
                    raise ValueError("Для тепловой карты необходимо указать все три параметра: X, Y и Значения")
            except Exception as e:
                raise ValueError(f"Ошибка при создании тепловой карты: {str(e)}")
        
        elif viz_type == 'pie':
            try:
                if x_column is None:
                    raise ValueError("Для круговой диаграммы необходимо указать колонку категорий")
                
                # Агрегация данных
                value_counts = data[x_column].value_counts().reset_index()
                value_counts.columns = [x_column, 'count']
                
                fig = px.pie(
                    value_counts, 
                    names=x_column, 
                    values='count',
                    title=title,
                    template="plotly_white"
                )
            except Exception as e:
                raise ValueError(f"Ошибка при создании круговой диаграммы: {str(e)}")
        
        else:
            raise ValueError(f"Неподдерживаемый тип визуализации: {viz_type}")
        
        # Настройка внешнего вида
        fig.update_layout(
            font=dict(family="Arial", size=14),
            title={
                'text': title,
                'x': 0.5,
                'y': 0.95,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=18)
            },
            margin=dict(l=50, r=50, t=80, b=50),
            legend_title_text="Категории",
            hovermode="closest"
        )
        
        return fig
    
    except Exception as e:
        # Создаем пустой график с сообщением об ошибке
        fig = go.Figure()
        fig.update_layout(
            title=f"Ошибка при создании визуализации: {str(e)}",
            annotations=[
                go.layout.Annotation(
                    text=f"Ошибка: {str(e)}",
                    showarrow=False,
                    font=dict(size=14, color="red"),
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5
                )
            ]
        )
        # Записываем ошибку в лог
        import logging
        logging.error(f"Ошибка при создании визуализации: {str(e)}")
        return fig

def create_multi_visualization(data, viz_types, columns, titles=None):
    """
    Создает несколько визуализаций для одного набора данных.
    
    Args:
        data (pd.DataFrame): Данные для визуализации.
        viz_types (list): Список типов визуализаций.
        columns (dict): Словарь колонок для каждой визуализации.
        titles (list): Список заголовков для визуализаций.
        
    Returns:
        list: Список объектов графиков Plotly.
    """
    figures = []
    
    for i, viz_type in enumerate(viz_types):
        # Определение параметров для каждой визуализации
        x_column = columns.get(i, {}).get('x')
        y_column = columns.get(i, {}).get('y')
        color_column = columns.get(i, {}).get('color')
        
        # Заголовок
        title = None
        if titles is not None and i < len(titles):
            title = titles[i]
        
        # Создание визуализации
        try:
            fig = create_visualization(
                data,
                viz_type,
                x_column,
                y_column,
                color_column,
                title=title
            )
            figures.append(fig)
        except Exception as e:
            print(f"Ошибка при создании визуализации {viz_type}: {str(e)}")
    
    return figures

def create_dashboard_visualization(data):
    """
    Создает готовый дашборд с несколькими визуализациями для анализа данных.
    
    Args:
        data (pd.DataFrame): Данные для визуализации.
        
    Returns:
        plotly.graph_objects.Figure: Объект дашборда Plotly.
    """
    from plotly.subplots import make_subplots
    
    # Определяем, какие колонки использовать для визуализации
    numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
    
    if not numeric_cols or not categorical_cols:
        raise ValueError("Недостаточно данных для создания дашборда")
    
    # Создаем макет для дашборда с 2x2 графиками
    fig = make_subplots(
        rows=2, 
        cols=2,
        subplot_titles=("Гистограмма", "Диаграмма рассеяния", "Столбчатая диаграмма", "Коробчатая диаграмма"),
        specs=[[{"type": "xy"}, {"type": "xy"}],
               [{"type": "xy"}, {"type": "xy"}]]
    )
    
    # 1. Гистограмма для первой числовой колонки
    first_numeric = numeric_cols[0]
    histogram_trace = go.Histogram(
        x=data[first_numeric],
        name=first_numeric,
        marker_color='#1f77b4'
    )
    fig.add_trace(histogram_trace, row=1, col=1)
    
    # 2. Диаграмма рассеяния для первых двух числовых колонок
    if len(numeric_cols) >= 2:
        second_numeric = numeric_cols[1]
        scatter_trace = go.Scatter(
            x=data[first_numeric],
            y=data[second_numeric],
            mode='markers',
            name=f'{first_numeric} vs {second_numeric}',
            marker=dict(color='#ff7f0e', size=8, opacity=0.7)
        )
        fig.add_trace(scatter_trace, row=1, col=2)
    
    # 3. Столбчатая диаграмма для первой категориальной колонки
    first_categorical = categorical_cols[0]
    value_counts = data[first_categorical].value_counts().nlargest(10)
    bar_trace = go.Bar(
        x=value_counts.index,
        y=value_counts.values,
        name=first_categorical,
        marker_color='#2ca02c'
    )
    fig.add_trace(bar_trace, row=2, col=1)
    
    # 4. Коробчатая диаграмма
    if len(categorical_cols) >= 2 and len(categorical_cols[1]) < 10:
        second_categorical = categorical_cols[1]
        box_trace = go.Box(
            x=data[second_categorical],
            y=data[first_numeric],
            name=f'{first_numeric} по {second_categorical}',
            marker_color='#d62728'
        )
        fig.add_trace(box_trace, row=2, col=2)
    else:
        box_trace = go.Box(
            y=data[first_numeric],
            name=first_numeric,
            marker_color='#d62728'
        )
        fig.add_trace(box_trace, row=2, col=2)
    
    # Настройка макета
    fig.update_layout(
        title_text="Дашборд анализа данных",
        font=dict(family="Arial", size=12),
        showlegend=False,
        height=800,
        template="plotly_white"
    )
    
    return fig

def visualize_correlation_matrix(data):
    """
    Создает визуализацию корреляционной матрицы для числовых данных.
    
    Args:
        data (pd.DataFrame): Данные для анализа корреляций.
        
    Returns:
        plotly.graph_objects.Figure: Объект графика Plotly.
    """
    # Выбираем только числовые колонки
    numeric_data = data.select_dtypes(include=['int64', 'float64'])
    
    # Если нет числовых колонок, вызываем ошибку
    if numeric_data.empty:
        raise ValueError("В данных отсутствуют числовые колонки для расчета корреляций")
    
    # Расчет корреляционной матрицы
    corr_matrix = numeric_data.corr()
    
    # Создание тепловой карты
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu_r',
        zmin=-1,
        zmax=1
    ))
    
    # Добавление текста значений корреляции
    annotations = []
    
    for i, row in enumerate(corr_matrix.values):
        for j, value in enumerate(row):
            annotations.append(
                dict(
                    x=corr_matrix.columns[j],
                    y=corr_matrix.index[i],
                    text=f"{value:.2f}",
                    font=dict(color='white' if abs(value) > 0.5 else 'black'),
                    showarrow=False
                )
            )
    
    # Настройка макета
    fig.update_layout(
        title="Корреляционная матрица",
        font=dict(family="Arial", size=14),
        annotations=annotations,
        height=600,
        width=800,
        template="plotly_white"
    )
    
    return fig