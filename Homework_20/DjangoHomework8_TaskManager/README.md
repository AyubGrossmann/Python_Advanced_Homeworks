# Homework 20 — регистрация и авторизация в Task Manager

Это следующая версия того же проекта из Homework 19 (и ДЗ 8–18).
Все предыдущие модели и API сохранены. Добавлены регистрация, вход по username/email,
выход, HttpOnly cookies, обновление и аннулирование refresh token.

## Запуск
```bash
python -m venv venv
# Windows PowerShell: venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Endpoints
- `POST /api/auth/register/` — регистрация: username, email, password, password_confirm.
- `POST /api/auth/login/` — вход: username_or_email и password; токены устанавливаются в HttpOnly cookies.
- `POST /api/auth/refresh/` — обновление по refresh cookie.
- `POST /api/auth/logout/` — blacklist refresh token и удаление cookies.
- `POST /api/token/` и `/api/token/refresh/` — исходные JWT endpoints из Homework 18 сохранены.

Пример регистрации:
```json
{"username":"student","email":"student@example.com","password":"StrongPass123!","password_confirm":"StrongPass123!"}
```
Локально `Secure=False`, чтобы cookies работали на HTTP localhost. Для production нужны HTTPS,
`Secure=True` и полноценная CSRF-защита.

## Автоматические тесты

```bash
python manage.py test
```
