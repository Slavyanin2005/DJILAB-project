# DJILab Platform

Платформа для продажи профессионального лабораторного оборудования. Полный стек: Django REST API + React/TypeScript frontend.

> Учебный проект, выполненный в рамках курса «Разработка Web-приложений», ЗГУ.

---

## Структура проекта
...


---

## Быстрый старт

### Требования
- **Backend**: Python 3.11+, PostgreSQL 15+, pip
- **Frontend**: Node.js 18+, npm/pnpm
- **Опционально**: Docker & Docker Compose

### Запуск через Docker (рекомендуется)
# Клонировать репозиторий
```bash
git clone <repository-url>
cd djilab-project
```

# Запустить все сервисы
```bash
docker-compose up -d
```

Backend: http://127.0.0.1:8000

Frontend: http://localhost:5173

### Запуск вручную
**Backend**
```bash
cd backend
```
1. Создать виртуальное окружение
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```
2. Установить зависимости
```bash
pip install -r requirements.txt
```
3. Применить миграции
```bash
python manage.py migrate
```
4. Запустить сервер
```bash
python manage.py runserver
```

API доступен по адресу: http://127.0.0.1:8000/api

**Frontend**
```bash
cd frontend
```
1. Установить зависимости
```bash
npm install
```
2. Запустить сервер разработки
```bash
npm run dev
```
Приложение доступно по адресу: http://localhost:5173

## Документация

| Компонент | Документация |
|-----------|--------------|
| 🔹 Backend | [backend/README.md](backend/README.md) |
| 🔹 Frontend | [frontend/README.md](frontend/README.md) |

## Стек технологий
### Backend
| Технология | Версия | Назначение |
|------------|--------|------------|
| Django | 5.2 | Веб-фреймворк |
| Django REST Framework | 3.15 | Построение API |
| PostgreSQL | 15 | База данных |
| flake8 / black / isort | latest | Качество кода |

### Frontend
| Технология | Версия | Назначение |
|------------|--------|------------|
| React | 19 | UI-библиотека |
| TypeScript | 5.9 | Типизация |
| Vite | 7 | Сборщик и dev-сервер |
| React Router DOM | 7 | Маршрутизация |
| Axios | 1.13 | HTTP-клиент |

## Инфраструктура
- **MinIO** — объектное хранилище для медиафайлов
- **CORS** — настроен для взаимодействия frontend ↔ backend
- **Сессии + CSRF** — безопасная аутентификация

## Функционал

### Для пользователя
- Просмотр каталога услуг с поиском
- Детальная страница товара с галереей (фото + видео)
- Корзина с управлением количеством позиций
- История заявок со статусами
- Создание, редактирование и удаление черновиков заявок

### Для разработчика
- REST API с документированными эндпоинтами
- Типизация TypeScript на фронтенде
- Разделение ответственности: backend ↔ frontend
- Линтинг и форматирование кода (flake8, ESLint, Prettier)

## Переменные окружения
**Backend** (`.env` или `settings.py`)
```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:pass@host:5433/djilab_db
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

**Frontend** (`.env`)
```bash
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## Качество кода
### Backend
```bash
cd backend
```
1. Линтинг
```bash
flake8 .
```
2. Проверка форматирования
```bash
black . --chec
```
3. Проверка импортов
```bash
isort . --check
```

## Лицензия
Проект создан в учебных целях, ЗГУ.
