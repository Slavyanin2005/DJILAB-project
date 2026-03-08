# DJILab Backend

## Описание
Backend для платформы продажи лабораторного оборудования. Реализует REST API для управления услугами, заказами и пользователями.

## Структура проекта
...

## Установка и запуск

### Требования
- Python 3.11+
- PostgreSQL 15+
- pip

### Шаги установки

1. Создать виртуальное окружение
```bash
python -m venv venv
```

2. Активировать (Windows)
```bash
venv\Scripts\activate
```

3. Установить зависимости
```bash
pip install -r requirements.txt
```

4. Применить миграции
```bash
python manage.py migrate
```

5. Запустить сервер
```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

## API Endpoints

### Услуги (Services)
| Метод | Эндпоинт                      | Описание                             |
|-------|-------------------------------|--------------------------------------|
| GET   | `/api/services/`              | Список всех активных услуг           |
| GET   | `/api/services/{id}/`         | Детальная информация об услуге       |
| POST  | `/api/services/{id}/add_to_order/` | Добавить услугу в заказ         |

### Заказы (Orders)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/api/orders/` | Список заказов текущего пользователя |
| GET | `/api/orders/{id}/` | Детальная информация о заказе |
| POST | `/api/orders/` | Создать новый заказ-черновик |
| POST | `/api/orders/{id}/add_item/` | Добавить позицию в заказ |
| POST | `/api/orders/{id}/update_item/` | Изменить количество позиции |
| POST | `/api/orders/{id}/remove_item/` | Удалить позицию из заказа |
| POST | `/api/orders/{id}/submit/` | Отправить заказ (статус → formed) |
| POST | `/api/orders/{id}/delete/`| Логическое удаление заказа |

### Профили (Profiles)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/api/profiles/` | Профиль текущего пользователя |

### Переменные окружения

| Переменная | Описание | Пример |
|------------|----------|--------|
|`DEBUG` | Режим отладки | True |
| `SECRET_KEY` | Секретный ключ Django | django-insecure-... |
| `DATABASE_URL` | Строка подключения к БД | postgres://user:pass@host:5433/db |
| `CORS_ALLOWED_ORIGINS` | Разрешённые CORS-источники | http://localhost:5173 |

## Технологии
- Django 5.2 — веб-фреймворк
- Django REST Framework — построение API
- PostgreSQL — база данных
- flake8 — линтер кода
- black — автоформатирование
- isort — сортировка импортов
- django-cors-headers — CORS middleware

## Качество кода

### Проверка кода линтером
```bash
flake8 .
```
### Форматирование кода (black)
```bash
black .
```

### Сортировка импортов (isort)
```bash
isort .
```

### Запуск всех проверок
```bash
flake8 . && black . --check && isort . --check
```

## Зависимости
Основные зависимости указаны в **requirements.txt**:

```bash
Django==5.2.11
psycopg==3.3.3
djangorestframework==3.15.2
django-cors-headers==4.3.1
flake8==7.1.0
black==24.4.2
isort==5.13.2
```

Установка:
```bash
pip install -r requirements.txt
```

## Безопасность
Важно: В продакшене обязательно:
1. Замените `SECRET_KEY` на сгенерированный безопасный ключ
2. Установите `DEBUG = False`
3. Настройте `ALLOWED_HOSTS` под ваш домен
4. Используйте HTTPS и безопасные настройки сессий

## Лицензия
Проект создан в учебных целях, ЗГУ.
