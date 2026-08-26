# 1.
student=[
    {"name":"李火旺","age":20,"major":"计算机科学与技术"},
    {"name":"叶凡","age":22,"major":"软件工程"},
    {"name":"龙傲天","age":25,"major":"ai"}]
# 2.
for i in student:
    print(f"{i["name"]}学的是{i["major"]}")
# 3.
api_data={
    "status":"ok",
    "messages":[
        {"role":"user","content":"你好"},
        {"role":"assistant","content":"你好！请问有什么可以帮助您？"}
    ]
}
answer=api_data["messages"][1]["content"]
print(answer)