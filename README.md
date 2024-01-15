# aaa_python_final_telegram_bot

# Telegram-бот для игры в крестики-нолики

В текущей реализации есть возможность играть с ботом в классические крестики-нолики 3 на 3.

## Чтобы запустить бота, необходимо:<br>
1. Установить все необходимые модули и библиотеки (в т.ч. python-telegram-bot);
2. В telegram получить от @BotFather токен (командой ```/newbot```);
3. Установить переменную окружения ```TG_TOKEN=<token_from_botfather>```;
4. Запустить скрипт tic_tac_toe_bot.py;
5. В телеграм должно прийти сообщение от вашего бота (если не пришло, то непосредственно заходим в него);
6. Пишем боту команду ```/start```;
7. Играем. (Если нужно начать новую игру, то снова пишем команду ```/start```).

*Замечание*: бот работает только при запущенном скрипте tic_tac_toe_bot.py.

Тесты можно запустить командой ```python -m pytest -v tests.py```.


Иллюстрация игры:<br>
![tic_tac_toe](https://github.com/turgunbek/aaa_python_final_telegram_bot/assets/35132790/58704f3d-bf6f-46f4-9b56-f273957d0489)
