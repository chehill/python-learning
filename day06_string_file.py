import json
# 1.字符串处理
raw=" 我的专业是 数据科学与大数据技术 "
print(raw.strip())
print("大数据" in raw)
# 2.文件读写
with open("day06_note.txt","w",encoding="utf-8") as f:
    f.write("我是张三\n")
    f.write("我的专业是数据科学与大数据技术\n")
    f.write("我爱学习\n")
with open("day06_note.txt","r",encoding="utf-8") as f:
    for line in f:
        print(line,end="")
# 3.JSON
api_data={
    "messages":[
    {"role":"user","content":"请问有什么帮助您的？"},
    {"role":"system","content":"你是一个蓝色的鲸鱼娘，性格傲娇"},
    {"role":"system","content":"你是偷奸耍滑的蓝色大肥鱼"}]
}
with open("chat.json","w",encoding="utf-8") as f:
    json.dump(api_data,f,ensure_ascii=False,indent=2)
with open("chat.json","r",encoding="utf-8") as f:
    chat_load=json.load(f)
print(chat_load["messages"][2]["content"])