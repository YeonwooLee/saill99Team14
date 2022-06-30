import pymongo
import certifi
import apiUtil
import time
ca = certifi.where()
client = pymongo.MongoClient('mongodb+srv://sail99Team14:sail99pw14@cluster0.zlqekaz.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbCovid
#tableName = 'covidAlert'

#안전삽입 - 개발중
def safe_insert(tableName,data):
    conf_tbl_name = tableName+"Conf"
    table = db[tableName]
    conf_tbl = db[conf_tbl_name]
    confTblRowId = apiUtil.load_json('static/conf/apiConf')[tableName]["confTblRowId"] #confTbl 세팅용 유일행의 아이디


    #config테이블의 using이 0일 때만 동작
    print(conf_tbl.find_one({'_id':confTblRowId}))


    #config테이블의 유일행의 usingidx를 1로 변경
    #config테이블의 유일행의 usingidx를 현재행의 id로 변경
    #config테이블의 lastIdx를 가져옴
    #newIdx = lastIdx+1
    #현재행에 [index:newIdx] 추가
    #기본테이블에 현재행 추가
    #config테이블의 using을 0으로 변경


#일반삽입 - 
def basic_insert(table_name,data):
    data['insertAt']=time.time_ns()
    db[table_name].insert_one(data)
    # 중복아이디 pymongo.errors.DuplicateKeyError

# 데이터 전체 조회
def get_all_data(table_name):
    alerts = list(db[table_name].find({}, {'_id': False}))  # 댓글 목록 id:false 생략 불가능
    return alerts


# 테이블 리셋
def resetTable(tableName):
    db[tableName].delete_many({})

    #코로나 인덱스 생성
    if tableName == 'covidAlert':
        result = db[tableName].create_index([('id', pymongo.ASCENDING)],
                                      unique=True)
    print("리셋완료")
if __name__=="__main__":
    resetTable("covidAlert")
    # temp_dicts = apiUtil.finalDict('covidAlert') #임시용row list
    # temp_one_dict =temp_dicts[1] #임시용 row
    # #safe_insert("covidAlert",temp_one_dict)
    # basic_insert("covidAlert",temp_one_dict)
    pass