import json
import uuid
from datetime import datetime, timedelta
import random

def create_demo_data():
    # Загружаем существующие данные или создаем новые
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {
            'users': [],
            'equipment': [],
            'inspections': []
        }
    
    # Создаем дополнительных пользователей
    users_data = [
        {'username': 'inspector1', 'password': 'pass123', 'name': 'Иванов И.И.', 'role': 'inspector'},
        {'username': 'inspector2', 'password': 'pass123', 'name': 'Петров П.П.', 'role': 'inspector'},
        {'username': 'manager', 'password': 'pass123', 'name': 'Сидоров С.С.', 'role': 'manager'},
    ]
    
    for user_data in users_data:
        if not any(u['username'] == user_data['username'] for u in data['users']):
            user = {
                'id': str(uuid.uuid4()),
                **user_data
            }
            data['users'].append(user)
    
    # Создаем демонстрационное оборудование
    equipment_data = [
        {
            'name': 'Токарный станок ТС-1',
            'model': 'ТС-1М',
            'serial_number': 'TS001-2024',
            'location': 'Цех №1, участок А',
            'status': 'active',
            'inspector_id': data['users'][0]['id'] if data['users'] else None
        },
        {
            'name': 'Фрезерный станок ФС-2',
            'model': 'ФС-2П',
            'serial_number': 'FS002-2024',
            'location': 'Цех №1, участок Б',
            'status': 'active',
            'inspector_id': data['users'][0]['id'] if data['users'] else None
        },
        {
            'name': 'Сварочный аппарат СА-3',
            'model': 'СА-3М',
            'serial_number': 'SA003-2024',
            'location': 'Цех №2, участок В',
            'status': 'maintenance',
            'inspector_id': data['users'][1]['id'] if len(data['users']) > 1 else None
        },
        {
            'name': 'Компрессор К-4',
            'model': 'К-4П',
            'serial_number': 'CP004-2024',
            'location': 'Компрессорная',
            'status': 'active',
            'inspector_id': data['users'][1]['id'] if len(data['users']) > 1 else None
        },
        {
            'name': 'Кран мостовой КМ-5',
            'model': 'КМ-5Т',
            'serial_number': 'CR005-2024',
            'location': 'Цех №3',
            'status': 'active',
            'inspector_id': data['users'][0]['id'] if data['users'] else None
        },
        {
            'name': 'Конвейер КВ-6',
            'model': 'КВ-6Л',
            'serial_number': 'CV006-2024',
            'location': 'Цех №2, линия 1',
            'status': 'active',
            'inspector_id': data['users'][1]['id'] if len(data['users']) > 1 else None
        }
    ]
    
    for eq_data in equipment_data:
        if not any(e['serial_number'] == eq_data['serial_number'] for e in data['equipment']):
            equipment = {
                'id': str(uuid.uuid4()),
                'last_inspection': None,
                'next_inspection': None,
                'notes': '',
                **eq_data
            }
            data['equipment'].append(equipment)
    
    # Создаем демонстрационные проверки
    inspection_results = ['passed', 'failed']
    checklist_items = [
        'visual_inspection', 'power_supply', 'safety_devices',
        'calibration', 'documentation', 'cleanliness'
    ]
    
    for equipment in data['equipment']:
        # Создаем несколько проверок для каждого оборудования
        for i in range(random.randint(1, 3)):
            inspection_date = datetime.now() - timedelta(days=random.randint(1, 30))
            result = random.choice(inspection_results)
            
            # Создаем случайный чек-лист
            selected_checks = random.sample(checklist_items, random.randint(3, 6))
            checklist_data = ','.join(selected_checks)
            
            inspection = {
                'id': str(uuid.uuid4()),
                'equipment_id': equipment['id'],
                'inspector_id': equipment['inspector_id'],
                'inspection_date': inspection_date.isoformat(),
                'status': 'completed',
                'result': result,
                'notes': f'Демонстрационная проверка #{i+1}. ' + 
                        ('Оборудование работает нормально.' if result == 'passed' else 'Обнаружены незначительные замечания.'),
                'checklist_data': checklist_data
            }
            
            data['inspections'].append(inspection)
            
            # Обновляем дату последней проверки оборудования
            if not equipment['last_inspection'] or inspection_date.isoformat() > equipment['last_inspection']:
                equipment['last_inspection'] = inspection_date.isoformat()
    
    # Сохраняем данные
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    print("Демонстрационные данные успешно созданы!")
    print(f"Создано пользователей: {len(data['users'])}")
    print(f"Создано оборудования: {len(data['equipment'])}")
    print(f"Создано проверок: {len(data['inspections'])}")

if __name__ == '__main__':
    create_demo_data() 