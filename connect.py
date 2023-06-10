from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB 연결
client = MongoClient('mongodb://localhost:27017/')
db = client['BookDB']
collection = db['Recd_book_age']

@app.route('/')
def index():
    # MongoDB에서 데이터 가져오기
    data = collection.find()

    # HTML 템플릿 렌더링
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
