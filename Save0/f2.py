point_list = [(0,0),(0,1),(0,9),(2,2),(9,9),(9,0),(1,1),(5,5),(1,9),(0,2),(2,0),(5,0)]

for i in range (len(point_list) - 1):
	quick_print(is_adjacent(point_list[0], point_list[i+1]))
	
def test_func():
	quick_print("Hello")
	
	def nested_func():
		quick_print("does this work?")
	
	nested_func()

test_func()