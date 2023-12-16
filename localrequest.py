import requests

#res = requests.get("http://127.0.0.1:3000/main")

# data = {'driver_first_name': "dwq", 'driver_last_name':"qwd", 'driver_patronymic': "bty4", 'driver_age': 43, 'driver_rank': "reb", 'mobile_phone': "435423", 'mail': "dqwdfre", 'a1_category': True, 'b1_category': True, 'login': "user1", 'password': "x4mws89Jf"}
# res = requests.post("http://localhost:5000/driver", json=data)
# print(res.json())

# data = {'driver_first_name': "dwq", 'driver_last_name':"qwd", 'driver_patronymic': "bty4", 'driver_age': 43, 'driver_rank': "reb", 'mobile_phone': "435423", 'mail': "dqwdfre", 'a1_category': True, 'b1_category': True, 'login': "user1", 'password': "x4mws89Jf"}
# res = requests.post("https://driver-monitoring-application-d48766f2cbe0.herokuapp.com/driver", json=data)
# print(res.json())

# data = {'driver_first_name': "dwq", 'driver_last_name':"qwd", 'driver_patronymic': "bty4", 'driver_age': 43, 'driver_rank': "reb", 'mobile_phone': "435423", 'mail': "dqwdfre", 'a1_category': True, 'b1_category': True, 'login': "user1", 'password': "x4mws89Jf"}
# res = requests.post("http://localhost:5000/driver", json=data)
# print(res)

# res = requests.delete("https://driver-monitoring-application-d48766f2cbe0.herokuapp.com/driver/1")
# print(res.json())

res = requests.delete("http://127.0.0.1:5000/driver/1")
print(res.json())

# data = {'driver_first_name': "dwq", 'driver_last_name':"qwd", 'driver_patronymic': "bty4", 'driver_age': 43, 'driver_rank': "reb", 'mobile_phone': "435423", 'mail': "dqwdfre", 'a1_category': True, 'b1_category': True, 'login': "user1", 'password': "x4mws89Jf"}
# res = requests.get("https://driver-monitoring-application-d48766f2cbe0.herokuapp.com/main")
# print(res.json())