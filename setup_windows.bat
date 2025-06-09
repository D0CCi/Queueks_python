@echo off
echo Настройка виртуального окружения для системы регистрации вагонов (Windows)...

REM Проверяем наличие Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не найден в системе!
    echo Скачайте и установите Python с https://python.org
    pause
    exit /b 1
)

REM Создаем виртуальное окружение
echo Создание виртуального окружения...
python -m venv venv

REM Активируем виртуальное окружение
echo Активация виртуального окружения...
call venv\Scripts\activate.bat

REM Обновляем pip
echo Обновление pip...
python -m pip install --upgrade pip

REM Устанавливаем зависимости
echo Установка зависимостей...
pip install -r requirements.txt

echo.
echo ✅ Установка завершена!
echo.
echo Для запуска приложения выполните:
echo   start_windows.bat
echo.
echo Или вручную:
echo   venv\Scripts\activate.bat
echo   python run.py
echo.
pause