// Основной JavaScript для приложения
class WagonQueueApp {
    constructor() {
        this.initializeApp();
        this.setupEventListeners();
        this.startAutoRefresh();
    }

    initializeApp() {
        console.log('Инициализация приложения системы регистрации вагонов');
        this.updateTimestamps();
    }

    setupEventListeners() {
        // Автообновление статистики
        this.setupStatsRefresh();
        
        // Обработка формы
        this.setupFormHandling();
        
        // Горячие клавиши
        this.setupKeyboardShortcuts();
    }

    setupStatsRefresh() {
        const refreshStats = () => {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    this.updateStatsDisplay(data);
                })
                .catch(error => {
                    console.error('Ошибка обновления статистики:', error);
                });
        };

        // Обновление каждые 30 секунд
        setInterval(refreshStats, 30000);
    }

    updateStatsDisplay(data) {
        const queueCountElement = document.getElementById('queueCount');
        const totalWeightElement = document.getElementById('totalWeight');
        
        if (queueCountElement) {
            queueCountElement.textContent = data.total_in_queue;
        }
        
        if (totalWeightElement) {
            totalWeightElement.textContent = data.total_weight;
        }

        // Обновление заголовка страницы
        document.title = `(${data.total_in_queue}) Система регистрации вагонов`;
    }

    setupFormHandling() {
        const form = document.getElementById('wagonForm');
        if (form) {
            form.addEventListener('submit', (e) => {
                this.handleFormSubmit(e);
            });

            // Автофокус на первое поле
            const firstInput = form.querySelector('input');
            if (firstInput) {
                firstInput.focus();
            }
        }
    }

    handleFormSubmit(e) {
        const form = e.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        
        // Отключаем кнопку и показываем загрузку
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Добавление...';
        }

        // Валидация формы
        if (!this.validateForm(form)) {
            e.preventDefault();
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-plus"></i> Добавить в очередь';
            }
            return;
        }
    }

    validateForm(form) {
        const wagonNumber = form.querySelector('#wagon_number').value.trim();
        const cargoType = form.querySelector('#cargo_type').value.trim();
        const destination = form.querySelector('#destination').value.trim();
        const weight = form.querySelector('#weight').value.trim();

        if (!wagonNumber || !cargoType || !destination || !weight) {
            this.showAlert('Все поля должны быть заполнены', 'error');
            return false;
        }

        const weightNum = parseFloat(weight);
        if (isNaN(weightNum) || weightNum <= 0) {
            this.showAlert('Вес должен быть положительным числом', 'error');
            return false;
        }

        return true;
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl + Enter - отправка формы
            if (e.ctrlKey && e.key === 'Enter') {
                const form = document.getElementById('wagonForm');
                if (form) {
                    form.submit();
                }
            }

            // Ctrl + P - обработка следующего вагона
            if (e.ctrlKey && e.key === 'p') {
                e.preventDefault();
                this.processNextWagon();
            }

            // Ctrl + R - обновление очереди
            if (e.ctrlKey && e.key === 'r') {
                e.preventDefault();
                this.refreshQueue();
            }
        });
    }

    processNextWagon() {
        if (confirm('Обработать следующий вагон в очереди?')) {
            fetch('/process_next', {
                method: 'POST',
            })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    this.showAlert('Ошибка обработки вагона', 'error');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                this.showAlert('Ошибка сети', 'error');
            });
        }
    }

    refreshQueue() {
        const refreshBtn = document.querySelector('[onclick="refreshQueue()"]');
        if (refreshBtn) {
            refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Обновление...';
            refreshBtn.disabled = true;
        }

        setTimeout(() => {
            location.reload();
        }, 500);
    }

    startAutoRefresh() {
        // Автообновление страницы каждые 5 минут
        setInterval(() => {
            if (document.visibilityState === 'visible') {
                this.refreshQueueData();
            }
        }, 300000); // 5 минут
    }

    refreshQueueData() {
        fetch('/api/queue')
            .then(response => response.json())
            .then(data => {
                this.updateQueueTable(data);
            })
            .catch(error => {
                console.error('Ошибка обновления очереди:', error);
            });
    }

    updateQueueTable(wagons) {
        const tbody = document.getElementById('queueTableBody');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (wagons.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center py-4">
                        <i class="fas fa-inbox fa-2x text-muted mb-2"></i>
                        <p class="text-muted mb-0">Очередь пуста</p>
                    </td>
                </tr>
            `;
            return;
        }

        wagons.forEach(wagon => {
            const row = this.createTableRow(wagon);
            tbody.appendChild(row);
        });
    }

    createTableRow(wagon) {
        const row = document.createElement('tr');
        row.className = wagon.position === 1 ? 'table-warning' : '';

        row.innerHTML = `
            <td>
                <span class="badge bg-${wagon.position === 1 ? 'warning' : 'secondary'}">
                    ${wagon.position}
                </span>
            </td>
            <td><strong>${wagon.wagon_number}</strong></td>
            <td>${wagon.cargo_type}</td>
            <td>${wagon.destination}</td>
            <td>${wagon.weight}</td>
            <td>${this.formatTimestamp(wagon.timestamp)}</td>
        `;

        return row;
    }

    updateTimestamps() {
        const timestamps = document.querySelectorAll('[data-timestamp]');
        timestamps.forEach(element => {
            const timestamp = element.getAttribute('data-timestamp');
            element.textContent = this.formatTimestamp(timestamp);
        });
    }

    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString('ru-RU', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    showAlert(message, type = 'info') {
        // Создаем алерт
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'info-circle'}"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Вставляем в начало контейнера
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
        }

        // Автоудаление через 5 секунд
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// Инициализация приложения при загрузке DOM
document.addEventListener('DOMContentLoaded', () => {
    new WagonQueueApp();
});

// Глобальные функции для совместимости с HTML
window.processNext = function() {
    if (window.app) {
        window.app.processNextWagon();
    } else {
        // Fallback
        if (confirm('Обработать следующий вагон в очереди?')) {
            fetch('/process_next', { method: 'POST' })
                .then(() => location.reload());
        }
    }
};

window.refreshQueue = function() {
    if (window.app) {
        window.app.refreshQueue();
    } else {
        location.reload();
    }
};