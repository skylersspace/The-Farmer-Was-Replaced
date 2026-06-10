# for i in range(10):
# 	print_string = ""
# 	for j in range(i):
# 		print_string = print_string + "*"
# 	quick_print(print_string)

# Minecraft fill command 
# /fill <from> <to> <block> [destroy|hollow|keep|outline|replace]
# /fill <from> <to> <block> replace [<filter>]

x, y, z = (42, 58, 588)
x1, y1, z1 = (x, y, z)
x2, y2, z2 = (x, y, z)
dx, dy, dz = (1, 1, 1)
height = 15

command_start = "/fill"
command_block = "cobblestone"

quick_print(command_start, x1, y1, z1, x2, y2, z2, command_block)

for i in range(1, height):
	# Move level up one
	z1 = z1 + dz
	z2 = z1

	# Expand width
	x1 = x1 - dx
	x2 = x2 + dx
	y1 = y1 - dy
	y2 = y2 + dy

	quick_print(command_start, x1, y1, z1, x2, y2, z2, command_block)

# Example Output
# /fill 42 58 588 42 58 588 cobblestone
# /fill 41 57 589 43 59 589 cobblestone
# /fill 40 56 590 44 60 590 cobblestone
# /fill 39 55 591 45 61 591 cobblestone
# /fill 38 54 592 46 62 592 cobblestone
# /fill 37 53 593 47 63 593 cobblestone
# /fill 36 52 594 48 64 594 cobblestone
# /fill 35 51 595 49 65 595 cobblestone
# /fill 34 50 596 50 66 596 cobblestone
# /fill 33 49 597 51 67 597 cobblestone
# /fill 32 48 598 52 68 598 cobblestone
# /fill 31 47 599 53 69 599 cobblestone
# /fill 30 46 600 54 70 600 cobblestone
# /fill 29 45 601 55 71 601 cobblestone
# /fill 28 44 602 56 72 602 cobblestone