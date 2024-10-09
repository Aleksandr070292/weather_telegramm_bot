import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from config_data.config import TELEGRAM_TOKEN, OPENWEATHERMAP_API_KEY
from database import log_request, Session, Log
from flask import Flask, jsonify, request
import threading

# Создаем Flask приложение
app = Flask(__name__)


@app.route('/logs', methods=['GET'])
def get_logs():
    session = Session()

    # Получаем параметры из запроса
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    query = session.query(Log)

    # Фильтрация по времени
    if start_time:
        query = query.filter(Log.timestamp >= start_time)
    if end_time:
        query = query.filter(Log.timestamp <= end_time)

    # Пагинация
    logs = query.offset((page - 1) * limit).limit(limit).all()

    return jsonify([{
        'user_id': log.user_id,
        'command': log.command,
        'timestamp': log.timestamp,
        'response': log.response
    } for log in logs])


@app.route('/logs/<int:user_id>', methods=['GET'])
def get_user_logs(user_id):
    session = Session()
    logs = session.query(Log).filter(Log.user_id == user_id).all()
    return jsonify([{
        'command': log.command,
        'timestamp': log.timestamp,
        'response': log.response
    } for log in logs])


# Функция для отображения меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Определяем кнопки
    buttons = [
        ["/weather <город>", "Как пользоваться"],
        ["Помощь", "Обратная связь"]
    ]

    # Создаем клавиатуру
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    # Отправляем сообщение с клавиатурой
    await update.message.reply_text(
        "Привет! Я бот, который предоставляет информацию о погоде. Чтобы узнать погоду, введите : /weather <Город>",
        reply_markup=keyboard
    )

# Команда для получения погоды
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    command = update.message.text

    # Проверка наличия города
    if len(context.args) == 0:
        await update.message.reply_text("Пожалуйста, укажите город. Пример: /weather Москва")
        log_request(user_id, command, "Город не указан")
        return

    city = ' '.join(context.args)
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"

    try:
        response = requests.get(weather_url)
        data = response.json()

        if response.status_code != 200:
            await update.message.reply_text("Город не найден. Попробуйте снова.")
            log_request(user_id, command, "Город не найден")
            return

        # Получаем данные о погоде
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Формируем ответ
        response_message = (f"Погода в {city}:\n"
                            f"Температура: {temperature}°C\n"
                            f"Ощущается как: {feels_like}°C\n"
                            f"Описание: {description}\n"
                            f"Влажность: {humidity}%\n"
                            f"Скорость ветра: {wind_speed} м/с")

        await update.message.reply_text(response_message)
        log_request(user_id, command, response_message)

    except Exception as e:
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")
        log_request(user_id, command, str(e))

# Функция для обработки кнопки "Как пользоваться"
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Чтобы получить информацию о погоде, используйте команду:\n"
        "/weather <город> - Например: /weather Москва\n"
        "Вы также можете нажимать на кнопки в меню для быстрого доступа к командам."
    )
    await update.message.reply_text(help_text)

# Основная функция
def main():
    # Создаем приложение с использованием токена
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('weather', weather))
    application.add_handler(CommandHandler('help', help))

    # Запускаем бота
    application.run_polling()

# Функция для запуска Flask
def run_flask():
    app.run(port=5000)


if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Запускаем Telegram-бота
    main()
