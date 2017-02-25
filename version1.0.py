from math import sqrt
import random

# Node of Tree
class Cell:

	def __init__(self, i, j, construction = 0):
		self.col, self.row = 0, 0
		self.i, self.j = i, j
		self.g, self.h, self.f = 0, 0, 0
		self.neighbors = list()
		self.previous = None
		self.wall = False
		
		if random.random() < 0.2:
			self.wall = True


	def __eq__(self, other):
		return self.i == other.i and self.j == other.j


	def add_neighbors(self, obj_field):
		row, col = obj_field.row, obj_field.col

		if self.__in_field(self.i + 1, self.j, row, col):
			self.neighbors.append(obj_field.field[self.i + 1][self.j])
		if self.__in_field(self.i - 1, self.j, row, col):
			self.neighbors.append(obj_field.field[self.i - 1][self.j])
		if self.__in_field(self.i, self.j + 1, row, col):
			self.neighbors.append(obj_field.field[self.i][self.j + 1])
		if self.__in_field(self.i, self.j - 1, row, col):
			self.neighbors.append(obj_field.field[self.i][self.j - 1])


	def __in_field(self, i, j, row, col):
		if i > row - 1 or i < 0:
			return False
		if j > col - 1 or j < 0:
			return False
		return True


	def heuristic(self, end):
		return sqrt(end.i**2 + end.j**2)

# Tree or Labirinth
class Field:

	def __init__(self, row, col):
		self.row, self.col = row, col
		self.field = list()
		self.__setup()


	def __setup(self):
		for i in range(self.row):
			temp = [0 for _ in range(self.col)]
			self.field.append(temp)

		for i in range(self.row):
			for j in range(self.col):
				self.field[i][j] = Cell(i, j)

		for i in range(self.row):
			for j in range(self.col):
				self.field[i][j].add_neighbors(self)



	# Finding successful path
	def backup(self, current):
		path = list()
		# Set root
		temp = current
		path.append(temp)

		while temp.previous is not None:
			path.append(temp.previous)
			temp = temp.previous

		return list(reversed(path))

	def show(self):
		for i in range(self.row):
			output = ''
			for j in range(self.col):
				output += '#' if self.field[i][j].wall else '+'
			print(output)


# Options
row, col = 50, 50
min_path = list()
output = ''

if __name__ == '__main__':
	# Create new Field
	box = Field(row, col)
	# New sets
	open_set = list()
	closed_set = list()

	# Set start vertex
	start = box.field[0][0]
	start.wall = False
	open_set.append(start)
	# Start index of vertex (index of min)
	winner = 0
	# Set end vertex
	end = box.field[row - 1][col - 1]
	end.wall = False
	# Show field
	box.show()

	"""
		START ALGORITHM A*
	"""

	while len(open_set) > 0:

		# Taking vertex with min 'f'
		for i in range(len(open_set)):
			if open_set[i].f < open_set[winner].f:
				winner = i
		# Assigning this vertex to 'current' 
		current = open_set[winner]

		if current == end:
			# Find path
			min_path = box.backup(current)
			print('Done!')
			break

		# Removing 'current' from 'open_set'
		open_set.remove(current)
		# And adding this vertex to 'closed_set'
		closed_set.append(current)

		for neighbor in current.neighbors:

			if neighbor not in closed_set and not neighbor.wall:
				temp_g = current.g + 1

				if neighbor in open_set:
					if temp_g < neighbor.g:
						neighbor.g = temp_g
				else: 
					neighbor.g = temp_g
					open_set.append(neighbor)

				neighbor.h = neighbor.heuristic(end)
				neighbor.f = neighbor.h + neighbor.g
				neighbor.previous = current

	# Printing path
	if len(min_path) > 0:
		for position in min_path:
			output += '(' + str(position.i) + ',' + str(position.j) + ')'
		print(output)
	else:
		print('no solution!')
