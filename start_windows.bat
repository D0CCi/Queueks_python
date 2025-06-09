@echo off
echo Запуск системы регистрации вагонов (Windows)...

REM Проверяем наличие виртуального окружения
if not exist "venv\Scripts\activate.bat" (
    echo Виртуальное окружение не найдено. Запуск установки...
    call setup_windows.bat
)

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Запуск приложения...
python run.py

pause