from django.core.management.base import BaseCommand

from habits.services import get_bot_info, send_telegram_message


class Command(BaseCommand):
    help = 'Проверка подключения к Telegram API и тестовая отправка сообщения'

    def add_arguments(self, parser):
        parser.add_argument('--chat-id', type=str, help='Chat id для тестовой отправки')
        parser.add_argument('--text', type=str, default='Тестовое сообщение от Habit Tracker')

    def handle(self, *args, **options):
        bot_info = get_bot_info()
        if not bot_info or not bot_info.get('ok'):
            self.stdout.write(self.style.ERROR('Telegram API недоступен. Проверьте TELEGRAM_BOT_TOKEN.'))
            return

        bot = bot_info.get('result', {})
        self.stdout.write(self.style.SUCCESS(f"Бот доступен: @{bot.get('username', 'unknown')}"))

        chat_id = options.get('chat_id')
        if chat_id:
            sent = send_telegram_message(chat_id, options['text'])
            if sent:
                self.stdout.write(self.style.SUCCESS('Тестовое сообщение отправлено.'))
            else:
                self.stdout.write(self.style.ERROR('Сообщение не отправлено. Проверьте chat_id и права бота.'))
        else:
            self.stdout.write(self.style.WARNING('Для тестовой отправки укажите --chat-id.'))
