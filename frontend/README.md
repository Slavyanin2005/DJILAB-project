# DJILab Frontend

## Описание
Frontend-приложение для платформы продажи лабораторного оборудования. Построено на React + TypeScript с использованием Vite.

## Структура проекта
...

## Установка и запуск

### Требования
- Node.js 18+
- npm или pnpm

### Шаги установки
1. Перейти в папку frontend
```bash
cd frontend
```

2. Установить зависимости
```bash
npm install
```

3. Запустить сервер разработки
```bash
npm run dev
```
Приложение будет доступно по адресу: http://localhost:5173

### Доступные команды
| Команда | Описание |
|---------|----------|
| `npm run dev` | Запуск сервера разработки с Hot Reload |
| `npm run build` | Сборка для production |
| `npm run preview` | Предпросмотр production-сборки |
| `npm run lint` | Проверка кода через ESLint |

## API интеграция
- Frontend подключается к backend API:
- Base URL: http://127.0.0.1:8000/api
- Клиент: src/services/api.ts (axios)
- Аутентификация: сессионные куки + CSRF-токен

## API Endpoints

### Услуги (Services)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/api/services/` | Список услуг |
| GET | `/api/services/{id}/` | Детали услуги |
| POST | `/api/services/{id}/add_to_order/` | Добавить в заказ |

### Заказы (Orders)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/api/orders/` | Список заказов |
| POST | `/api/orders/` | Создать черновик |
| POST | `/api/orders/{id}/add_item/` | Добавить позицию |
| POST | `/api/orders/{id}/update_item/` | Изменить количество |
| POST | `/api/orders/{id}/remove_item/` | Удалить позицию |
| POST | `/api/orders/{id}/submit/` | Отправить заказ |
| POST | `/api/orders/{id}/delete/` | Удалить заказ |
## Переменные окружения
Создайте файл `.env` в корне `frontend/`:
```bash
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```
| Переменная | Описание | Пример |
|------------|----------|--------|
| `VITE_API_BASE_URL` | Базовый URL backend API | `http://localhost:8000/api` |

## Технологии
| Технология | Версия | Назначение |
|------------|--------|------------|
| `React` | 19 | UI-библиотека |
| `TypeScript` | 5.9 | Типизация |
| `Vite` | 7 | Сборщик и сервер разработки |
| `React Router DOM` | 7 | Маршрутизация |
| `Axios` | 1.13 | HTTP-клиент |

## Качество кода
### ESLint
Проект использует ESLint с конфигурацией для React + TypeScript:
1. Проверка кода
```bash
npm run lint
```
2. Автоисправление (если возможно)
```bash
npx eslint . --fix
```

### TypeScript
Строгая типизация включена в `tsconfig.app.json`:
- `strict: true`
- `noUnusedLocals: true`
- `noUnusedParameters: true`

Проверка типов:
```bash
npx tsc --noEmit
```
##  Стилизация
Проект использует глобальные CSS-переменные и CSS-классы (без CSS-in-JS):
- Файл стилей: `src/index.css`
- CSS-переменные определены в `:root`
- Адаптивная вёрстка через `@media`-запросы

### Основные переменные
```css
:root {
  --dji-blue: #0971CE;
  --dji-blue-dark: #0759a3;
  --dark: #272727;
  --error: #ff3b30;
  --radius: 12px;
  --shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}
```

## Зависимости
Основные зависимости **package.json**
```json
"dependencies": {
  "axios": "^1.13.6",
  "react": "^19.2.0",
  "react-dom": "^19.2.0",
  "react-router-dom": "^7.13.1"
}
```

Dev-зависимости
```json
"devDependencies": {
  "@vitejs/plugin-react": "^5.1.1",
  "typescript": "~5.9.3",
  "eslint": "^9.39.1",
  "vite": "^7.3.1"
}
```
## State Management
Для управления состоянием корзины используется **React Context**

### Использование
```tsx
import { useCart } from '../context/CartContext';

const MyComponent = () => {
  const { cartCount, refreshCart } = useCart();
  // ...
};
```
## CORS и аутентификация
- Включена отправка куки: `withCredentials: true`
- CSRF-токен автоматически добавляется к запросам
- Backend должен разрешать `http://localhost:5173` в `CORS_ALLOWED_ORIGINS`

## Code Style

### Именование
| Тип | Стиль | Пример |
|-----|-------|--------|
| Переменные | `camelCase` | `cartCount`, `userName` |
| Функции | `camelCase` | `handleAddToCart()`, `loadServices()` |
| Компоненты | `PascalCase` | `ProductCard`, `OrderHistory` |
| Файлы компонентов | `PascalCase.tsx` | `ProductCard.tsx`, `Header.tsx` |
| Файлы утилит | `camelCase.ts` | `api.ts`, `utils.ts` |
| Константы | `UPPER_SNAKE_CASE` | `API_BASE_URL`, `MAX_ITEMS` |
| Типы/Интерфейсы | `PascalCase` | `Service`, `OrderItem` |

### Инструменты
- **ESLint** — линтинг TypeScript/React кода
- **Prettier** — форматирование кода (опционально)

## Лицензия
Проект создан в учебных целях, ЗГУ.
