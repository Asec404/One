from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
import json
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Файл для хранения данных
DATA_FILE = 'data.json'

def load_data():
    """Загружает данные из JSON файла"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'users': [],
        'equipment': [],
        'inspections': []
    }

def save_data(data):
    """Сохраняет данные в JSON файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

def get_user_by_username(username):
    """Находит пользователя по имени"""
    data = load_data()
    for user in data['users']:
        if user['username'] == username:
            return user
    return None

def get_equipment_by_id(equipment_id):
    """Находит оборудование по ID"""
    data = load_data()
    for equipment in data['equipment']:
        if equipment['id'] == equipment_id:
            return equipment
    return None

def get_inspections_by_equipment(equipment_id):
    """Находит проверки для оборудования"""
    data = load_data()
    return [i for i in data['inspections'] if i['equipment_id'] == equipment_id]

# Инициализация данных при первом запуске
def init_data():
    data = load_data()
    if not data['users']:
        # Создаем администратора по умолчанию
        admin = {
            'id': str(uuid.uuid4()),
            'username': 'admin',
            'password': 'admin123',
            'name': 'Администратор',
            'role': 'admin'
        }
        data['users'].append(admin)
        save_data(data)

@app.template_filter('format_dt')
def format_dt(value, fmt='%d.%m.%Y'):
    if not value:
        return ''
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime(fmt)
    except Exception:
        return value

# Маршруты
@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    equipment_count = len(data['equipment'])
    pending_inspections = len([i for i in data['inspections'] if i['status'] == 'pending'])
    overdue_inspections = 0  # Упрощенная логика
    
    recent_inspections = sorted(data['inspections'], 
                               key=lambda x: x.get('inspection_date', ''), 
                               reverse=True)[:5]
    
    return render_template('dashboard.html', 
                         equipment_count=equipment_count,
                         pending_inspections=pending_inspections,
                         overdue_inspections=overdue_inspections,
                         recent_inspections=recent_inspections)

@app.route('/equipment')
def equipment_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    return render_template('equipment_list.html', equipment=data['equipment'])

@app.route('/equipment/add', methods=['GET', 'POST'])
def add_equipment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = load_data()
        equipment = {
            'id': str(uuid.uuid4()),
            'name': request.form['name'],
            'model': request.form['model'],
            'serial_number': request.form['serial_number'],
            'location': request.form['location'],
            'status': request.form.get('status', 'active'),
            'last_inspection': None,
            'next_inspection': request.form.get('next_inspection'),
            'inspector_id': session['user_id'],
            'notes': request.form.get('notes', '')
        }
        data['equipment'].append(equipment)
        save_data(data)
        flash('Оборудование добавлено успешно!', 'success')
        return redirect(url_for('equipment_list'))
    
    return render_template('add_equipment.html')

@app.route('/inspection/<equipment_id>')
def inspection_form(equipment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    equipment = get_equipment_by_id(equipment_id)
    if not equipment:
        flash('Оборудование не найдено!', 'error')
        return redirect(url_for('equipment_list'))
    
    return render_template('inspection_form.html', equipment=equipment)

@app.route('/inspection/submit', methods=['POST'])
def submit_inspection():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    equipment_id = request.form['equipment_id']
    result = request.form['result']
    notes = request.form['notes']
    checklist_data = request.form.get('checklist_data', '{}')
    
    inspection = {
        'id': str(uuid.uuid4()),
        'equipment_id': equipment_id,
        'inspector_id': session['user_id'],
        'inspection_date': datetime.now().isoformat(),
        'status': 'completed',
        'result': result,
        'notes': notes,
        'checklist_data': checklist_data
    }
    
    data['inspections'].append(inspection)
    
    # Обновляем дату последней проверки оборудования
    for equipment in data['equipment']:
        if equipment['id'] == equipment_id:
            equipment['last_inspection'] = datetime.now().isoformat()
            break
    
    save_data(data)
    flash('Проверка завершена успешно!', 'success')
    return redirect(url_for('equipment_list'))

@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    inspections = sorted(data['inspections'], 
                        key=lambda x: x.get('inspection_date', ''), 
                        reverse=True)
    return render_template('reports.html', inspections=inspections)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            flash('Неверные учетные данные!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# API маршруты для получения данных
@app.route('/api/equipment/<equipment_id>')
def get_equipment_details(equipment_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    equipment = get_equipment_by_id(equipment_id)
    if equipment:
        inspections = get_inspections_by_equipment(equipment_id)
        return jsonify({
            'equipment': equipment,
            'inspections_count': len(inspections),
            'last_inspection': equipment.get('last_inspection'),
            'status': equipment['status']
        })
    return jsonify({'error': 'Equipment not found'}), 404

@app.route('/equipment/edit/<equipment_id>', methods=['GET', 'POST'])
def edit_equipment(equipment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    data = load_data()
    equipment = next((e for e in data['equipment'] if e['id'] == equipment_id), None)
    if not equipment:
        flash('Оборудование не найдено!', 'error')
        return redirect(url_for('equipment_list'))
    if request.method == 'POST':
        equipment['name'] = request.form['name']
        equipment['model'] = request.form['model']
        equipment['serial_number'] = request.form['serial_number']
        equipment['location'] = request.form['location']
        equipment['status'] = request.form.get('status', 'active')
        equipment['next_inspection'] = request.form.get('next_inspection')
        equipment['notes'] = request.form.get('notes', '')
        save_data(data)
        flash('Оборудование успешно обновлено!', 'success')
        return redirect(url_for('equipment_list'))
    return render_template('edit_equipment.html', equipment=equipment)

if __name__ == '__main__':
    init_data()
    # Поддержка переменных окружения для Render
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 