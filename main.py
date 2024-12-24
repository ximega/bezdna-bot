#!/bin/python

from telegram.ext import ApplicationBuilder, MessageHandler, filters

from commands import *
from dotenv import load_dotenv
import os


def main() -> None:
    load_dotenv()

    TOKEN: str | None = os.getenv('TOKEN')

    if TOKEN is None:
        print('No token given')
        return
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handlers([
        MessageHandler(filters.ChatType.GROUPS & filters.UpdateType.MESSAGE, check),
        MessageHandler(filters.ChatType.GROUPS & filters.UpdateType.EDITED_MESSAGE, check_edited),
    ])

    try:
        print('Bot run successfully!')
        
        app.run_polling()
        
    except Exception as exc:
        print('Bot couldn\'t run')
        print(exc.args[0])

if __name__ == "__main__":
    main()