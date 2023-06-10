from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB 연결
client = MongoClient('mongodb://localhost:27017/')
db = client['BookDB']
collection = db['Popular_borrow']
   
@app.route('/', methods=['GET', 'POST'])
def index():
    print('여기맞아요')
    if request.method == 'POST':
        print('여기에요')
        search_query = request.form['search_query']
        query = {
            "AGE_FLAG_NM": "영유아(0~5)",        
            "BOOK_TITLE_NM": {"$regex": search_query, "$options": "i"}
        }
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
<<<<<<< HEAD
        data = list(collection.find(query, projection))
        print('1')
        return render_template('index.html', data=data, search_query=search_query)
    else:
        data = collection.find()
        print('2')
        return render_template('index.html', data=data)
=======
        print('여기까지오나확인')
        data = list(collection.find(query, projection).sort("RANK_CO", 1).limit(20))
        return render_template('landing.html', data=data, search_query=search_query)
    else:
        query = {
            "AGE_FLAG_NM": "영유아(0~5)",
            "ANALS_TY_CD": 2,
            "ANALS_PD_CD_NM": "30일"
        }
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
        return render_template('index.html',data=data)
>>>>>>> 0d3a162b1bab5e9b8387708df8f525f7191ad8e0

@app.route('/landing', methods=['GET', 'POST'])
def landing():
    print('여기맞아요')
    if request.method == 'POST':
        print('여기에요')
        search_query = request.form['search_query']
        query = {
            "AGE_FLAG_NM": "영유아(0~5)",        
            "BOOK_TITLE_NM": {"$regex": search_query, "$options": "i"}
        }
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
<<<<<<< HEAD
        print('쿼리성공')
        data = list(collection.find(query, projection).sort("RANK_CO", 1).limit(2))
=======
        print('여기까지오나확인')
        data = list(collection.find(query, projection).sort("RANK_CO", 1).limit(20))
>>>>>>> 0d3a162b1bab5e9b8387708df8f525f7191ad8e0
        return render_template('landing.html', data=data, search_query=search_query)
    else:
        query = {
            "AGE_FLAG_NM": "영유아(0~5)",
            "ANALS_TY_CD": 2,
            "ANALS_PD_CD_NM": "30일"
        }
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
        return render_template('landing.html',data=data)


@app.route('/generic')
def generic():
    data = collection.find_one({})
    return render_template('generic.html',data=data)

if __name__ == '__main__':
    app.run()