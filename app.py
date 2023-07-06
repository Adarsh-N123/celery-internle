import os
import random
from flask import Flask, flash, render_template, redirect
from tasks import add
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', "super-secret")

def store_result(x, y):
    with open('results.txt', 'a') as file:
        file.write(f'x: {x}, y: {y}\n')

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/generate-and-add')
def generate_and_add():
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    add.delay(x, y)
    store_result(x, y)
    return "Random numbers generated and added."

# Create a scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(generate_and_add, 'interval', minutes=2)
scheduler.start()

if __name__ == '__main__':
    app.run()
