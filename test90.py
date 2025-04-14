def b():
    print('iam b')
    def a():
        return True
    return a()

if b() == True:
    print('yeah')
else:
    print('no')