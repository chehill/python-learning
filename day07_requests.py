# ---- 本机专属环境补丁（换电脑通常不需要）----
# 卡巴斯基会扫描 HTTPS 流量并用它自己的证书重新签发，而 Python 的 certifi 证书包
# 不认这张证书，所以报 SSLCertVerificationError。truststore 让 Python 改用
# Windows 系统证书库（已信任卡巴斯基根证书），在【不关闭安全校验】的前提下修好。
import truststore
truststore.inject_into_ssl()
# ------------------------------------------------

# 1.
import requests
url="https://api.github.com/users/chehill"
resp=requests.get(url)  

print("HTTP 状态码：",resp.status_code)
data=resp.json()
print("用户名：",data["login"])
print("公开仓库数：",data["public_repos"])
print("注册时间：",data["created_at"])
# 2.
resp=requests.get("https://api.github.com/users/abcdefg_hacker_123")
if resp.status_code==200:
    print("找到用户")
else:
    print("请求失败：",resp.status_code)
# 3.
resp=requests.get("https://api.github.com/repos/chehill/python-learning")
if resp.status_code==200:
    data=resp.json()
    print("stars:",data["stargazers_count"])
    print("描述：",data["description"])
    print("创建时间",data["created_at"])
else:
    print("请求失败：",resp.status_code)