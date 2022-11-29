import os

from flask import Flask, render_template
from dotenv import load_dotenv
import requests

load_dotenv()

w_api_key = os.getenv('WEATHER_API')
er_api_key = os.getenv('EXCHANGE_API')

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html', resp_w=(round(requests.get(f"https://api.openweathermap.org/data/2.5/"
                                                                   f"weather?q=minsk&appid={w_api_key}").json()['main'][
                                                          'temp'] - 273.15, 2)),
                           resp_er=(requests.get(f"https://currate.ru/api/?get=rates&pairs=USDBYN&key="
                                                 f"{er_api_key}")).json()["data"]["USDBYN"])


@app.route('/weather/')
@app.route('/weather/<string:city>')
def weather(city=None):
    if city is None:
        resp_w = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=minsk&appid={w_api_key}")
    else:
        resp_w = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={w_api_key}")
    return render_template('weather.html', resp_w=f"{resp_w.json()['name']} : "
                                                  f"{round(resp_w.json()['main']['temp'] - 273.15, 2)}")


@app.route('/exchange_rate')
@app.route('/exchange_rate/<string:cur>')
def exchange_rate(cur=None):
    if cur is None:
        cur = "BYN"
        resp_er = requests.get(f"https://currate.ru/api/?get=rates&pairs=USD{cur}&key={er_api_key}")
        return render_template("exchange.html", cur=cur.upper(), resp_er=f'{resp_er.json()["data"]["USDBYN"]}')
    else:
        resp_er = requests.get(f"https://currate.ru/api/?get=rates&pairs={cur.upper()}USD&key={er_api_key}")
        return render_template("exchange.html", cur=cur.upper(), resp_er=resp_er.json()["data"][f"{cur.upper()}USD"])


if __name__ == '__main__':
    app.run()
