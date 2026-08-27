# 1. if语句
import random

success = False
attempt=0
while attempt<5:
    attempt+=1
    print(f"第{attempt}次尝试调用模型...")
   
    if random.random()>0.5:
        print(f"第{attempt}次调用成功")
        success=True
        break
    else:
            print("失败，重试...")
if not success:
    print("调用失败，请检查网络")