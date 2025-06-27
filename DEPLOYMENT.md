# Инструкция по деплою на GitHub и Render

## 📋 Подготовка к загрузке на GitHub

### 1. Инициализация Git репозитория

```bash
# Инициализируйте Git в папке проекта
git init

# Добавьте все файлы в индекс
git add .

# Создайте первый коммит
git commit -m "Initial commit: Equipment Inspection System"

# Добавьте удаленный репозиторий (замените на ваш URL)
git remote add origin https://github.com/your-username/equipment-inspection-system.git

# Отправьте код на GitHub
git push -u origin main
```

### 2. Проверьте, что все файлы добавлены

Убедитесь, что в репозитории есть следующие файлы:
- ✅ `app_simple.py` - основное приложение
- ✅ `requirements.txt` - зависимости
- ✅ `templates/` - HTML шаблоны
- ✅ `static/` - статические файлы
- ✅ `render.yaml` - конфигурация Render
- ✅ `Procfile` - конфигурация для деплоя
- ✅ `runtime.txt` - версия Python
- ✅ `.gitignore` - исключения Git
- ✅ `README.md` - документация

### 3. Проверьте .gitignore

Убедитесь, что файл `data.json` добавлен в `.gitignore`, чтобы данные не загружались в репозиторий.

## 🚀 Деплой на Render

### Вариант 1: Автоматический деплой через Blueprint

1. **Перейдите на Render:**
   - Откройте [render.com](https://render.com)
   - Войдите или зарегистрируйтесь

2. **Создайте Blueprint:**
   - Нажмите "New +" → "Blueprint"
   - Подключите ваш GitHub аккаунт
   - Выберите репозиторий `equipment-inspection-system`

3. **Настройте деплой:**
   - Render автоматически обнаружит `render.yaml`
   - Проверьте настройки:
     - **Name:** equipment-inspection-system
     - **Environment:** Python
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app_simple:app`

4. **Создайте сервис:**
   - Нажмите "Apply"
   - Render автоматически развернет приложение

### Вариант 2: Ручной деплой

1. **Создайте Web Service:**
   - Нажмите "New +" → "Web Service"
   - Подключите GitHub репозиторий

2. **Настройте параметры:**
   - **Name:** equipment-inspection-system
   - **Environment:** Python
   - **Region:** Выберите ближайший к вам
   - **Branch:** main
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app_simple:app`

3. **Добавьте переменные окружения:**
   - **SECRET_KEY:** (оставьте пустым, Render сгенерирует автоматически)
   - **PYTHON_VERSION:** 3.9.16

4. **Создайте сервис:**
   - Нажмите "Create Web Service"

## 🔧 Настройка после деплоя

### 1. Проверьте логи

После деплоя проверьте логи в Render Dashboard:
- Убедитесь, что приложение запустилось без ошибок
- Проверьте, что все зависимости установились

### 2. Настройте домен (опционально)

В настройках сервиса можно:
- Добавить кастомный домен
- Настроить SSL сертификат
- Настроить редирект с www

### 3. Обновите README

После успешного деплоя обновите `README.md`:
```markdown
## 🚀 Демо

**Живая версия:** https://your-app-name.onrender.com
```

## 🐛 Решение проблем

### Проблема: "Build failed"

**Решение:**
1. Проверьте `requirements.txt` - все зависимости должны быть совместимы
2. Убедитесь, что в коде нет синтаксических ошибок
3. Проверьте логи сборки в Render

### Проблема: "Application error"

**Решение:**
1. Проверьте логи приложения в Render
2. Убедитесь, что `app_simple.py` запускается локально
3. Проверьте переменные окружения

### Проблема: "Module not found"

**Решение:**
1. Добавьте недостающие зависимости в `requirements.txt`
2. Убедитесь, что используется правильная версия Python

### Проблема: "Port binding error"

**Решение:**
1. Убедитесь, что приложение слушает на порту из переменной окружения:
```python
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

## 📊 Мониторинг

### Логи в Render

- **Build Logs:** Логи сборки приложения
- **Runtime Logs:** Логи работы приложения
- **Deploy Logs:** Логи деплоя

### Метрики

Render предоставляет:
- Время отклика
- Количество запросов
- Использование ресурсов

## 🔄 Обновления

### Автоматические обновления

При каждом push в ветку `main` Render автоматически:
1. Обнаружит изменения
2. Запустит новую сборку
3. Развернет обновленную версию

### Ручные обновления

Если нужно развернуть конкретную версию:
1. Перейдите в настройки сервиса
2. Выберите "Manual Deploy"
3. Укажите коммит или ветку

## 💰 Стоимость

### Render Free Tier

- **Web Services:** 750 часов/месяц
- **Custom Domains:** Поддерживаются
- **SSL:** Автоматически
- **Sleep:** После 15 минут неактивности

### Render Paid Plans

- **Starter:** $7/месяц
- **Standard:** $25/месяц
- **Pro:** $85/месяц

## 🔒 Безопасность

### Рекомендации

1. **Переменные окружения:**
   - Не храните секреты в коде
   - Используйте переменные окружения Render

2. **HTTPS:**
   - Render автоматически предоставляет SSL
   - Все соединения защищены

3. **Доступ:**
   - Ограничьте доступ к админ-панели
   - Используйте сложные пароли

## 📞 Поддержка

### Render Support

- **Документация:** [docs.render.com](https://docs.render.com)
- **Community:** [community.render.com](https://community.render.com)
- **Email:** support@render.com

### GitHub Support

- **Issues:** Создайте Issue в репозитории
- **Discussions:** Используйте Discussions для вопросов
- **Wiki:** Создайте Wiki для документации

---

**Удачного деплоя! 🚀** 