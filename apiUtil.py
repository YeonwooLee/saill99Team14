import json
import pathlib
import requests
import pandas as pd
from xml.etree import ElementTree as ET

def load_json(filename):
    file = pathlib.Path(str(filename) + '.json')
    file_text = file.read_text(encoding='utf-8-sig')
    return json.loads(file_text)

def write_json(filename, data):
    with open(str(filename) + '.json', 'w', encoding='UTF-8-sig') as file:
        file.write(json.dumps(data, ensure_ascii=False))

def url_maker(subject):

    subjectDict = load_json('static/conf/apiConf')[subject]

    url = subjectDict['url']
    params = subjectDict['params']

    if params == {}: # 파라미터 없는 경우
        return url
    else: # 파라미터 있는 경우
        url += "?"
        for param in params:
            if params[param]=='':
                continue
            url += param+"="+str(params[param])+"&"
        url = url[:-1] #끝 & 제거
    # print("url = ",url)
    return url

def reqGetXml(url):
    xmlContent = requests.get(url).content
    return xmlContent



def xmlsToDicts(xmlStr):
    # url = url_maker('corona')
    # res = requests.get(url)
    tree = ET.fromstring(xmlStr)
    ET.indent(tree, space="  ")
    # ET.dump(tree)
    items = tree[1][0]
    listOfItems = [[i.text for i in item] for item in items]

    columns = [i.tag for i in items[0]]
#    print(url)
    df = pd.DataFrame(listOfItems, columns=columns)
    result = []
    # print(df.columns)
    for i in range(len(df)):
        temp_dict = {}
        for key in df.columns:
            temp_dict[key] = df.iloc[i][key]
        result.append(temp_dict)
    return result


def finalDict(subject):
    url = url_maker(subject)
    xmlStr = reqGetXml(url)
    results = xmlsToDicts(xmlStr)
    return results

def setParam(subject,param,value):
    datas = load_json('static/conf/apiConf')
    datas[subject]['params'][param]=value
    write_json('static/conf/apiConf',datas)



if __name__=="__main__":
    setParam("flag",'pageNo',33333)

