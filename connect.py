from flask import Flask, render_template, request, url_for
from pymongo import MongoClient
import time

app = Flask(__name__)
app.jinja_env.auto_reload = True  # 템플릿 자동로드 활성화 (개발 환경에서만 사용)
app.config['TEMPLATES_AUTO_RELOAD'] = True  # 템플릿 자동로드 활성화 (개발 환경에서만 사용)

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
    area_nm_falg_nm = request.args.get('area_nm_falg_nm', '')
    
    projection = {
        "BOOK_TITLE_NM": 1,
        "AUTHR_NM": 1,
        "BOOK_INTRCN_CN": 1,
        "PUBLISHER_NM": 1,
        "BOOK_IMAGE_NM": 1,
        "RANK_CO": 1,
        "AREA_NM": 1
    }

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
        query["AREA_NM"] = area_nm_falg_nm

    sort_key = None  # 초기값 설정

    # 하나의 레이블만 선택되었을 때 정렬을 수행할 필드 선택
    if anals_pd_cd_nm and not (age_flag_nm or sexdstn_flag_nm):
        sort_key = "ANALS_PD_CD_NM"
    elif age_flag_nm and not (anals_pd_cd_nm or sexdstn_flag_nm):
        sort_key = "AGE_FLAG_NM"
    elif sexdstn_flag_nm and not (anals_pd_cd_nm or age_flag_nm):
        sort_key = "SEXDSTN_FLAG_NM"
    elif area_nm_falg_nm and not (anals_pd_cd_nm or age_flag_nm or sexdstn_flag_nm):
        sort_key = "AREA_NM"

    data = list(collection.find(query, projection).sort("RANK_CO", 1).limit(20))

    # sections 리스트 동적 생성
    title_set = set()
    sections = []
    
    for item in data:
        if area_nm_falg_nm and item.get('ANALS_TY_CD') == 3:
            section = {
                'url': 'URL_1',
                'image': item.get('BOOK_IMAGE_NM', url_for('static', filename='images/placeholder.png')),
                'title': item.get('BOOK_TITLE_NM', 'No Title'),
                'description': item.get('BOOK_INTRCN_CN', 'No Description'),
                'rank': item.get('RANK_CO', 'No RANK'),
                'authr': item.get('AUTHR_NM', 'No Authr'),
                'publi': item.get('PUBLISHER_NM', 'No publi'),
                'area': item.get('AREA_NM', ' ')
            }
        else:
            section = {
                'url': 'URL_1',
                'image': item.get('BOOK_IMAGE_NM', url_for('static', filename='images/placeholder.png')),
                'title': item.get('BOOK_TITLE_NM', 'No Title'),
                'description': item.get('BOOK_INTRCN_CN', 'No Description'),
                'rank': item.get('RANK_CO', 'No RANK'),
                'authr': item.get('AUTHR_NM', 'No Authr'),
                'publi': item.get('PUBLISHER_NM', 'No publi'),
                'area': item.get('AREA_NM', item.get('AGE_FLAG_NM', ' '))
            }

        title = section.get('title')
        if title not in title_set:
            sections.append(section)
            title_set.add(title)

    # 정렬 수행
    sections.sort(key=lambda x: x.get('rank', 'No RANK'))
    return render_template('landing.html', sections=sections)






@app.route('/generic', methods=['GET'])
def generic():
    pipeline = [
        { '$match' : { 'ANALS_TY_CD_NM' : "지역별", 'AREA_NM': "충북", 'ANALS_PD_CD': "p2"}},
        { '$sort' : { 'RANK_CO' : 1 } },
        { '$limit' : 10 },
        { '$project' : {'_id': 0, 'RANK_CO' : 1, 'BOOK_TITLE_NM' : 1, 'PUBLISHER_NM' : 1, 'BOOK_INTRCN_CN' : 1, 'BOOK_IMAGE_NM' : 1}}
    ]
    result = list(collection.aggregate(pipeline))
    
    return render_template('generic.html', data=result)



@app.route('/mzman', methods=['GET', 'POST'])
def mzman():
    pipeline = [
        {
            '$match': {
                'ANALS_PD_CD': "p2",
                'SEXDSTN_FLAG_NM': "남성",
                'ANALS_TY_CD_NM': "연령 및 성별",
                '$or': [
                    {'AGE_FLAG_NM': "20대"},
                    {'AGE_FLAG_NM': "30대"}
                ]
            }
        },
        { '$sort': { 'RANK_CO': 1 } },
        { '$limit': 40 },
        { '$project' : {'_id': 0, 'RANK_CO' : 1, 'BOOK_TITLE_NM' : 1, 'PUBLISHER_NM' : 1, 'BOOK_INTRCN_CN' : 1, 'BOOK_IMAGE_NM' : 1}}
    ]

    result = list(collection.aggregate(pipeline).sort("RANK_CO", 1))

    # 중복 제거를 위한 세트(set) 생성
    title_set = set()
    unique_result = []

    for item in result:
        title = item.get('BOOK_TITLE_NM')
        if title not in title_set:
            unique_result.append(item)
            title_set.add(title)

    return render_template('generic.html', data=unique_result)

@app.route('/mzwoman')
def mzwoman():
    pipeline = [
        {
            '$match': {
                'ANALS_PD_CD': "p2",
                'SEXDSTN_FLAG_NM': "여성",
                '$or': [
                    {'AGE_FLAG_NM': "20대"},
                    {'AGE_FLAG_NM': "30대"},
                    {'ANALS_TY_CD_NM': "연령 및 성별"},
                    {'ANALS_TY_CD_NM': "지역별"},
                    {'AREA_NM': "인천"},
                    {'AREA_NM': "경기"},
                    {'AREA_NM': "서울"}
                ]
            }
        },
        {
            '$sort': {'RANK_CO': 1}
        },
        {
            '$limit': 40
        },
        {
            '$project': {
                '_id': 0,
                'RANK_CO': 1,
                'BOOK_TITLE_NM': 1,
                'PUBLISHER_NM': 1,
                'BOOK_INTRCN_CN': 1,
                'BOOK_IMAGE_NM': 1
            }
        }
    ]


    result = list(collection.aggregate(pipeline).sort("RANK_CO", 1))

    # 중복 제거를 위한 세트(set) 생성
    title_set = set()
    unique_result = []

    for item in result:
        title = item.get('BOOK_TITLE_NM')
        if title not in title_set:
            unique_result.append(item)
            title_set.add(title)

    return render_template('generic.html', data=unique_result)


@app.route('/indexing', methods=['GET'])
def indexing():
    # Create an index
    collection.create_index([('ANALS_TY_CD', 1), ('ANALS_TY_CD_NM', 1), ('ANALS_PD_CD_NM', 1), ('ANALS_PD_CD', 1)], name="index_anals")

    query = {
        'ANALS_TY_CD': 3,
        'ANALS_TY_CD_NM': '지역별',
        'ANALS_PD_CD_NM': '30일',
        'ANALS_PD_CD': 'p2'
    }

    pipeline = [
        { '$match': query },
        { '$sort': { 'RANK_CO': 1 } },
        { '$limit': 100 },
        { '$project': { '_id': 0, 'ANALS_TY_CD': 1, 'ANALS_TY_CD_NM': 1, 'ANALS_PD_CD_NM': 1, 'ANALS_PD_CD': 1, 'RANK_CO': 1, 'BOOK_TITLE_NM': 1, 'PUBLISHER_NM': 1, 'BOOK_INTRCN_CN': 1, 'BOOK_IMAGE_NM': 1 } }
    ]

    # Using index
    start_time_indexed = time.time()
    indexed_result = list(collection.aggregate(pipeline))
    end_time_indexed = time.time()

    # Remove duplicates using a set
    unique_indexed_result = list({item['BOOK_TITLE_NM']: item for item in indexed_result}.values())

    # Without using index
    start_time_non_indexed = time.time()
    non_indexed_result = list(collection.find(query).sort("RANK_CO", 1).limit(100))
    end_time_non_indexed = time.time()

    # Remove duplicates using a set
    unique_non_indexed_result = list({item['BOOK_TITLE_NM']: item for item in non_indexed_result}.values())

    # Calculate indexing time
    indexing_time = (end_time_indexed - start_time_indexed)*100
    non_indexing_time = (end_time_non_indexed - start_time_non_indexed)*100

    return render_template('indexspeed.html', indexed_data=unique_indexed_result, non_indexed_data=unique_non_indexed_result, indexing_time=indexing_time, non_indexing_time=non_indexing_time)



if __name__ == '__main__':
    app.run()