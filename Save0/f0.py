test = [5,8,1,6,2,9,10,3,7,4]
bubble_sort(test)
quick_print(test)


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



point_list = [(0,0),(0,1),(0,9),(2,2),(9,9),(9,0),(1,1),(5,5),(1,9),(0,2),(2,0),(5,0)]

for i in range (len(point_list) - 1):
	quick_print(is_adjacent(point_list[0], point_list[i+1]))
	
def test_func():
	quick_print("Hello")
	
	def nested_func():
		quick_print("does this work?")
	
	nested_func()

test_func()