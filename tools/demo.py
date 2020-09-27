import pendulum


# print(pendulum.now())
# print(pendulum.now().format('YYMMDDHHmmss SSSSSS'))
# print(len(pendulum.now().format('YYMMDDHHmmssSSSSSS')))

# from decimal import Decimal


# print(0.1 + 0.2)
# print(12 * 0.8)
# print(Decimal(0.1) + Decimal(0.2))
# print(Decimal(str(12)) * Decimal(str(0.8)) * 100 / 100)
# print(type(Decimal('0.1')))
# print(float(str(Decimal('1') / Decimal('0.3'))))
# print(Decimal('1') / Decimal('0.3'))
# print(float(round(Decimal('2') / Decimal('0.3'), 3)))

# import random
# def random_domain():
#     char_range = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', 'q', 'w', 'e',
#                   'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j',
#                   'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
#     return ''.join(map(lambda _: random.choice(char_range), range(6)))

# print(random_domain())

# import requests

# resp = requests.get('https://api.jisuapi.com/caipiao/query?appkey=yourappkey&caipiaoid=13&issueno=', params={'username': 'dd发送'})
# print(resp.json().get('status'))


# import re

# ret = re.match(r"^1[35678]\d{9}$", '22')
# print(ret)

# class A:
#     a = 3
#     b = a

# print([*[1,2,3]])

print(pendulum.now().add(days=-30))
