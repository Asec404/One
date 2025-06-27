from app import app, db, User, Equipment, Inspection
from datetime import datetime, timedelta
import random

def create_demo_data():
    with app.app_context():
        # Создаем дополнительных пользователей
        users_data = [
            {'username': 'inspector1', 'password': 'pass123', 'name': 'Иванов И.И.', 'role': 'inspector'},
            {'username': 'inspector2', 'password': 'pass123', 'name': 'Петров П.П.', 'role': 'inspector'},
            {'username': 'manager', 'password': 'pass123', 'name': 'Сидоров С.С.', 'role': 'manager'},
        ]
        
        for user_data in users_data:
            if not User.query.filter_by(username=user_data['username']).first():
                user = User(**user_data)
                db.session.add(user)
        
        # Создаем демонстрационное оборудование
        equipment_data = [
            {
                'name': 'Токарный станок ТС-1',
                'model': 'ТС-1М',
                'serial_number': 'TS001-2024',
                'location': 'Цех №1, участок А',
                'status': 'active',
                'inspector_id': 1
            },
            {
                'name': 'Фрезерный станок ФС-2',
                'model': 'ФС-2П',
                'serial_number': 'FS002-2024',
                'location': 'Цех №1, участок Б',
                'status': 'active',
                'inspector_id': 1
            },
            {
                'name': 'Сварочный аппарат СА-3',
                'model': 'СА-3М',
                'serial_number': 'SA003-2024',
                'location': 'Цех №2, участок В',
                'status': 'maintenance',
                'inspector_id': 2
            },
            {
                'name': 'Компрессор К-4',
                'model': 'К-4П',
                'serial_number': 'CP004-2024',
                'location': 'Компрессорная',
                'status': 'active',
                'inspector_id': 2
            },
            {
                'name': 'Кран мостовой КМ-5',
                'model': 'КМ-5Т',
                'serial_number': 'CR005-2024',
                'location': 'Цех №3',
                'status': 'active',
                'inspector_id': 1
            },
            {
                'name': 'Конвейер КВ-6',
                'model': 'КВ-6Л',
                'serial_number': 'CV006-2024',
                'location': 'Цех №2, линия 1',
                'status': 'active',
                'inspector_id': 2
            }
        ]
        
        for eq_data in equipment_data:
            if not Equipment.query.filter_by(serial_number=eq_data['serial_number']).first():
                equipment = Equipment(**eq_data)
                db.session.add(equipment)
        
        db.session.commit()
        
        # Получаем созданное оборудование
        equipment_list = Equipment.query.all()
        
        # Создаем демонстрационные проверки
        inspection_results = ['passed', 'failed']
        checklist_items = [
            'visual_inspection', 'power_supply', 'safety_devices',
            'calibration', 'documentation', 'cleanliness'
        ]
        
        for equipment in equipment_list:
            # Создаем несколько проверок для каждого оборудования
            for i in range(random.randint(1, 3)):
                inspection_date = datetime.now() - timedelta(days=random.randint(1, 30))
                result = random.choice(inspection_results)
                
                # Создаем случайный чек-лист
                selected_checks = random.sample(checklist_items, random.randint(3, 6))
                checklist_data = ','.join(selected_checks)
                
                inspection = Inspection(
                    equipment_id=equipment.id,
                    inspector_id=equipment.inspector_id,
                    inspection_date=inspection_date,
                    status='completed',
                    result=result,
                    notes=f'Демонстрационная проверка #{i+1}. ' + 
                          ('Оборудование работает нормально.' if result == 'passed' else 'Обнаружены незначительные замечания.'),
                    checklist_data=checklist_data
                )
                
                db.session.add(inspection)
                
                # Обновляем дату последней проверки оборудования
                if not equipment.last_inspection or inspection_date > equipment.last_inspection:
                    equipment.last_inspection = inspection_date
        
        db.session.commit()
        print("Демонстрационные данные успешно созданы!")
        print(f"Создано пользователей: {User.query.count()}")
        print(f"Создано оборудования: {Equipment.query.count()}")
        print(f"Создано проверок: {Inspection.query.count()}")

if __name__ == '__main__':
    create_demo_data() 