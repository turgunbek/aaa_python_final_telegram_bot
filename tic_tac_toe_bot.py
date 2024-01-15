"""
Bot for playing tic tac toe game with multiple CallbackQueryHandlers.
"""

from copy import deepcopy
from enum import Enum
import logging
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
import os


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being
# logged
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# get token using BotFather
TOKEN = os.getenv('TG_TOKEN')

SIZE_SELECTION, CONTINUE_GAME, FINISH_GAME = range(3)

FREE_SPACE = '.'
CROSS = 'X'
ZERO = 'O'

FIELD_SIZE = 3


DEFAULT_STATE = [
    [FREE_SPACE for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)
    ]


class Message(Enum):
    X_WON = f'You have won! {FIELD_SIZE} crosses on a line.'
    O_WON = f'Bot has won! {FIELD_SIZE} zeros on a line.'
    DRAW = 'Draw! Nobody has won.'
    X_TURN = 'Start the game. You play for X (cross).\nClick on the free cell'


def get_default_state():
    """Helper function to get default state of the game"""
    return deepcopy(DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]) ->\
      list[list[InlineKeyboardButton]]:
    """Generate tic tac toe keyboard size of FIELD_SIZE (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(FIELD_SIZE)
        ]
        for c in range(FIELD_SIZE)
    ]


async def update_game_status(update: Update,
                             message: Message,
                             keyboard_state: list[list[str]],
                             gameover: bool) -> int:
    """Displays the game update on the screen and returns the code of the
    following status"""

    keyboard = generate_keyboard(keyboard_state)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.effective_message.edit_text(message.value,
                                             reply_markup=reply_markup)
    if gameover:
        return FINISH_GAME
    return CONTINUE_GAME


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(Message.X_TURN.value,
                                    reply_markup=reply_markup)
    return CONTINUE_GAME


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Main processing of the game"""

    # user's turn
    keyboard_state = context.user_data['keyboard_state']
    try:
        user_col, user_row = users_turn(context)

        keyboard_state[user_col][user_row] = CROSS
    except ValueError:
        return await update_game_status(update, Message.DRAW, keyboard_state,
                                        gameover=True)
    # check if user has won
    if won(keyboard_state, CROSS):
        return await update_game_status(update, Message.X_WON, keyboard_state,
                                        gameover=True)

    # bot's turn
    try:
        bot_col, bot_row = bots_turn(keyboard_state)
        keyboard_state[bot_col][bot_row] = ZERO
    except ValueError:
        # field is completed, no free cells, no wins => draw
        return await update_game_status(update, Message.DRAW, keyboard_state,
                                        gameover=True)
    # check if bot has won
    if won(keyboard_state, ZERO):
        return await update_game_status(update, Message.O_WON, keyboard_state,
                                        gameover=True)

    # continue the game
    return await update_game_status(update, Message.X_TURN, keyboard_state,
                                    gameover=False)


def users_turn(context: ContextTypes.DEFAULT_TYPE) -> tuple[int, int]:
    """
    Processing of user's turn (user puts the CROSS).
    The case of ValueError ocurs when the FIELD_SIZE is even (4,6,...), i.e.
    when the bot's turn is last so the user can't turn
    """

    keyboard_state = context.user_data['keyboard_state']
    if any(FREE_SPACE in row for row in keyboard_state):
        return tuple(map(int, context.match.string))
    else:
        raise ValueError("No free cells.")


def bots_turn(fields: list[list[str]]) -> tuple[int, int]:
    """
    Bot's turn (puts the ZERO).
    Accordingly to the problem's task bot's turn is random free cell
    """

    free_cells = []
    for i, row in enumerate(fields):
        for j, cell in enumerate(row):
            if cell == FREE_SPACE:
                free_cells.append((i, j))

    if len(free_cells) == 0:
        raise ValueError('No free cells.')
    else:
        return random.choice(free_cells)  # bot_col, bot_row


def won(fields: list[list[str]], sign: str) -> bool:
    """Check the win condition for the selected sign"""

    for i in range(FIELD_SIZE):
        # check rows
        if all(c == sign for c in fields[i]):
            return True

        # check columns
        if all(row[i] == sign for row in fields):
            return True

    # check diagonals
    if all(fields[i][i] == sign for i in range(FIELD_SIZE)) or \
       all(fields[i][FIELD_SIZE - 1 - i] == sign for i in range(FIELD_SIZE)):
        return True

    return False


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    # reset state to default so you can play again with /start
    context.user_data['keyboard_state'] = get_default_state()
    return ConversationHandler.END


def main() -> None:
    """Run the bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Setup conversation handler with the states CONTINUE_GAME and FINISH_GAME
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONTINUE_GAME: [
                CallbackQueryHandler(game, pattern='^' + f'{r}{c}' + '$')
                for r in range(FIELD_SIZE)
                for c in range(FIELD_SIZE)
            ],
            FINISH_GAME: [
                CallbackQueryHandler(end, pattern='^' + f'{r}{c}' + '$')
                for r in range(FIELD_SIZE)
                for c in range(FIELD_SIZE)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to application that will be used for handling
    # updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
