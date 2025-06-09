#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from collections import deque
from datetime import datetime

class WagonQueue:
    def __init__(self):
        self.queue = deque()
        self.data_file = "wagon_queue.json"
        self.load_data()
    
    def add_wagon(self, wagon_data):
        wagon_data['timestamp'] = datetime.now().isoformat()
        wagon_data['position'] = len(self.queue) + 1
        self.queue.append(wagon_data)
        self.save_data()
        print(f"✓ Вагон {wagon_data['wagon_number']} добавлен в очередь (позиция {wagon_data['position']})")
    
    def process_next(self):
        if self.queue:
            wagon = self.queue.popleft()
            self.update_positions()
            self.save_data()
            return wagon
        return None
    
    def update_positions(self):
        for i, wagon in enumerate(self.queue):
            wagon['position'] = i + 1
    
    def get_queue_list(self):
        return list(self.queue)
    
    def get_queue_size(self):
        return len(self.queue)
    
    def save_data(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.queue), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.queue = deque(data)
                print(f"Загружено {len(self.queue)} вагонов из файла")
            except Exception as e:
                print(f"Ошибка загрузки данных: {e}")
                self.queue = deque()
        else:
            self.queue = deque()

class WagonRegistrationSystem:
    def __init__(self):
        self.wagon_queue = WagonQueue()
        
    def show_menu(self):
        print("\n" + "="*60)
        print("           СИСТЕМА РЕГИСТРАЦИИ ВАГОНОВ")
        print("="*60)
        print("1. Добавить новый вагон в очередь")
        print("2. Обработать следующий вагон")
        print("3. Показать текущую очередь")
        print("4. Показать статистику")
        print("5. Выход")
        print("="*60)
        
    def add_wagon(self):
        print("\n--- РЕГИСТРАЦИЯ НОВОГО ВАГОНА ---")
        
        try:
            wagon_number = input("Номер вагона: ").strip()
            if not wagon_number:
                print("❌ Номер вагона не может быть пустым")
                return
                
            cargo_type = input("Тип груза: ").strip()
            if not cargo_type:
                print("❌ Тип груза не может быть пустым")
                return
                
            destination = input("Пункт назначения: ").strip()
            if not destination:
                print("❌ Пункт назначения не может быть пустым")
                return
                
            weight_str = input("Вес груза (тонн): ").strip()
            if not weight_str:
                print("❌ Вес не может быть пустым")
                return
                
            weight = float(weight_str)
            if weight <= 0:
                print("❌ Вес должен быть положительным числом")
                return
                
        except ValueError:
            print("❌ Вес должен быть числом")
            return
        except KeyboardInterrupt:
            print("\n❌ Регистрация отменена")
            return
            
        wagon_data = {
            'wagon_number': wagon_number,
            'cargo_type': cargo_type,
            'destination': destination,
            'weight': weight
        }
        
        self.wagon_queue.add_wagon(wagon_data)
        
    def process_next_wagon(self):
        print("\n--- ОБРАБОТКА СЛЕДУЮЩЕГО ВАГОНА ---")
        
        wagon = self.wagon_queue.process_next()
        if wagon:
            print("✓ Вагон успешно обработан:")
            print(f"  Номер: {wagon['wagon_number']}")
            print(f"  Груз: {wagon['cargo_type']}")
            print(f"  Направление: {wagon['destination']}")
            print(f"  Вес: {wagon['weight']} тонн")
            print(f"  Зарегистрирован: {wagon['timestamp'][:19].replace('T', ' ')}")
        else:
            print("❌ Очередь пуста - нет вагонов для обработки")
            
    def show_queue(self):
        print("\n--- ТЕКУЩАЯ ОЧЕРЕДЬ ВАГОНОВ ---")
        
        queue_list = self.wagon_queue.get_queue_list()
        if not queue_list:
            print("Очередь пуста")
            return
            
        print(f"{'Поз':<4} {'Номер':<12} {'Груз':<15} {'Направление':<20} {'Вес(т)':<8} {'Время регистрации'}")
        print("-" * 80)
        
        for wagon in queue_list:
            timestamp = wagon['timestamp'][:19].replace('T', ' ')
            print(f"{wagon['position']:<4} {wagon['wagon_number']:<12} {wagon['cargo_type']:<15} "
                  f"{wagon['destination']:<20} {wagon['weight']:<8} {timestamp}")
                  
    def show_statistics(self):
        print("\n--- СТАТИСТИКА СИСТЕМЫ ---")
        queue_size = self.wagon_queue.get_queue_size()
        print(f"Вагонов в очереди: {queue_size}")
        
        if queue_size > 0:
            queue_list = self.wagon_queue.get_queue_list()
            total_weight = sum(wagon['weight'] for wagon in queue_list)
            print(f"Общий вес груза: {total_weight:.1f} тонн")
            print(f"Средний вес вагона: {total_weight/queue_size:.1f} тонн")
            
            cargo_types = {}
            for wagon in queue_list:
                cargo_type = wagon['cargo_type']
                cargo_types[cargo_type] = cargo_types.get(cargo_type, 0) + 1
                
            print("\nТипы грузов:")
            for cargo_type, count in cargo_types.items():
                print(f"  {cargo_type}: {count} вагон(ов)")
        
    def run(self):
        print("Добро пожаловать в систему регистрации вагонов!")
        
        while True:
            try:
                self.show_menu()
                choice = input("\nВыберите действие (1-5): ").strip()
                
                if choice == '1':
                    self.add_wagon()
                elif choice == '2':
                    self.process_next_wagon()
                elif choice == '3':
                    self.show_queue()
                elif choice == '4':
                    self.show_statistics()
                elif choice == '5':
                    print("\nДо свидания! Данные сохранены.")
                    break
                else:
                    print("❌ Неверный выбор. Выберите число от 1 до 5.")
                    
            except KeyboardInterrupt:
                print("\n\nВыход из программы. Данные сохранены.")
                break
            except Exception as e:
                print(f"❌ Произошла ошибка: {e}")

if __name__ == "__main__":
    system = WagonRegistrationSystem()
    system.run()