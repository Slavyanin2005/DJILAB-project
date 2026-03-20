# DJILab Project

Платформа для продажи лабораторного оборудования. Full-stack приложение с React frontend и Django backend.

---

## Содержание 🗒

- [Описание](#описание)
- [Структура проекта](#структура-проекта)
- [Технологии](#технологии)
- [Быстрый старт](#быстрый-старт)
- [Установка и запуск](#установка-и-запуск)
- [API Документация](#api-документация)
- [Пре-коммит хуки](#пре-коммит-хуки)
- [Code Style](#code-style)

---

## Описание ✎

**DJILab** — это веб-платформа для продажи профессионального лабораторного оборудования. Проект включает:

- **Backend**: Django REST API + Django Templates
- **Frontend**: React 19 + TypeScript + Vite
- **База данных**: PostgreSQL
- **Хранилище файлов**: MinIO (S3-compatible)
- **Контейнеризация**: Docker + Docker Compose

### Основные возможности:

✅ Каталог товаров с поиском и фильтрацией
✅ Корзина с управлением заказами
✅ История заявок с отслеживанием статусов
✅ REST API для интеграции
✅ Админ-панель Django
✅ Адаптивный дизайн

---

## Структура проекта 🗁

```
djilab-project/
├── backend/                     # Django backend
├── frontend/                    # React frontend
├── .flake8                      # Конфигурация flake8
├── .gitignore                   # Git ignore
├── .pre-commit-config.yaml      # Pre-commit хуки
├── docker-compose.yml           # Docker Compose конфигурация
└── README.md                    # Этот файл
```

---

## Технологии 🛠

### Backend
| Технология | Версия | Назначение |
|------------|--------|------------|
| **Python** | 3.11 | Язык программирования |
| **Django** | 5.2.11 | Web-фреймворк |
| **Django REST Framework** | 3.15.2 | REST API |
| **PostgreSQL** | 15 | База данных |
| **psycopg** | 3.3.3 | PostgreSQL драйвер |

### Frontend
| Технология | Версия | Назначение |
|------------|--------|------------|
| **React** | 19.2.0 | UI библиотека |
| **TypeScript** | 5.9.3 | Типизация |
| **Vite** | 7.3.1 | Сборщик |
| **Axios** | 1.13.6 | HTTP клиент |
| **React Router DOM** | 7.13.1 | Маршрутизация |

### DevOps & Tools
| Инструмент | Назначение |
|------------|------------|
| **Docker** | Контейнеризация |
| **Docker Compose** | Оркестрация контейнеров |
| **MinIO** | Объектное хранилище |
| **Adminer** | GUI для PostgreSQL |
| **pre-commit** | Pre-commit хуки |
| **Black** | Форматтер Python |
| **isort** | Сортировка импортов |
| **flake8** | Линтер Python |
| **ESLint** | Линтер TypeScript/React |
| **Prettier** | Форматтер кода |

---

## Быстрый старт ▶

### Требования

- **Docker** и **Docker Compose**
- **Python 3.11+** (для локальной разработки backend)
- **Node.js 20+** (для локальной разработки frontend)

### Запуск через Docker (рекомендуется)

```bash
# Клонировать репозиторий
git clone https://github.com/Slavyanin2005/DJILAB-project.git
cd DJILAB-project

# Запустить все сервисы
docker-compose up -d

# Применить миграции
docker-compose exec backend python manage.py migrate

# Создать суперпользователя
docker-compose exec backend python manage.py createsuperuser
```

**Сервисы будут доступны по адресам:**

| Сервис | URL |
|--------|-----|
| **Frontend** | http://localhost:5173/ |
| **Backend API** | http://localhost:8000/api/ |
| **Django Admin** | http://localhost:8000/admin/ |
| **MinIO Console** | http://localhost:9001/ |
| **Adminer (БД)** | http://localhost:8080/ |

---

## Установка и запуск ▶

### Backend (локально)

```bash
cd backend

# Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver
```

**Backend доступен:** http://localhost:8000/

### Frontend (локально)

```bash
cd frontend

# Установить зависимости
npm install

# Запустить dev-сервер
npm run dev
```

**Frontend доступен:** http://localhost:5173/

---

## API Документация ᯤ

### Базовый URL

```
http://localhost:8000/api/
```

### Endpoints

#### Услуги (Services)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/services/` | Список всех услуг |
| `GET` | `/services/{id}/` | Детальная информация |
| `POST` | `/services/{id}/add_to_order/` | Добавить в заказ |

#### Заказы (Orders)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/orders/` | Список всех заказов |
| `GET` | `/orders/{id}/` | Детальная информация |
| `POST` | `/orders/` | Создать новый заказ |
| `POST` | `/orders/{id}/add_item/` | Добавить позицию |
| `POST` | `/orders/{id}/update_item/` | Обновить позицию |
| `POST` | `/orders/{id}/remove_item/` | Удалить позицию |
| `POST` | `/orders/{id}/submit/` | Отправить заказ |
| `POST` | `/orders/{id}/delete/` | Удалить заказ |

#### Профили (Profiles)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/profiles/` | Профиль пользователя |

### Пример запроса

```bash
# Получить список услуг
curl http://localhost:8000/api/services/

# Создать заказ
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d "{}"
```

---

## Pre-commit хуки ⚙

Проект использует **pre-commit** для автоматической проверки кода.

### Установка

```bash
# Установить pre-commit
pip install pre-commit

# Инициализировать хуки
pre-commit install
```

### Доступные хуки

| Хук | Описание |
|-----|----------|
| `trailing-whitespace` | Удаляет пробелы в конце строк |
| `end-of-file-fixer` | Добавляет пустую строку в конец файла |
| `check-yaml` | Проверяет валидность YAML |
| `check-added-large-files` | Проверка размера файлов (< 1MB) |
| `check-merge-conflict` | Проверка конфликтов слияния |
| `black` | Форматирование Python кода |
| `isort` | Сортировка импортов Python |
| `flake8` | Линтинг Python |
| `prettier-frontend` | Форматирование TypeScript/JS/CSS |
| `eslint-frontend` | Линтинг TypeScript/React |

### Ручной запуск

```bash
# Проверить все файлы
pre-commit run --all-files

# Проверить только изменённые файлы
pre-commit run
```

---

## Code Style ☰

### Backend (Python)

| Тип | Стиль | Пример |
|-----|-------|--------|
| Переменные | `snake_case` | `user_id`, `order_total` |
| Функции | `snake_case` | `get_order()`, `create_service()` |
| Классы | `PascalCase` | `OrderItem`, `UserProfile` |
| Файлы | `snake_case.py` | `api_views.py`, `models.py` |
| Константы | `UPPER_SNAKE_CASE` | `DEBUG`, `SECRET_KEY` |

**Инструменты:**
- **Black** — автоматическое форматирование
- **isort** — сортировка импортов
- **flake8** — линтинг

### Frontend (TypeScript/React)

| Тип | Стиль | Пример |
|-----|-------|--------|
| Переменные | `camelCase` | `cartCount`, `userName` |
| Функции | `camelCase` | `handleAddToCart()`, `loadServices()` |
| Компоненты | `PascalCase` | `ProductCard`, `OrderHistory` |
| Файлы компонентов | `PascalCase.tsx` | `ProductCard.tsx` |
| Файлы утилит | `camelCase.ts` | `api.ts`, `utils.ts` |
| Константы | `UPPER_SNAKE_CASE` | `API_BASE_URL`, `MAX_ITEMS` |

**Инструменты:**
- **ESLint** — линтинг TypeScript/React
- **Prettier** — форматирование кода

---

## Переменные окружения 🔒︎

### Backend (.env)

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=djilab_db
DB_USER=admin
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5433
MINIO_URL=http://localhost:9000
MINIO_BUCKET=djilab-products
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=your-secret-key
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000/api
```

---

## Docker команды 🐳

```bash
# Запустить все сервисы
docker-compose up -d

# Остановить все сервисы
docker-compose down

# Перезапустить конкретный сервис
docker-compose restart backend

# Посмотреть логи
docker-compose logs backend
docker-compose logs frontend

# Применить миграции
docker-compose exec backend python manage.py migrate

# Создать суперпользователя
docker-compose exec backend python manage.py createsuperuser

# Выполнить команду в контейнере
docker-compose exec backend bash
docker-compose exec frontend sh
```

---

## Авторы

- **Slavyanin2005** — основная разработка

---

## Лицензия 🗎

Проект создан в учебных целях для лабораторной работы.

---

## Контакты ☎

- **Email**: ostafinskijvadim@gmail.com
- **Телефон**: +7 (905) 978-65-14
- **Адрес репозитория**: https://github.com/Slavyanin2005/DJILAB-project
