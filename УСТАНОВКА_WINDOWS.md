# Установка и запуск на Windows

## Требования

- **Windows 10/11** или Windows Server
- **Python 3.7+** (скачать с [python.org](https://python.org))
- **Браузер** (Chrome, Firefox, Edge)

## Быстрая установка

### 1. Автоматическая установка (рекомендуется)

1. Скачайте проект на компьютер
2. Откройте папку проекта в проводнике
3. Запустите файл **`setup_windows.bat`** (двойной клик)
4. Дождитесь завершения установки
5. Запустите **`start_windows.bat`**

### 2. Ручная установка

Откройте **командную строку** (cmd) или **PowerShell** и выполните:

```cmd
# Перейдите в папку проекта
cd путь\к\папке\Queueks_python

# Создайте виртуальное окружение
python -m venv venv

# Активируйте окружение
venv\Scripts\activate.bat

# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
python run.py
```

## Использование

### Запуск приложения

**Способ 1:** Двойной клик на `start_windows.bat`

**Способ 2:** Через командную строку:
```cmd
cd путь\к\проекту
start_windows.bat
```

**Способ 3:** Вручную:
```cmd
cd путь\к\проекту
venv\Scripts\activate.bat
python run.py
```

### Доступ к сайту

После запуска откройте браузер и перейдите по адресу:
```
http://localhost:5000
```

### Тестовые аккаунты

- **Администратор:** `admin` / `admin123`
- **Пользователь:** `test` / `test123`

## Остановка приложения

- Нажмите **Ctrl+C** в окне командной строки
- Или просто закройте окно

## Возможные проблемы

### Python не найден

**Ошибка:** `'python' не является внутренней или внешней командой`

**Решение:**
1. Установите Python с [python.org](https://python.org)
2. При установке отметьте "Add Python to PATH"
3. Перезагрузите компьютер

### Порт занят

**Ошибка:** `Port 5000 is in use`

**Решение:**
1. Закройте другие приложения на порту 5000
2. Или измените порт в файле `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Измените на 5001
```

### Ошибки установки пакетов

**Решение:**
```cmd
# Обновите pip
python -m pip install --upgrade pip

# Установите пакеты заново
pip install -r requirements.txt
```

## Структура файлов для Windows

```
Queueks_python/
├── setup_windows.bat      # Установка для Windows
├── start_windows.bat      # Запуск для Windows
├── setup.sh              # Установка для Linux/Mac
├── start.sh              # Запуск для Linux/Mac
├── app.py                # Основное приложение
├── run.py                # Скрипт запуска
├── requirements.txt      # Зависимости Python
├── venv/                 # Виртуальное окружение
├── instance/
│   └── wagon_queue.db   # База данных
├── templates/           # HTML шаблоны
└── static/             # CSS и JS файлы
```

## Альтернативные версии

### Консольная версия
```cmd
python console_main.py
```

### GUI версия (если установлен tkinter)
```cmd
python main.py
```

## Разработка

Для разработки рекомендуется использовать:
- **VS Code** с расширением Python
- **PyCharm Community Edition**
- **Sublime Text** с плагинами Python

---

**Курсовая работа МГППУ ИТ-МО23 Корнеенков Никита**