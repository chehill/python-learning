import my_utils
import random 
# 1.
print(my_utils.add(1,1))
print(my_utils.greet("小明"))
# 2.
for i in range(10):
    if my_utils.is_even(i):
        print("是偶数")
    else:
        print("是奇数")
# 3.
def retry_call(max_attempts=5):
    attempt=0
    while attempt<max_attempts:
        attempt+=1
        if random.random()>0.5:
            return f"第{attempt}次调用成功！"
    return "调用失败,请检查网络"
print(retry_call())