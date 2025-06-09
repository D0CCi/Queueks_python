from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wagon-queue-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wagon_queue.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице.'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    company_name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    wagons = db.relationship('Wagon', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Wagon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wagon_number = db.Column(db.String(50), nullable=False)
    cargo_type = db.Column(db.String(100), nullable=False)
    departure_point = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='в_очереди')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'wagon_number': self.wagon_number,
            'cargo_type': self.cargo_type,
            'departure_point': self.departure_point,
            'destination': self.destination,
            'weight': self.weight,
            'position': self.position,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'owner': self.owner.company_name or self.owner.username,
            'user_id': self.user_id
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    company_name = StringField('Название компании', validators=[Length(max=200)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

class WagonForm(FlaskForm):
    wagon_number = StringField('Номер вагона', validators=[DataRequired()])
    cargo_type = StringField('Тип груза', validators=[DataRequired()])
    departure_point = StringField('Пункт отправки', validators=[DataRequired()])
    destination = StringField('Пункт назначения', validators=[DataRequired()])
    weight = FloatField('Вес груза (тонн)', validators=[DataRequired(), NumberRange(min=0.1)])
    submit = SubmitField('Добавить в очередь')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'Добро пожаловать, {user.username}!', 'success')
            return redirect(url_for('index'))
        flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Пользователь с таким именем уже существует', 'error')
            return render_template('auth/register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Пользователь с таким email уже существует', 'error')
            return render_template('auth/register.html', form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            company_name=form.company_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь вы можете войти в систему.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    all_wagons = Wagon.query.filter_by(status='в_очереди').order_by(Wagon.position).all()
    user_wagons = [w for w in all_wagons if w.user_id == current_user.id]
    form = WagonForm()
    return render_template('index.html', wagons=all_wagons, user_wagons=user_wagons, form=form)

@app.route('/add_wagon', methods=['POST'])
@login_required
def add_wagon():
    form = WagonForm()
    
    if form.validate_on_submit():
        existing_wagon = Wagon.query.filter_by(
            wagon_number=form.wagon_number.data, 
            status='в_очереди'
        ).first()
        
        if existing_wagon:
            flash(f'Вагон {form.wagon_number.data} уже находится в очереди', 'error')
            return redirect(url_for('index'))
        
        max_position = db.session.query(db.func.max(Wagon.position)).filter_by(status='в_очереди').scalar() or 0
        
        new_wagon = Wagon(
            wagon_number=form.wagon_number.data,
            cargo_type=form.cargo_type.data,
            departure_point=form.departure_point.data,
            destination=form.destination.data,
            weight=form.weight.data,
            position=max_position + 1,
            user_id=current_user.id
        )
        
        db.session.add(new_wagon)
        db.session.commit()
        
        flash(f'Вагон {new_wagon.wagon_number} добавлен в очередь (позиция {new_wagon.position})', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'error')
    
    return redirect(url_for('index'))

@app.route('/process_next', methods=['POST'])
@login_required
def process_next():
    if not current_user.username == 'admin':
        flash('Только администратор может обрабатывать вагоны', 'error')
        return redirect(url_for('index'))
    
    try:
        next_wagon = Wagon.query.filter_by(status='в_очереди').order_by(Wagon.position).first()
        
        if not next_wagon:
            flash('Очередь пуста - нет вагонов для обработки', 'warning')
            return redirect(url_for('index'))
        
        next_wagon.status = 'обработан'
        
        remaining_wagons = Wagon.query.filter_by(status='в_очереди').filter(Wagon.position > next_wagon.position).all()
        for wagon in remaining_wagons:
            wagon.position -= 1
        
        db.session.commit()
        
        flash(f'Вагон {next_wagon.wagon_number} (владелец: {next_wagon.owner.company_name or next_wagon.owner.username}) успешно обработан', 'success')
        
    except Exception as e:
        flash(f'Произошла ошибка: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_wagons_in_queue = Wagon.query.filter_by(user_id=current_user.id, status='в_очереди').order_by(Wagon.position).all()
    user_wagons_processed = Wagon.query.filter_by(user_id=current_user.id, status='обработан').order_by(Wagon.timestamp.desc()).all()
    
    total_weight_queue = sum(w.weight for w in user_wagons_in_queue)
    total_weight_processed = sum(w.weight for w in user_wagons_processed)
    
    return render_template('dashboard.html', 
                         wagons_in_queue=user_wagons_in_queue,
                         wagons_processed=user_wagons_processed,
                         total_weight_queue=total_weight_queue,
                         total_weight_processed=total_weight_processed)

@app.route('/api/queue')
@login_required
def api_queue():
    wagons = Wagon.query.filter_by(status='в_очереди').order_by(Wagon.position).all()
    return jsonify([wagon.to_dict() for wagon in wagons])

@app.route('/api/user_stats')
@login_required
def api_user_stats():
    user_in_queue = Wagon.query.filter_by(user_id=current_user.id, status='в_очереди').count()
    user_processed = Wagon.query.filter_by(user_id=current_user.id, status='обработан').count()
    
    if user_in_queue > 0:
        user_weight = db.session.query(db.func.sum(Wagon.weight)).filter_by(
            user_id=current_user.id, status='в_очереди'
        ).scalar() or 0
    else:
        user_weight = 0
    
    total_in_queue = Wagon.query.filter_by(status='в_очереди').count()
    
    return jsonify({
        'user_in_queue': user_in_queue,
        'user_processed': user_processed,
        'user_weight': round(user_weight, 1),
        'total_in_queue': total_in_queue,
        'user_position': min([w.position for w in Wagon.query.filter_by(user_id=current_user.id, status='в_очереди').all()]) if user_in_queue > 0 else None
    })

@app.route('/history')
@login_required
def history():
    if current_user.username == 'admin':
        processed_wagons = Wagon.query.filter_by(status='обработан').order_by(Wagon.timestamp.desc()).all()
    else:
        processed_wagons = Wagon.query.filter_by(user_id=current_user.id, status='обработан').order_by(Wagon.timestamp.desc()).all()
    
    return render_template('history.html', wagons=processed_wagons)

@app.route('/clear_queue', methods=['POST'])
@login_required
def clear_queue():
    if not current_user.username == 'admin':
        flash('Только администратор может очищать очередь', 'error')
        return redirect(url_for('index'))
    
    try:
        Wagon.query.filter_by(status='в_очереди').delete()
        db.session.commit()
        flash('Очередь очищена', 'success')
    except Exception as e:
        flash(f'Ошибка очистки очереди: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Создаем администратора, если его нет
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@wagon-queue.com',
                company_name='Администрация'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Создан администратор: admin / admin123")
    
    app.run(debug=True, host='0.0.0.0', port=5000)