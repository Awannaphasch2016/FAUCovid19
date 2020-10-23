def func():
    for i in range(10):
        yield  i

x = func()
for i in x:
    if i > 5:
        break
    print(i)
print('-----------')
for i in x:
    print(i)
try:
    print(next(x))
except StopIteration as e:
    raise e
except Exception as e:
    raise e

