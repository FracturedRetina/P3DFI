class Point:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z
