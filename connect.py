from flask import Flask, render_template, request, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB 연결
client = MongoClient('mongodb://localhost:27017/')
db = client['BookDB']
collection = db['Popular_borrow']
   
@app.route('/', methods=['GET', 'POST'])
def index():   
    return render_template('index.html')

@app.route('/landing', methods=['GET', 'POST'])
def landing():
    search_keyword = request.args.get('search_keyword', '')
    anals_pd_cd_nm = request.args.get('anals_pd_cd_nm', '')
    age_flag_nm = request.args.get('age_flag_nm', '')
    sexdstn_flag_nm = request.args.get('sexdstn_flag_nm', '')
    area_nm_falg_nm=request.args.get('area_nm_falg_nm', '')
    query = {
        "BOOK_TITLE_NM": {"$regex": search_keyword, "$options": "i"}
    }

    if anals_pd_cd_nm:
        query["ANALS_PD_CD_NM"] = anals_pd_cd_nm

    if age_flag_nm:
        query["AGE_FLAG_NM"] = age_flag_nm

    if sexdstn_flag_nm:
        query["SEXDSTN_FLAG_NM"] = sexdstn_flag_nm

    if area_nm_falg_nm:
        query["AREA_NM"] =area_nm_falg_nm

    sort_key = None  # 초기값 설정

    # 하나의 레이블만 선택되었을 때 정렬을 수행할 필드 선택
    if anals_pd_cd_nm and not (age_flag_nm or sexdstn_flag_nm):
        sort_key = "ANALS_PD_CD_NM"
    elif age_flag_nm and not (anals_pd_cd_nm or sexdstn_flag_nm):
        sort_key = "AGE_FLAG_NM"
    elif sexdstn_flag_nm and not (anals_pd_cd_nm or age_flag_nm):
        sort_key = "SEXDSTN_FLAG_NM"
    elif area_nm_falg_nm and not (anals_pd_cd_nm or age_flag_nm):
        sort_key = "AREA_NM"


    projection = {
        "BOOK_TITLE_NM": 1,
        "AUTHR_NM": 1,
        "BOOK_INTRCN_CN": 1,
        "PUBLISHER_NM": 1,
        "BOOK_IMAGE_NM": 1,
        "RANK_CO": 1,
        "AREA_NM": 1
    }
    data = list(collection.find(query, projection).limit(10))

    # sections 리스트 동적 생성
    sections = []
    for item in data:
        section = {
            'url': 'URL_1',
            'image': item.get('BOOK_IMAGE_NM', 'default_image.jpg'),
            'title': item.get('BOOK_TITLE_NM', 'No Title'),
            'description': item.get('BOOK_INTRCN_CN', 'No Description'),
            'rank' : item.get('RANK_CO','No RANK'),
            'authr' : item.get('AUTHR_NM','No RANK'),
            'publi' : item.get('PUBLISHER_NM','No RANK'),
            'area' : item.get('AREA_NM',' ')
        }
        sections.append(section)

    # 정렬 수행
    if sort_key:
        sections.sort(key=lambda x: x.get(sort_key) if x.get(sort_key) is not None else '')

    return render_template('landing.html', sections=sections)



@app.route('/generic')
def generic():
    data = collection.find_one({})
    return render_template('generic.html',data=data)

@app.route('/mzman')
def mzman():
    data = collection.find_one({})
    return render_template('mzman.html',data=data)

if __name__ == '__main__':
    app.run()