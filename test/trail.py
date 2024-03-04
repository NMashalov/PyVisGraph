class ClassHook:
    a = {
        '1': 1,
        '2': 2
    }

    def __init__(self,cfg:dict):
        ClassHook.a |= cfg  



print(ClassHook.a)
ClassHook({'3':3})
print(ClassHook.a)