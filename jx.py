import json

def parse_data(data):
    # 检查到 data: 开头的数据 就删除
    if data.startswith("data:"):
        data = data[5:]
    else:

        return None

    parsed_data = json.loads(data)


    return parsed_data

if __name__ == '__main__':
    pass
    # 读入data.json
    with open("data.json", "r", encoding="utf-8") as f:
        data = f.read()
    # 换行符分割文本然后 去掉 前面的 data:
    datas = data.split("\n")
    hdjson = {}
    for v in datas:
        try:
            parsed_data = parse_data(v)
            print(parsed_data)
            if parsed_data['message']['content']['parts'] != None:
                hdjson = parsed_data
        except:
            pass
            print(v,"失败")

    print(hdjson)