MENU_VK = "Привет. Я бот Окей, Горный!\nЯ помогу найти тебя серферам, чтоб ты поскорее начал вливаться в новый коллектив, а также подскажу ответы на интересующие тебя вопросы"
MENU_TG = "Привет. Я бот Окей, Горный!\nЯ помогу найти тебя серферам, чтоб ты поскорее начал вливаться в новый коллектив, а также подскажу ответы на интересующие тебя вопросы"

CANCEL_BUTTON = "Обратно в меню"
BACK_BUTTON = "Назад"

FORM_ASK_FIO = "Пришли ФИО полностью"
FORM_ASK_VK = "Пришли ссылку на свой VK, свой VK ID или никнейм VK (тот, что идет после vk.ru)"
FORM_VK_FAILED = "Не нашел такого пользователя, повтори попытку"
FORM_ASK_NUMBER = "Пришли уникальный номер"
FORM_NUMBER_FAILED = "Не распознал номер, повтори попытку"
FORM_ASK_YES_NO = "Лидер школы?"
FORM_YES_NO_FAILED = "Не распознал ответ, напиши 'Да' или 'Нет'"
FORM_ASK_DIRECTION = "Выбери направление"
FORM_DONE = "Спасибо! Данные записаны. Теперь можешь ждать, с тобой свяжутся в ближайшее время"
FORM_NOT_FOUND = "Такого направления не существует"
FORM_SUBMITTING = "Принял, записываю данные"

FORM_BUTTON = "Найдите меня"

FAQ_BUTTON = "Вопросы и ответы"

FAQ_EMPTY = "База знаний не найдена"
FAQ_ASK_TOPIC = "Выбери тему, которая тебя интересует"
def FAQ_ASK_SUBTOPIC(topic: str, subtopic_titles: list[str]) -> str:
    listing = "\n".join(f"• {title}" for title in subtopic_titles)
    return f'Что конкретно тебя интересует по теме «{topic}»?\n\n{listing}'



OWN_QUESTION_BUTTON="Задать свой вопрос"
TG_OWN_QUESTION_BUTTON="Задать свой вопрос в ВК"

SUPPORT_ASK_QUESTION = "Задай свой вопрос, и тебе ответят в ближайшее время"
SUPPORT_ENTERED="Мы приняли твой вопрос и в скором времени ответим"
SUPPORT_MODE=(
    "Режим чата\n\n"
    "В этом режиме ты сможешь вести диалог с модератором\n"
    'Работают только команды "Начать" и "Обратно в меню", которые отключат этот режим и вопрос будет закрыт'
)

TICKET_TAKE_BUTTON = "Взять"
TICKET_CLOSE_BUTTON = "Закрыть нахуй"

TICKET_OPEN_TEXT = "Вопрос #{id} по теме «{topic}»"
TICKET_TAKEN_NOTICE = "Вопрос #{id} по теме «{topic}» взял [id{vk_id}|модератор]"
TICKET_CLOSED_TEXT = "Вопрос #{id} закрыт"
TICKET_CLOSED_FOR_USER = "Вопрос закрыт модератером"

MAIN_EXIT_WORDS = (CANCEL_BUTTON.lower(), 'Начать'.lower(), 'Start'.lower())

SUPPORT_LIMIT_REACHED = (
    "Сегодня уже набралось много вопросов, и модераторы отвечают с задержкой 🙏\n"
    "Попробуй задать вопрос завтра — а пока загляни в базу знаний, вдруг ответ уже там"
)

SUPPORT_OUTSIDE_HOURS = (
    "Модераторы отвечают на вопросы с 10:00 до 22:00 по Москве.\n"
    "Напиши, пожалуйста, в это время — а пока можешь поискать ответ в базе знаний"
)


FAQ_ASK_VK_URL = "https://vk.com/im?media=&sel=-169197316"

ROOMMATES_BUTTON = "Мои соседи"
ROOMMATES_ASK_CIPHER = "Пришли свой уникальный номер"
ROOMMATES_CIPHER_INVALID = "Номер должен быть числом, попробуй ещё раз."
ROOMMATES_CIPHER_NOT_FOUND = "Такой номер не найден в списке заселения"
ROOMMATES_CIPHER_TAKEN = "Этот номер уже привязан к другому аккаунту"
ROOMMATES_FILL_FORM_REMINDER = f'Кстати, вижу, ты не заполнял форму - пожалуйста, заполни её через "{FORM_BUTTON}"'
ROOMMATES_NEW_NEIGHBOR = "🎉 У тебя новый сосед: {mention}"
ROOMMATES_LIST_HEADER = "Твои соседи:"
ROOMMATES_YOUR_ROOM = "Ты живёшь в общежитии «{comfort}», комната {room_number}"
ROOMMATES_NONE_YET = "Пока никто из твоих соседей не зарегистрировался в боте"