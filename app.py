from flask import Flask, render_template, request, jsonify #기본 라이브러리들
from pymongo import MongoClient #디비 연결 라이브러리
import certifi
from datetime import datetime
import covidService


ca = certifi.where()
client = MongoClient('mongodb+srv://sail99Team14:sail99pw14@cluster0.zlqekaz.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbCovid

app = Flask(__name__)



@app.route('/')
def home():

    return render_template('index2.html') #템플릿 리턴시 이렇게

@app.route('/db-check')
def dbCheck():
    temp_data = {"time":datetime.now()}
    db.testTbl.insert_one(temp_data) #db에 현재시간 입력

    connectTimes= list(db.testTbl.find({},{'_id':False}))
    lastConnect = connectTimes[-1]
    return jsonify({'전체 접속 시간':connectTimes,'마지막 접속시간':lastConnect}) #데이터 리턴시 이렇게


#요청받으면 api요청 -> 정리해서 db등록 -> db에서 꺼내옴
@app.route("/coivd", methods=["GET"])
def covidAlertget():
    insertAt=request.args.get('insertAt')

    if insertAt==None:
        print("게시글 리스트 요청")
        datas = covidService.covidAlertsGet()
        for i in datas:
            print(i['title'], "insertAt:", i['insertAt'])
            i['insertAt'] = str(i['insertAt'])

    else:
        print("게시글 내용 요청 insertAt:",insertAt)
        datas = covidService.covidBoardOne(insertAt)
        print("data = ", datas['title'], datas['insertAt'])
        # return datas['contentHtml'] # 제공되는 html 사용시
        return render_template('window2.html',datas=datas) #자체 html 사용시


    return jsonify(datas) #데이터 리턴시 이렇게

#데이터갱신
@app.route("/coivd", methods=["POST"])
def covidAlertpost():
    datas = covidService.covidAlertsPost()

    return jsonify(datas) #

#국기 이미지 요청 /flag?nnk=국가명
@app.route("/flag", methods=["GET"])
def flagLink():
    nameNationKorea = request.args.get('nnk')
    print('nameNationKorea=',nameNationKorea)
    datas = {'flagImgUrl':covidService.flag(nameNationKorea=nameNationKorea)}

    return jsonify(datas) #


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)