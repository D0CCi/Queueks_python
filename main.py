import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import json
import os
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
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(list(self.queue), f, ensure_ascii=False, indent=2)
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.queue = deque(data)
            except:
                self.queue = deque()

class WagonRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Регистрация вагонов - Система очереди")
        self.root.geometry("800x600")
        
        self.wagon_queue = WagonQueue()
        
        self.setup_ui()
        self.update_queue_display()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        ttk.Label(main_frame, text="Регистрация нового вагона", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Label(main_frame, text="Номер вагона:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.wagon_number_entry = ttk.Entry(main_frame, width=20)
        self.wagon_number_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(main_frame, text="Тип груза:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.cargo_type_entry = ttk.Entry(main_frame, width=20)
        self.cargo_type_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(main_frame, text="Пункт назначения:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.destination_entry = ttk.Entry(main_frame, width=20)
        self.destination_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(main_frame, text="Вес (тонн):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.weight_entry = ttk.Entry(main_frame, width=20)
        self.weight_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Добавить в очередь", command=self.add_wagon).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Обработать следующий", command=self.process_next_wagon).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить форму", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(main_frame, text="Текущая очередь:", font=("Arial", 12, "bold")).grid(row=6, column=0, columnspan=2, pady=(20, 10), sticky=tk.W)
        
        columns = ('position', 'wagon_number', 'cargo_type', 'destination', 'weight', 'timestamp')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=10)
        
        self.tree.heading('position', text='Позиция')
        self.tree.heading('wagon_number', text='Номер вагона')
        self.tree.heading('cargo_type', text='Тип груза')
        self.tree.heading('destination', text='Пункт назначения')
        self.tree.heading('weight', text='Вес (т)')
        self.tree.heading('timestamp', text='Время регистрации')
        
        self.tree.column('position', width=80)
        self.tree.column('wagon_number', width=120)
        self.tree.column('cargo_type', width=120)
        self.tree.column('destination', width=150)
        self.tree.column('weight', width=80)
        self.tree.column('timestamp', width=150)
        
        self.tree.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=7, column=2, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        main_frame.rowconfigure(7, weight=1)
        
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=8, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Готов к работе")
        self.status_label.pack(side=tk.LEFT)
        
        self.queue_count_label = ttk.Label(status_frame, text="Вагонов в очереди: 0")
        self.queue_count_label.pack(side=tk.RIGHT)
    
    def add_wagon(self):
        wagon_number = self.wagon_number_entry.get().strip()
        cargo_type = self.cargo_type_entry.get().strip()
        destination = self.destination_entry.get().strip()
        weight = self.weight_entry.get().strip()
        
        if not all([wagon_number, cargo_type, destination, weight]):
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return
        
        try:
            weight_float = float(weight)
        except ValueError:
            messagebox.showerror("Ошибка", "Вес должен быть числом")
            return
        
        wagon_data = {
            'wagon_number': wagon_number,
            'cargo_type': cargo_type,
            'destination': destination,
            'weight': weight_float
        }
        
        self.wagon_queue.add_wagon(wagon_data)
        self.update_queue_display()
        self.clear_form()
        self.status_label.config(text=f"Вагон {wagon_number} добавлен в очередь")
    
    def process_next_wagon(self):
        wagon = self.wagon_queue.process_next()
        if wagon:
            self.update_queue_display()
            self.status_label.config(text=f"Обработан вагон {wagon['wagon_number']}")
            messagebox.showinfo("Обработка завершена", 
                              f"Вагон {wagon['wagon_number']} успешно обработан\n"
                              f"Груз: {wagon['cargo_type']}\n"
                              f"Направление: {wagon['destination']}")
        else:
            messagebox.showwarning("Очередь пуста", "Нет вагонов для обработки")
    
    def clear_form(self):
        self.wagon_number_entry.delete(0, tk.END)
        self.cargo_type_entry.delete(0, tk.END)
        self.destination_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.wagon_number_entry.focus()
    
    def update_queue_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        queue_list = self.wagon_queue.get_queue_list()
        for wagon in queue_list:
            timestamp = wagon['timestamp'][:19].replace('T', ' ')
            self.tree.insert('', 'end', values=(
                wagon['position'],
                wagon['wagon_number'],
                wagon['cargo_type'],
                wagon['destination'],
                wagon['weight'],
                timestamp
            ))
        
        self.queue_count_label.config(text=f"Вагонов в очереди: {len(queue_list)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WagonRegistrationApp(root)
    root.mainloop()