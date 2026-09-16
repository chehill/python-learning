# 第 7 课：调用大模型 API —— 让你的程序和 AI 说上话
# 阶段 0 · 第 2 周 · 第 1 天
#
# 本文件是"厂商无关"写法：换 DeepSeek / 智谱 / 硅基流动，只改 .env，不动代码

import os

# ---- 本机专属环境补丁（卡巴斯基 HTTPS 扫描）----
# 任何联网脚本都要这两行，换电脑通常不需要
import truststore
truststore.inject_into_ssl()
# ------------------------------------------------

import requests
from dotenv import load_dotenv

# ============================================================
# 1. 从 .env 读取配置（绝不要把 Key 写死在代码里）
# ============================================================
load_dotenv()                                  # 读取同目录下的 .env（不是 .env.example！）

API_KEY  = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL")
MODEL    = os.getenv("LLM_MODEL")

if not API_KEY or not BASE_URL or not MODEL:
    print("❌ 配置不完整，请检查仓库根目录下的 .env 文件")
    print("   需要这三行：LLM_API_KEY / LLM_BASE_URL / LLM_MODEL")
    raise SystemExit(1)

print(f"当前使用模型：{MODEL}")

# ============================================================
# 2. 请求三件套：地址、请求头、请求体
# ============================================================
headers = {
    "Authorization": f"Bearer {API_KEY}",   # 身份凭证：告诉服务器"我是谁"
    "Content-Type": "application/json",     # 告诉服务器"我发的是 JSON"
}

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "你是一位耐心的编程老师。回答要简洁。"},
        {"role": "user", "content": "用一句话解释什么是大语言模型。"},
    ],
}

# ============================================================
# 3. 发 POST 请求
# ============================================================
# json= 会自动把字典转成 JSON 并设置 Content-Type（第 5 课 json.dumps 的自动化版）
resp = requests.post(BASE_URL, headers=headers, json=payload, timeout=60)
print("状态码:", resp.status_code)

# ============================================================
# 4. 剥洋葱取出回答（第 2 课练过的结构，现在见到真的了）
# ============================================================
if resp.status_code == 200:
    data = resp.json()
    print("\nAI 回答：", data["choices"][0]["message"]["content"])
else:
    print("请求失败：", resp.status_code)
    print(resp.text)      # 出错时把服务器给的原因打出来 —— 排错全靠它


# ============================================================
# 练习 2（你来写）：感受 system 提示词的作用
# ============================================================
# 把上面 payload 里的 system 内容改掉，再发一次请求，对比风格差异：
#   比如 "你是一位喜欢用比喻的物理老师，回答不超过 50 字"
#   或者 "你是严肃的技术面试官，回答要挑毛病"
# 这就是"Prompt 工程"的起点：同一个问题，不同的 system 得到不同的答案。
print("\n=== 练习 2：修改 system 看风格变化 ===")

# ---- 下面开始写 ----
headers2={"Authorization":f"Bearer {API_KEY}",
            "Content-Type":"application/json"
          }
payload2={
    "model":MODEL,
    "messages":[
        {"role":"system","content":"你是一位喜欢用比喻的物理老师，回答不超过 50 字"},
        {"role":"user","content":"用一句话解释什么是大语言模型。"}
    ]
}
resp2=requests.post(BASE_URL,headers=headers2,json=payload2,timeout=60)
print("状态码：",resp2.status_code)
if resp2.status_code==200: 
    data2=resp2.json()
    print("AI:",data2["choices"][0]["message"]["content"])
else:
    print("请求失败：",resp2.status_code)
    print(resp2.text)





# ============================================================
# 练习 3（你来写，本课最重要）：让 AI "记住"上下文
# ============================================================
# 关键事实：大模型【没有记忆】，每次请求都是独立的、无状态的。
# 所谓"多轮对话"，其实是把历史消息一起再发一遍。理解这点，你就理解了 Agent 的地基。
#
# 做法提示：
#   messages = [{"role": "system", "content": "..."}]                先放 system
#   messages.append({"role": "user", "content": "我叫小明，你呢？"})  第 1 问
#   发请求 -> 拿到回答
#   messages.append({"role": "assistant", "content": 回答})           把 AI 的回答存回历史
#   messages.append({"role": "user", "content": "我叫什么名字？"})     第 2 问
#   再发一次请求 -> 看它能不能答出"小明"
#
# 进阶（选做）：把"发请求"写成一个函数 ask(messages)，避免复制粘贴代码
print("\n=== 练习 3：多轮对话（理解无状态）===")

# ---- 下面开始写 ----
def ask(messages):
    resp3=requests.post(BASE_URL,
                        headers=headers,
                        json={"model":MODEL,"messages":messages},timeout=60)
    if resp3.status_code==200:
        data3=resp3.json()
        return data3["choices"][0]["message"]["content"]
            
    else:
        print("请求失败:",resp3.status_code)
        return resp3.text
messages=[
        {"role":"system","content":"你是一位记性很好的助手，回答简洁"},
        {"role":"user","content":"我是小明，你是谁？"}
]
answer1=ask(messages)
print("AI-1:",answer1)
messages.append({"role":"assistant","content":answer1})
messages.append({"role":"user","content":"我叫什么名字？"})
answer2=ask(messages)
print("AI-2:",answer2)