# Telegram Advance Security (TAS) - Core Module
from telegram import *
from telegram.ext import *
from telegram.constants import ParseMode
from . import *

PUBLIC_KEY = ""


def main():
    print(read_config())

if __name__ == "__main__":
    main()