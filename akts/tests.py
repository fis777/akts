from akts.models import Tickets

tickets = Tickets()

# Не определен
result = tickets.byServiceprovider(1)
print(result)
print('Всего неопределен вариант',result.__len__())

# ЗИП 15
result = tickets.byServiceprovider(2)
print(result)
print('Всего ЗИП 15',result.__len__())

# ЗИП 16
result = tickets.byServiceprovider(3)
print(result)
print('Всего ЗИП 16',result.__len__())

# ЗИП 17
result = tickets.byServiceprovider(4)
print(result)
print('Всего ЗИП 17',result.__len__())

# ЗИП 404
result = tickets.byServiceprovider(5)
print(result)
print('Всего ЗИП 404',result.__len__())

# Без денег
result = tickets.byServiceprovider(6)
print(result)
print('Всего без денег',result.__len__())

# Корекс
result = tickets.byServiceprovider(7)
print(result)
print('Всего гарантийных',result.__len__())

# Актион 751
result = tickets.byServiceprovider(8)
print(result)
print('Всего Актион 751',result.__len__())
