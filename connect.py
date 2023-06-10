from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB 연결
client = MongoClient('mongodb://localhost:27017/')
db = client['BookDB']
collection = db['Popular_borrow']
   
@app.route('/')
def index():
    data = collection.find()
    return render_template('index.html')

@app.route('/landing')
def landing():
    query = {"AGE_FLAG_NM": "영유아(0~5)", "ANALS_TY_CD": 2 ,"ANALS_PD_CD_NM":"30일"}
    projection = {
        "BOOK_TITLE_NM": 1,
        "AUTHR_NM": 1,
        "BOOK_INTRCN_CN": 1,
        "PUBLISHER_NM": 1,
        "BOOK_IMAGE_NM": 1,
        "RANK_CO": 1,
        "PBLICTE_DE": 1,
        "ANALS_TY_CD": 1
    }
    data = list(collection.find(query, projection).sort("RANK_CO", 1).limit(20))
    return render_template('landing.html', data=data)

@app.route('/generic')
def generic():
    data = collection.find_one({})
    return render_template('generic.html',data=data)

if __name__ == '__main__':
    app.run()
    