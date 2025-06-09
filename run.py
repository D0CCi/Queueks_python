#!/usr/bin/env python3
from app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("База данных инициализирована")
        print("Запуск веб-сервера на http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)