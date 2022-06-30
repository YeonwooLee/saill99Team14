import apiUtil
import pymongo
import dbControl

#get요청 covid
def covidAlertsGet(numData=50,subject='covidAlert'):
    #API에 요청하는 부분
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
    print(dataFromDb[0].keys())
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

def covidBoardOne(insertAt):
    insertAt = int(insertAt)
    return dbControl.get_one_covid(insertAt)


if __name__=="__main__":
    print(covidBoardOne('1656546117223814700'))

    # temp = covidAlertsGet(50)

    #apiUtil.write_json()
    # for i in temp:
    #     print(i['title'],i['wrtDt'],i['id'],i['insertAt'])

