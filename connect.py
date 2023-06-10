from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB 연결
client = MongoClient('mongodb://localhost:27017/')
db = client['BookDB']
collection = db['Recd_book_age']
   
@app.route('/')
def index():
    data = collection.find()
    return render_template('index.html')

@app.route('/landing')
def landing():
    data = collection.find()
    return render_template('landing.html')

@app.route('/generic')
def generic():
    return render_template('generic.html')

@app.route('/elements')
def elements():
    return render_template('elements.html')

if __name__ == '__main__':
    app.run()
    