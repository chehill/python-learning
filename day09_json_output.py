# 第 8 课：让 AI 返回结构化 JSON —— 从"聊天玩具"到"能干活的组件"
# 阶段 0 · 第 2 周 · 第 2 天
#
# 为什么重要：自然语言的回答程序没法直接用。要存数据库、要传给前端、要做 if 判断，
# 都必须先把 AI 的输出变成【结构化数据】。这一课之后，AI 才真正成为你的程序组件。

import os
import json

# ---- 本机专属环境补丁（卡巴斯基 HTTPS 扫描）----
import truststore
truststore.inject_into_ssl()
# ------------------------------------------------

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY  = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL")
MODEL    = os.getenv("LLM_MODEL")

if not API_KEY or not BASE_URL or not MODEL:
    print("❌ .env 配置不完整")
    raise SystemExit(1)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


# ============================================================
# 把"调用 AI + 解析 JSON"封装成一个函数（避免重复代码）
# ============================================================
def ask_json(user_prompt, system="你是信息抽取助手，只输出 JSON，不要输出任何解释。"):
    """让 AI 返回 JSON，并解析成 Python 字典；失败时返回 None"""
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt},
        ],
        # ★ 关键：强制 JSON 模式，AI 就不会裹 Markdown 代码块了
        "response_format": {"type": "json_object"},
    }

    resp = requests.post(BASE_URL, headers=headers, json=payload, timeout=60)

    if resp.status_code != 200:
        print("请求失败:", resp.status_code, resp.text)
        return None

    text = resp.json()["choices"][0]["message"]["content"]

    # 防御性编程：即使强制了 JSON 模式，也要防一手（工程习惯）
    try:
        return json.loads(text)          # JSON 字符串 -> Python 字典（第 5 课学过）
    except json.JSONDecodeError as e:
        print("❌ AI 返回的不是合法 JSON:", e)
        print("原始内容:", text)
        return None


# ============================================================
# 练习 1（示范）：把一段学习笔记变成结构化数据
# ============================================================
note = """
今天学了 Python 的字典，感觉用键取值很方便。
但是 KeyError 老是报错，后来改用 .get() 就好了。
明天打算学 requests 库，感觉有点难。
"""

# 注意这里用了 f-string 把变量拼进 Prompt —— 第 1 课说的"f-string 是拼 Prompt 的基础"，
# 今天真的用上了
result = ask_json(f"""
下面是我的学习笔记，请提取信息，严格按这些字段返回 JSON：
- title: 字符串，不超过 15 字
- tags: 字符串数组，2-4 个知识点标签
- summary: 字符串，一句话总结
- difficulty: 字符串，只能是"简单"、"中等"、"困难" 三个值之一

学习笔记：
{note}
""")

print("=== 练习 1：结构化提取结果 ===")
if result:
    print("标题:", result.get("title"))          # get 而不是 []，字段缺失不报错（第 2 课学过）
    print("标签:", result.get("tags"))
    print("总结:", result.get("summary"))
    print("难度:", result.get("difficulty"))
    print("\n完整字典:", result)


# ============================================================
# 练习 2（你来写）：换一个场景做信息抽取
# ============================================================
# 场景自选，比如：
#   ① 从一段聊天记录里提取"待办事项" -> {"todos": [{"who": ..., "what": ..., "when": ...}]}
#   ② 给一条商品评论做情感分析 -> {"sentiment": "正面/负面/中性", "score": 1-5, "reason": "..."}
#   ③ 从简历文本里提取 -> {"name": ..., "skills": [...], "years": 数字}
#
# 要求：自己定字段 -> 写 Prompt -> 调用 ask_json -> 打印结果
print("\n=== 练习 2：换场景做信息抽取 ===")

# ---- 下面开始写 ----
chat="""
妈妈：小明你明天早上记得叫你姐姐帮忙晒衣服
妈妈：对了，也叫妹妹收拾一下自己的房间，你也是
小明：收到
"""
result2=ask_json(f"""
下面是我的聊天记录，请提取信息，严格按这些字段返回 JSON：
-"todos":数组，简单总结，可以重复
-"who":字符串数组，谁去做，每个名字不超过5个
-"what":字符串，一句话总结
-"when":字符串，时间
聊天记录:
{chat}
""")
print("------自己做的------")
if result2:
    print("大家：",result2.get("todos"))
    print("谁：",result2.get("who"))
    print("事情：",result2.get("what"))
    print("时间：",result2.get("when"))
    print("\n完成的聊天记录",result2)



# ============================================================
# 练习 3（你来写）：把结果存成 JSON 文件，做成一个小工具
# ============================================================
# 第 5 课学过 json.dump，现在把它接上：
#   with open("note_analysis.json", "w", encoding="utf-8") as f:
#       json.dump(result, f, ensure_ascii=False, indent=2)
#
# 进阶（选做）：把 prompt 里的笔记改成从文件读取，做成
#   "输入任意一个 .txt 笔记 -> 输出结构化 JSON" 的小工具
print("\n=== 练习 3：结果存成 JSON 文件 ===")

# ---- 下面开始写 ----
def w_json_tool(result,name):
    with open(f"{name}.json","w",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
        
w_json_tool(result,"note_analysis")
print("已保存")
def analyze_note(txt_path,out_name):
    with open(txt_path,"r",encoding="utf-8") as f:
        note=f.read()

    result = ask_json(f"""
下面是我的学习笔记，请提取信息，严格按这些字段返回 JSON：
- title: 字符串，不超过 15 字
- tags: 字符串数组，2-4 个知识点标签
- summary: 字符串，一句话总结
- difficulty: 字符串，只能是"简单"、"中等"、"困难" 三个值之一

学习笔记：
{note}
""")
    if result:
        w_json_tool(result,out_name)
        print(f"已保存到{out_name}.json")
        return result
    else:
        print("提取失败")
        return None
result4=analyze_note("test_txt.txt","test_json")
if result4:
    print("标题:", result4.get("title"))
    print("标签:", result4.get("tags"))
    print("总结:", result4.get("summary"))
    print("难度:", result4.get("difficulty"))