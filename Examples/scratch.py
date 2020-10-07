# def example(n):
#     i = 1
#     while i <= n:
#         yield i
#         i += 1
#
# print("hello")
#
# print("goodbye")
#
# if __name__ == '__main__':
#     for i in [1,2,3,4]:
#         example(i)

def example(n):
    i = 1
    while i <= n:
        yield [1,2,3]
        i += 1

def test(x):
    # con = []
    # for i in example(x):
    #     yield i
    return example(x)

def test1(x):
    # con = []
    # for i in example(x):
    #     yield i
    return test(x)

def test2(x):
    # con = []
    # for i in example(x):
    #     yield i
    return test1(x)
def test3(x):
    # con = []
    # for i in example(x):
    #     yield i
    return test2(x)
def test4(x):
    # con = []
    # for i in example(x):
    #     yield i
    return test3(x)
def test5(x):
    # con = []
    # for i in example(x):
    #     yield i
    # print(next(test4(x)))
    # exit()
    return test4(x)

print("hello")

# print(example(3)) # can't debug
# print(test(3))
print(next(test5(3)))
# print([i for i in test5(3)])
# print([i for i in test2(3)])
# print([i for i in test(3)])
# x = [i for i in test(3)]
# print([i for i in example(3)])

# for n in example(3):
#     print(n)

print("goodbye")
