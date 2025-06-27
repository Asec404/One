# 🚀 Быстрый деплой на GitHub + Render

## Шаг 1: Загрузка на GitHub

```bash
# В папке проекта
git init
git add .
git commit -m "Initial commit: Equipment Inspection System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/equipment-inspection-system.git
git push -u origin main
```

## Шаг 2: Деплой на Render

1. **Откройте [render.com](https://render.com)**
2. **Нажмите "New +" → "Web Service"**
3. **Подключите GitHub репозиторий**
4. **Настройте:**
   - **Name:** equipment-inspection-system
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app_simple:app`
5. **Нажмите "Create Web Service"**

## Готово! 🎉

Ваше приложение будет доступно по адресу:
`https://equipment-inspection-system.onrender.com`

### Учетные данные:
- **Логин:** admin
- **Пароль:** admin123

---

**Подробная инструкция:** [DEPLOYMENT.md](DEPLOYMENT.md) 