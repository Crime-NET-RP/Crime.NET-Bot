import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
	return "I'm alive"

def run():
	app.run(debug=True, port=int(os.environ.get('PORT', 33507)))

def keep_alive():
	t = Thread(target=run)
	t.start()
