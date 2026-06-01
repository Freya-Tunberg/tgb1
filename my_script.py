from random import choice
import telebot

token = '8960789352:AAHim1yRqNm-V_l2EoXbAufbPu4bEI9Op'

bot = telebot.TeleBot(token)

RANDOM_TASKS = [
    'Заварить чашку любимого чая/кофе и выпить её, наслаждаясь ароматом.',
    'Сделать 10 приседаний и 5 отжиманий.',
    'Написать три благодарности за то, что есть в жизни прямо сейчас.',
    'Выйти на 10-минутную прогулку и обратить внимание на три необычных детали вокруг.',
    'Почитать 5 страниц любой книги.',
    'Нарисовать простой рисунок: солнце, домик или цветок — на выбор.',
    'Позвонить или написать короткое сообщение кому‑то из близких просто так, без повода.',
    'Убрать одну зону в доме: стол, полку или ящик.'
]

todos = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я бот для задач. Напиши /help для списка команд.')

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = '''
Команды:
/add <дата> <задача> — добавить задачу
/print <дата> — показать задачи на дату
/all — все задачи
/random — случайная задача на сегодня
/edit <номер> <новый текст> — изменить задачу
/delete <номер> — удалить задачу'''
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['random'])
def random_command(message):
    try:
        task = choice(RANDOM_TASKS)
        if 'сегодня' not in todos:
            todos['сегодня'] = []
        todos['сегодня'].append(task)
        bot.send_message(message.chat.id, f'📌 Случайная задача на сегодня:\n{task}')
    except Exception as e:
        bot.send_message(message.chat.id, f'❌ Ошибка при добавлении случайной задачи: {e}')

@bot.message_handler(commands=['add'])
def add_command(message):
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            bot.send_message(message.chat.id, '❌ Используйте формат /add <дата> <задача>')
            return
        date = parts[1]
        task = parts[2].strip()
        if len(task) < 3:
            bot.send_message(message.chat.id, '❗ Задача должна содержать не менее 3 символов.')
            return
        if date not in todos:
            todos[date] = []
        todos[date].append(task)
        bot.send_message(message.chat.id, f'✅ Задача "{task}" добавлена на {date}')
    except Exception as e:
        bot.send_message(message.chat.id, f'❌ Ошибка {e}')

@bot.message_handler(commands=['print'])
def print_command(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.send_message(message.chat.id, '❌ Ошибка: укажите дату')
            return
        date = parts[1]
        if date in todos and todos[date]:
            response = f'📌 Задачи на {date}:\n'
            for i, task in enumerate(todos[date], 1):
                response += f'{i}. {task}\n'
        else:
            response = f'📌 На {date} задач нет.'
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f'❌ Ошибка при выполнении /print: {e}')

@bot.message_handler(commands=['all'])
def all_command(message):
    try:
        if not todos:
            bot.send_message(message.chat.id, '❗ У вас пока нет задач.')
            return
        response = '📝 Все задачи:\n\n'
        for date, tasks in todos.items():
            response += f'📝 {date}:\n'
            for i, task in enumerate(tasks, 1):
                response += f'{i}. {task}\n'
            response += '\n'
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f'❌ Ошибка при выполнении /all: {e}')

@bot.message_handler(commands=['edit'])
def edit_command(message):
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            bot.send_message(message.chat.id, '❌ Используйте формат /edit <номер> <новый текст>')
            return
        task_num = int(parts[1]) - 1
        if task_num < 0:
            bot.send_message(message.chat.id, '❌ Номер задачи не может быть отрицательным.')
            return
        new_task = parts[2]
        found = False
        for date, tasks in todos.items():
            if 0 <= task_num < len(tasks):
                old_task = tasks[task_num]
                tasks[task_num] = new_task
                bot.send_message(message.chat.id, f'✅ Задача №{task_num + 1} изменена:\nБыло: {old_task}\nСтало: {new_task}')
                found = True
                break
        if not found:
            bot.send_message(message.chat.id, '❌ Задача с таким номером не найдена.')
    except ValueError:
        bot.send_message(message.chat.id, '❌ Номер задачи должен быть числом.')
    except Exception as e:
        bot.send_message(message.chat.id, f'❌ Ошибка при редактировании: {e}')

@bot.message_handler(commands=['delete'])
def delete_command(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.send_message(message.chat.id, '❌ Используйте формат /delete <номер>')
            return
        task_num = int(parts[1]) - 1
        if task_num < 0:
            bot.send_message(message.chat.id, '❌ Номер задачи не может быть отрицательным.')
            return
        found = False
        for date, tasks in todos.items():
            if 0 <= task_num < len(tasks):
                deleted_task = tasks.pop(task_num)
                bot.send_message(message.chat.id, f'✅ Задача "{deleted_task}" удалена.')
                found = True
                break
        if not found:
            bot.send_message(message.chat.id, '❌ Задача с таким номером не найдена.')
    except ValueError:
        bot.send_message(message.chat.id, '❌ Номер задачи должен быть числом.')
    except Exception as e:
        bot.send_message(message.chat.id, f'❌ Ошибка при удалении: {e}')

bot.polling(none_stop=True)