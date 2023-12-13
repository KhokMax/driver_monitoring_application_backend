import requests

#res = requests.get("http://127.0.0.1:3000/main")

# data = {'driver_first_name': "dwq", 'driver_last_name':"qwd", 'driver_patronymic': "bty4", 'driver_age': 43, 'driver_rank': "reb", 'mobile_phone': "435423", 'mail': "dqwdfre", 'a1_category': True, 'b1_category': True, 'login': "user1", 'password': "x4mws89Jf"}
# res = requests.post("http://127.0.0.1:3000/driver", json=data)
# print(res.json())

res = requests.delete("http://127.0.0.1:3000/driver/b4ecc474-f071-4494-8005-7e5970b02ad9")
print(res.json())