def func1():
    print('in func1')
    raise Warning('warning in func1')

def func2():
    try:
        func1()
    except Exception as e:
        print('in func2 ')
        raise Warning(str(e))

def func3():
    try:
        func2()
    except Exception as e:
        print('in func3')
        print(str(e))

if __name__ == '__main__':
    func3()

