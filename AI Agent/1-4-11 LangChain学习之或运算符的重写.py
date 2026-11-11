from setuptools.dist import sequence


class Test(object):
    def __init__(self,name):
        self.name=name
    def __or__(self,other): #该方法想返回自定义类型MySequence类
        return MySequence(self,other)
    def __str__(self):
        return self.name

class MySequence(object):
    def __init__(self,*args):
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)
    def __or__(self,other):
        self.sequence.append(other)
        return self
    def run(self):
        for arg in self.sequence:
            print(arg)

if __name__ == '__main__':
    a = Test("1")
    b = Test("2")
    c = Test("3")

    d = a|b|c #对|或运算符进行重写，使得d最终的结果为[1,2,3],类型是自定义类型MySequence类
    d.run()
    print(type(d))


