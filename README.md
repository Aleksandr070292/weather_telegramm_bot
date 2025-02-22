# Telegram Weather Bot

Этот проект представляет собой Telegram-бота, который предоставляет информацию о погоде в указанном городе, используя Telegram Bot API и API погоды. Бот логирует все запросы пользователей и предоставляет REST API для просмотра истории запросов.

## Структура проекта

- `weather_telegramm_bot/` - содержит основной код бота
  - `app.py` - основная логика взаимодействия с Telegram и API погоды
- `database/` - управление базой данных
  - `models.py` - описание базы данных и логов
- `config/` - конфигурационные файлы
  - `config.py` - загрузка переменных окружения (например, токенов API)
- `.env` - файл с конфиденциальными настройками, такими как API-ключи
- `README.md` - описание проекта и руководство по установке

## Требования

- Python 3.7+
- Telegram Bot API ключ
- OpenWeatherMap API ключ


## Установка и настройка

### Шаг 1: Клонируйте репозиторий и перейдите в директорию проекта

git clone <URL вашего репозитория>

### Шаг 2: Установите виртуальное окружение и зависимости

- python -m venv venv
- source venv/bin/activate  # для Windows используйте venv\Scripts\activate
- pip install -r requirements.txt

### Шаг 3: Создайте файл .env и добавьте API ключи

TELEGRAM_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
OPENWEATHERMAP_API_KEY=YOUR_OPENWEATHERMAP_API_KEY

### Шаг 4: Запустите бота

python3 app.py


## Использование

- Команда бота: отправьте /weather <город> в Telegram, чтобы получить текущую погоду в указанном городе

- Логирование запросов: все запросы пользователей записываются в базу данных SQLite (logs.db)


# API Documentation

## Telegram Bot

### /start
- **Описание**: Инициализация бота и отображение меню.
- **Метод**: GET
- **Пример использования**: `/start`

### /weather <город>
- **Описание**: Получение текущей погоды для указанного города.
- **Метод**: GET
- **Пример использования**: `/weather Москва`

### /help
- **Описание**: Информация о том, как использовать бота.
- **Метод**: GET
- **Пример использования**: `/help`

## REST API

### GET /logs
- **Описание**: Получение логов с возможностью пагинации и фильтрации.
- **Параметры**:
  - `page`: Номер страницы (по умолчанию 1).
  - `limit`: Количество записей на странице (по умолчанию 10).
  - `start_time`: Начальная дата и время (например, `2024-10-09T00:00:00`).
  - `end_time`: Конечная дата и время (например, `2024-10-09T23:59:59`).
- **Пример запроса**: `/logs?page=1&limit=10&start_time=2024-10-01T00:00:00&end_time=2024-10-09T23:59:59`

### GET /logs/<int:user_id>
- **Описание**: Получение логов для конкретного пользователя по его ID.
- **Пример запроса**: `/logs/1`# weather_telegramm_bot
