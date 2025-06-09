#!/bin/bash

echo "Настройка виртуального окружения для системы регистрации вагонов..."

# Создаем виртуальное окружение
python -m venv venv

# Активируем виртуальное окружение
source venv/bin/activate

# Обновляем pip
pip install --upgrade pip

# Устанавливаем зависимости
pip install -r requirements.txt

echo ""
echo "✅ Установка завершена!"
echo ""
echo "Для запуска приложения выполните:"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "Или используйте скрипт запуска:"
echo "  ./start.sh"