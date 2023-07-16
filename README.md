# Wishlist Bot for Telegram

Bot for creating and storing wishlists

## Getting started

For personal use go to https://t.me/wishlist_organizer_bot. All instructions for commands are available here.

As usual (from 8-9 AM to 11-12 PM) it will be open,
but when the laptop is charging, on which the bot is hosted - it will be stopped for maximum 1.5 hours. In such unlucky
case, write to https://t.me/muhammaduss any time.

### Installation

1. Clone the repository (you can find HTTPS link on Code button)
2. Install Telebot library, run on terminal: ```pip install pyTelegramBotAPI```
3. Rename config.py to config_local.py
4. In config_local.py put your bot's token (you can obtain your own bot and token for it in https://t.me/BotFather)
5. For running bot on your machine run on terminal: ```python bot.py```

Feel free to use code and change it in your interests.
If you find good feature which can be added, you are welcome! You can fork the repository and do a pull request

### Usage

Here bot commands:

```/start``` - start the bot and see available commands

```/new_wishlist``` - create a new wishlist

```/open_wishlist``` - open and show existing wishlist

```/add``` - add items to wishlist

```/delete``` - delete items from wishlist

```/delete_wishlist``` - delete chosen wishlist

```/all_wishlists``` - show all existing wishlists

```/commands``` - list of commands for operating with wishlists
