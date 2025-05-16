import pandas as pd
import numpy as np

def process_data(data, filters=None):
    """
    Обрабатывает данные на основе фильтров.
    
    Args:
        data (pd.DataFrame): Исходный DataFrame.
        filters (dict): Словарь фильтров в формате {column: value}.
        
    Returns:
        pd.DataFrame: Обработанный DataFrame.
    """
    if filters is None:
        return data
    
    filtered_data = data.copy()
    
    for column, value in filters.items():
        if column in filtered_data.columns:
            # Для числовых колонок ожидаем диапазон значений
            if filtered_data[column].dtype in [np.int64, np.float64]:
                if isinstance(value, dict) and 'min' in value and 'max' in value:
                    filtered_data = filtered_data[
                        (filtered_data[column] >= value['min']) & 
                        (filtered_data[column] <= value['max'])
                    ]
            # Для категориальных данных ожидаем список значений
            elif isinstance(value, list):
                filtered_data = filtered_data[filtered_data[column].isin(value)]
            # Для строковых данных ожидаем точное совпадение или паттерн
            else:
                filtered_data = filtered_data[filtered_data[column] == value]
    
    return filtered_data

def get_data_summary(data):
    """
    Создает сводку данных, включая основные статистики и информацию о колонках.
    
    Args:
        data (pd.DataFrame): Исходный DataFrame.
        
    Returns:
        dict: Словарь со сводной информацией о данных.
    """
    # Базовая информация
    summary = {
        'rows_count': len(data),
        'columns_count': len(data.columns),
        'columns': list(data.columns),
        'column_types': {},
        'missing_values': {},
        'numeric_stats': {},
        'categorical_stats': {}
    }
    
    # Типы колонок и пропущенные значения
    for column in data.columns:
        dtype_name = str(data[column].dtype)
        summary['column_types'][column] = dtype_name
        summary['missing_values'][column] = int(data[column].isna().sum())
        
        # Статистика для числовых колонок
        if data[column].dtype in [np.int64, np.float64]:
            summary['numeric_stats'][column] = {
                'min': float(data[column].min()),
                'max': float(data[column].max()),
                'mean': float(data[column].mean()),
                'median': float(data[column].median()),
                'std': float(data[column].std())
            }
        # Статистика для категориальных колонок
        else:
            value_counts = data[column].value_counts()
            if len(value_counts) <= 20:  # Ограничиваем количество уникальных значений
                summary['categorical_stats'][column] = {
                    'unique_count': int(len(value_counts)),
                    'top_values': value_counts.head(10).to_dict()
                }
            else:
                summary['categorical_stats'][column] = {
                    'unique_count': int(len(value_counts)),
                    'top_values': value_counts.head(10).to_dict(),
                    'note': 'Показаны только 10 наиболее частых значений'
                }
    
    return summary

def aggregate_data(data, group_by, agg_column, agg_func='mean'):
    """
    Агрегирует данные по указанной колонке с применением функции агрегации.
    
    Args:
        data (pd.DataFrame): Исходный DataFrame.
        group_by (str): Колонка для группировки.
        agg_column (str): Колонка для агрегации.
        agg_func (str): Функция агрегации ('mean', 'sum', 'count', 'min', 'max').
        
    Returns:
        pd.DataFrame: Агрегированный DataFrame.
    """
    if group_by not in data.columns or agg_column not in data.columns:
        raise ValueError("Указанные колонки отсутствуют в данных")
    
    if agg_func == 'mean':
        result = data.groupby(group_by)[agg_column].mean().reset_index()
    elif agg_func == 'sum':
        result = data.groupby(group_by)[agg_column].sum().reset_index()
    elif agg_func == 'count':
        result = data.groupby(group_by)[agg_column].count().reset_index()
    elif agg_func == 'min':
        result = data.groupby(group_by)[agg_column].min().reset_index()
    elif agg_func == 'max':
        result = data.groupby(group_by)[agg_column].max().reset_index()
    else:
        raise ValueError("Неподдерживаемая функция агрегации")
    
    return result

def detect_data_type(data):
    """
    Определяет тип загруженных данных на основе структуры.
    
    Args:
        data (pd.DataFrame): Исходный DataFrame.
        
    Returns:
        str: Тип данных ('табличные', 'временной_ряд', 'другое').
    """
    # Проверка на временной ряд - наличие колонки даты/времени
    date_cols = [col for col in data.columns if data[col].dtype in ['datetime64[ns]', 'object']]
    
    for col in date_cols:
        # Пытаемся преобразовать в дату/время
        try:
            pd.to_datetime(data[col])
            return 'временной_ряд'
        except:
            pass
    
    # Если есть числовые колонки, считаем табличными данными
    numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) > 0:
        return 'табличные'
    
    return 'другое'

def pivot_data(data, index, columns, values, agg_func='mean'):
    """
    Создает сводную таблицу из данных.
    
    Args:
        data (pd.DataFrame): Исходный DataFrame.
        index (str): Колонка для индекса.
        columns (str): Колонка для столбцов.
        values (str): Колонка для значений.
        agg_func (str): Функция агрегации.
        
    Returns:
        pd.DataFrame: Сводная таблица.
    """
    try:
        pivot_table = pd.pivot_table(
            data, 
            values=values, 
            index=index, 
            columns=columns, 
            aggfunc=agg_func
        )
        return pivot_table
    except Exception as e:
        raise ValueError(f"Ошибка при создании сводной таблицы: {str(e)}")