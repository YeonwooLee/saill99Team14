import apiUtil
import pymongo
import dbControl

#get요청 covid
def covidAlertsGet(numData=50,subject='covidAlert'):
    # dataFromApi = apiUtil.finalDict(subject)
    # for i in dataFromApi:
    #     try:
    #         dbControl.basic_insert(subject,i)
    #     except pymongo.errors.DuplicateKeyError as e:
    #         print(i['title'],i['id'],"<<중복자료")
    #         continue
    dataFromDb = dbControl.get_all_data(subject)
    dataFromDb=dataFromDb[:numData]#클라이언트에 넘겨줄 데이터
    dataFromDb.sort(key=lambda x:x['insertAt']) #정렬 - 삽입시간
    #dataFromDb.sort(key=lambda x: x['wrtDt'])  # 정렬 - 날짜
    #dataFromDb.sort(key=lambda x: x['title']) #정렬 - 제목
    # print("!!!@@@")
    
    #요청 - 번호삽입
    num=0
    for i in dataFromDb:
        i['num']=num
        num+=1
    return dataFromDb

#post요청 covid 갱신지점 아직 없음
def covidAlertsPost(numData=50,subject='covidAlert'):
    dataFromApi = apiUtil.finalDict(subject)
    for i in dataFromApi:
        try:
            dbControl.basic_insert(subject,i)
        except pymongo.errors.DuplicateKeyError as e:
            print(i['title'],i['id'],"<<중복자료")
            continue


if __name__=="__main__":

    temp = covidAlerts(50)
    confNow = apiUtil.load_json('static/conf/apiConf')
    confNow['covidAlert']['confTblRowId']='62bcc1a9fab81cf31ba2d75d'
    #apiUtil.write_json()
    for i in temp:
        print(i['title'],i['wrtDt'],i['id'],i['num'])

    # coronaList = apiUtil.finalDict(subject)
    # num=0
    # for i in coronaList:
    #     num+=1
    #     print(num,end="|")
    #     print(i['countryName'], end='|')
    #     print(i['title'], end='|')
    #     print(i['wrtDt'])
