/**
 * main.js - Основной JavaScript-файл для системы визуализации научных данных
 */

// Ожидаем полной загрузки документа
document.addEventListener('DOMContentLoaded', function() {
    // Включение всех всплывающих подсказок
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Автоматическое закрытие алертов через 5 секунд
    var alertList = document.querySelectorAll('.alert');
    alertList.forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Функция для преобразования графиков Plotly при изменении размера окна
    function resizePlotlyCharts() {
        const charts = document.querySelectorAll('[id^="plotly-"]');
        if (charts.length > 0) {
            charts.forEach(function(chart) {
                Plotly.relayout(chart, {
                    'xaxis.autorange': true,
                    'yaxis.autorange': true
                });
            });
        }
    }
    
    // Слушатель события изменения размера окна
    window.addEventListener('resize', resizePlotlyCharts);
    
    // Инициализация выпадающих меню
    var dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
    var dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
        return new bootstrap.Dropdown(dropdownToggleEl);
    });
    
    // Функция для локализации дат в русский формат
    function formatDateToRussian(date) {
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit' 
        };
        return date.toLocaleDateString('ru-RU', options);
    }
    
    // Локализация дат на странице
    const dateElements = document.querySelectorAll('.date-localized');
    dateElements.forEach(function(element) {
        const timestamp = parseInt(element.getAttribute('data-timestamp'));
        if (!isNaN(timestamp)) {
            const date = new Date(timestamp * 1000);
            element.textContent = formatDateToRussian(date);
        }
    });
    
    // Обработка кнопки прокрутки вверх
    const scrollTopBtn = document.getElementById('scroll-top-btn');
    if (scrollTopBtn) {
        window.addEventListener('scroll', function() {
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                scrollTopBtn.style.display = 'block';
            } else {
                scrollTopBtn.style.display = 'none';
            }
        });
        
        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Обработка форм с подтверждением
    const confirmForms = document.querySelectorAll('form[data-confirm]');
    confirmForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const confirmMessage = this.getAttribute('data-confirm');
            
            if (confirm(confirmMessage)) {
                this.submit();
            }
        });
    });
    
    // Создание единой настройки для всех графиков Plotly
    window.plotlyConfig = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['sendDataToCloud', 'autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian', 'lasso2d', 'select2d'],
        displaylogo: false,
        locale: 'ru',
        toImageButtonOptions: {
            format: 'png',
            filename: 'научная_визуализация',
            height: 800,
            width: 1200,
            scale: 2
        }
    };
    
    // Настройка локализации Plotly для русского языка
    if (Plotly) {
        Plotly.setPlotConfig({
            locale: 'ru',
            locales: {
                'ru': {
                    dictionary: {
                        'Zoom': 'Увеличить',
                        'Pan': 'Перемещение',
                        'Box Select': 'Выделение области',
                        'Lasso Select': 'Произвольное выделение',
                        'Zoom In': 'Приблизить',
                        'Zoom Out': 'Отдалить',
                        'Reset axes': 'Сбросить оси',
                        'Download plot as a png': 'Скачать как PNG',
                        'Download plot': 'Скачать график',
                        'Downloadable formats': 'Форматы для скачивания',
                        'Snapshot succeeded': 'Снимок создан',
                        'Snapshot failed': 'Ошибка создания снимка',
                        'Transform': 'Трансформировать',
                        'Zoom to fit data': 'Масштабировать по данным',
                        'Toggle Spike Lines': 'Вкл/выкл линии проекции',
                        'Show closest data on hover': 'Показывать ближайшие точки при наведении',
                        'Compare data on hover': 'Сравнивать данные при наведении',
                        'mode': 'ru',
                        'Save to Cloud': 'Сохранить в облако',
                        'Click to toggle trail': 'Нажмите для переключения',
                        'Press Shift for pan': 'Нажмите Shift для перемещения',
                        'Click to toggle trace': 'Нажмите для переключения ряда',
                        'Double-click to zoom back out': 'Двойной клик для возврата масштаба',
                        'Click to enter selected data point': 'Нажмите для выбора точки данных',
                        'Click to enter transform': 'Нажмите для ввода преобразования',
                        'Click to toggle showing extra data': 'Нажмите для отображения доп. данных',
                        'Click to make this subseries visible': 'Нажмите для отображения подсерии'
                    },
                    format: {
                        days: ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'],
                        shortDays: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
                        months: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
                        shortMonths: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
                        date: '%d.%m.%Y'
                    }
                }
            }
        });
    }
    
    // Обработка форм визуализации с задержкой отправки
    const vizForms = document.querySelectorAll('form[data-viz-form]');
    vizForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Обработка...';
            }
        });
    });
    
    // Динамическое изменение интерфейса в зависимости от выбранных опций
    const columnSelects = document.querySelectorAll('select[data-column-type]');
    columnSelects.forEach(function(select) {
        select.addEventListener('change', function() {
            const columnType = this.getAttribute('data-column-type');
            const dependentSelects = document.querySelectorAll(`select[data-depends-on="${columnType}"]`);
            
            dependentSelects.forEach(function(depSelect) {
                const dependsValue = depSelect.getAttribute('data-depends-value');
                const selectedValue = select.value;
                
                if (dependsValue === selectedValue || dependsValue === '*') {
                    depSelect.closest('.form-group').style.display = 'block';
                } else {
                    depSelect.closest('.form-group').style.display = 'none';
                }
            });
        });
    });
    
    // Предпросмотр выбранного файла
    const filePreviewInputs = document.querySelectorAll('input[type="file"][data-preview]');
    filePreviewInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const previewContainer = document.getElementById(this.getAttribute('data-preview'));
            if (!previewContainer) return;
            
            const file = this.files[0];
            if (!file) {
                previewContainer.innerHTML = '<p class="text-muted">Файл не выбран</p>';
                return;
            }
            
            // Для текстовых файлов (CSV, JSON)
            if (file.type === 'text/csv' || file.type === 'application/json' || file.name.endsWith('.csv') || file.name.endsWith('.json')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let content = e.target.result;
                    // Ограничиваем количество строк для предпросмотра
                    const lines = content.split('\n').slice(0, 10);
                    content = lines.join('\n');
                    
                    previewContainer.innerHTML = `
                        <div class="alert alert-info">
                            <p><strong>Предпросмотр файла:</strong> ${file.name}</p>
                            <pre class="mb-0" style="max-height: 200px; overflow-y: auto;">${content}</pre>
                        </div>
                    `;
                };
                reader.readAsText(file);
            } else {
                previewContainer.innerHTML = `
                    <div class="alert alert-warning">
                        <p>Выбран файл неподдерживаемого формата: ${file.name}</p>
                        <p>Поддерживаются только файлы CSV и JSON.</p>
                    </div>
                `;
            }
        });
    });
});