from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///equipment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Модели данных
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='inspector')

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    model = db.Column(db.String(100))
    serial_number = db.Column(db.String(100), unique=True)
    location = db.Column(db.String(200))
    status = db.Column(db.String(20), default='active')
    last_inspection = db.Column(db.DateTime)
    next_inspection = db.Column(db.DateTime)
    inspector_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notes = db.Column(db.Text)

class Inspection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    inspector_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    inspection_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
    result = db.Column(db.String(20))
    notes = db.Column(db.Text)
    checklist_data = db.Column(db.Text)  # JSON данные чек-листа

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Маршруты
@app.route('/')
@login_required
def dashboard():
    equipment_count = Equipment.query.count()
    pending_inspections = Inspection.query.filter_by(status='pending').count()
    overdue_inspections = Inspection.query.filter(
        Inspection.next_inspection < datetime.utcnow()
    ).count()
    
    recent_inspections = Inspection.query.order_by(
        Inspection.inspection_date.desc()
    ).limit(5).all()
    
    return render_template('dashboard.html', 
                         equipment_count=equipment_count,
                         pending_inspections=pending_inspections,
                         overdue_inspections=overdue_inspections,
                         recent_inspections=recent_inspections)

@app.route('/equipment')
@login_required
def equipment_list():
    equipment = Equipment.query.all()
    return render_template('equipment_list.html', equipment=equipment)

@app.route('/equipment/add', methods=['GET', 'POST'])
@login_required
def add_equipment():
    if request.method == 'POST':
        equipment = Equipment(
            name=request.form['name'],
            model=request.form['model'],
            serial_number=request.form['serial_number'],
            location=request.form['location'],
            inspector_id=current_user.id
        )
        db.session.add(equipment)
        db.session.commit()
        flash('Оборудование добавлено успешно!', 'success')
        return redirect(url_for('equipment_list'))
    
    return render_template('add_equipment.html')

@app.route('/inspection/<int:equipment_id>')
@login_required
def inspection_form(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    return render_template('inspection_form.html', equipment=equipment)

@app.route('/inspection/submit', methods=['POST'])
@login_required
def submit_inspection():
    equipment_id = request.form['equipment_id']
    result = request.form['result']
    notes = request.form['notes']
    checklist_data = request.form.get('checklist_data', '{}')
    
    inspection = Inspection(
        equipment_id=equipment_id,
        inspector_id=current_user.id,
        result=result,
        notes=notes,
        checklist_data=checklist_data
    )
    
    # Обновляем статус оборудования
    equipment = Equipment.query.get(equipment_id)
    equipment.last_inspection = datetime.utcnow()
    
    db.session.add(inspection)
    db.session.commit()
    
    flash('Проверка завершена успешно!', 'success')
    return redirect(url_for('equipment_list'))

@app.route('/reports')
@login_required
def reports():
    inspections = Inspection.query.order_by(Inspection.inspection_date.desc()).all()
    return render_template('reports.html', inspections=inspections)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:  # В реальном проекте используйте хеширование
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Неверные учетные данные!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Создаем тестового пользователя, если его нет
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password='admin123', name='Администратор', role='admin')
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True) 