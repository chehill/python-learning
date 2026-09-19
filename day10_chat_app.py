# 第 9 课：交互式聊天程序 —— 你的第一个"别人也能用"的 AI 应用
# 阶段 0 · 第 2 周 · 第 3 天
#
# 这节课把你前面学的东西全部串起来：
#   第 2 课 字典（用 PERSONAS 查角色）
#   第 3 课 while 循环（不停地聊）
#   第 4 课 模块（import chat —— 你自己写的角色库！）
#   第 7 课 多轮历史管理（messages 追加）
#   第 8 课 防御性编程（失败就撤回，保持历史干净）

import os

# ---- 本机专属环境补丁（卡巴斯基 HTTPS 扫描）----
import truststore
truststore.inject_into_ssl()
# ------------------------------------------------

import requests
from dotenv import load_dotenv
import json
import chat                       # ← 导入你自己写的角色库（第 4 课的知识）

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


def ask(messages):
    """把【整个历史】发给模型，返回回答文字；失败返回 None"""
    payload = {"model": MODEL, "messages": messages}
    resp = requests.post(BASE_URL, headers=headers, json=payload, timeout=60)

    if resp.status_code != 200:
        print("请求失败:", resp.status_code, resp.text)
        return None

    return resp.json()["choices"][0]["message"]["content"]


def choose_persona():
    """列出可选角色，让用户选一个（直接复用 chat.py 里的 PERSONAS 字典）"""
    print("\n可选角色：")
    for key in chat.PERSONAS:
        print("  -", key)

    name = input("请选择角色（直接回车 = default）：").strip()
    if not name:
        name = "default"
    if name not in chat.PERSONAS:
        print(f"没有「{name}」这个角色，先用 default")
        name = "default"
    return name


def build_system(role):
    """取出角色对应的 system 提示词
    注意：PERSONAS 里存的是【函数】，所以要加 () 调用它才拿到字符串
    """
    return {"role": "system", "content": chat.PERSONAS[role]()}

def trim_history(messages,max_rounds=10):
    system=messages[0]
    rest=messages[1:]
    if  len(rest)>max_rounds*2:
        rest=rest[-max_rounds*2:]
    return [system]+rest

def main():
    role = choose_persona()
    messages = [build_system(role)]        # 历史里第一条永远是 system

    print(f"\n已进入聊天（当前角色：{role}）")
    print("命令：/exit 退出 ｜ /clear 清空记忆 ｜ /role 切换角色 | /save 保存聊天")

    while True:                             # 第 3 课的循环：一直聊到你喊停
        user_input = input("\n你：").strip()

        if not user_input:
            continue

        # ---- 特殊命令 ----
        if user_input == "/exit":
            print("再见！")
            break                           # 跳出循环，程序结束

        if user_input == "/clear":
            messages = [build_system(role)]  # 只留 system，历史全清
            print("（记忆已清空，它不记得刚才聊什么了）")
            continue

        if user_input == "/role":
            role = choose_persona()
            messages[0] = build_system(role)
            print(f"（角色已切换为 {role}）")
            continue
        if user_input=="/save":
            with open("chat_log.json","w",encoding="utf-8") as f:
                json.dump(messages,f,ensure_ascii=False,indent=2)
            print("聊天已保存至 chat_log.json")
            continue        

        # ---- 正常聊天 ----
        messages.append({"role": "user", "content": user_input})
        messages=trim_history(messages)

        answer = ask(messages)

        if answer is None:
            messages.pop()      # ★ 失败就把刚加的问题撤回，保持历史干净（第 8 课的防御思想）
            continue



        print(f"\n{role}：{answer}")
        messages.append({"role": "assistant", "content": answer})
        # 注意这一行：把 AI 的回答存回历史，下一轮对话它才"记得"（第 7 课练习 3 的核心）

if __name__ =="__main__":
    main()
