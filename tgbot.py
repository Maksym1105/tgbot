import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests

bot = telebot.TeleBot("SECRET_KEY")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # keyboard

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("News")
    button2 = types.KeyboardButton("Matches")
    button3 = types.KeyboardButton("Results")

    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Weclome, what do you want to see".format(message.from_user, bot.get_me()),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def button_settings(message):
    global news
    if message.chat.type == 'private':

        # button News

        if message.text == 'News':
            url_news = "https://www.hltv.org/"
            response = requests.get(url_news)
            soup = BeautifulSoup(response.content, "html.parser")
            news_info = []
            items = soup.find("div", class_="standard-box standard-list")
            for item in items:
                news_info.append({
                    "title": item.find("div", class_="newstext").text,
                    "link": item["href"]
                })

            for news in news_info:
                a = f'{news["title"]} : {"https://www.hltv.org/"}{news["link"]}'

                bot.send_message(message.chat.id, a)

        # button Matches

        elif message.text == "Matches":
            url_news = "https://www.hltv.org/matches"
            response = requests.get(url_news)
            soup = BeautifulSoup(response.content, "html.parser")
            match_items = soup.find("div", {"class": "upcomingMatchesSection"})
            match_info = [item["href"] for item in match_items.findAll("a", {"class": "match a-reset"})]


            for match in match_info:
                b = "https://www.hltv.org/" + match

                bot.send_message(message.chat.id, b)


        # button Results

        elif message.text == "Results":
            url_news = "https://www.hltv.org/results"
            response = requests.get(url_news)
            soup = BeautifulSoup(response.content, "html.parser")

            results_items = soup.find("div", {"class": "results-holder allres"})
            a = results_items.find("div", {"class": "results-sublist"})
            results_info = [item["href"] for item in a.findAll("a", {"class": "a-reset"})]
            for results in results_info:
                c = "https://www.hltv.org/" + results

                bot.send_message(message.chat.id, c)


        else:
            bot.send_message(message.chat.id, "Sorry, i don't know this command...")


bot.infinity_polling()