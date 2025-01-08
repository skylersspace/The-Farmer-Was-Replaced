def hello_world():
    quick_print("Hello World!")

def run_func(func):
    func()

def test_func():
    func_variable = "I am a function variable."

    #These are effectively private functions that cannot be accessed outside of this function
    def sub_func1():
        quick_print("I am a sub-function. The first one!")

    def sub_func2():
        quick_print("I am a sub-function. The second one!")
        
    sub_func1()
    sub_func2()

def default_func(a = 0):
    quick_print (a)

#run_func(hello_world)

#test_func()

#default_func()
#default_func(3)

#Overload?

#def too_many(a, b):
#    quick_print("Normal", a, b)

def too_many(a, b, c = 0):
    quick_print("Overloaded", a, b, c)

too_many(1,2)
too_many(1,2,3)

crop_func = dict()
crop_func["test"] = hello_world

crop_func["test"]()