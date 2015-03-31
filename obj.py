from p3dfi import Point

class UV:
	def __init__(self, u, v):
		self.u = u
		self.v = v
	def __str__(self):
		return u + ", " + v

class ObjFace:
	def __init__(self, params):
		self.size = len(params)
		self.vertIndxs = []
		self.txtrIndxs = []
		self.normIndxs = []
		
		for param in params:
			split_param = param.split("/")
			
			self.vertIndxs.append(int(split_param[0]))
			
			if split_param[1] != "":
				self.txtrIndxs.append(int(split_param[1]))
			if split_param[2] != "":
				self.normIndxs.append(int(split_param[2]))
	def to_def(self):
		definition = ""
		
		for i in range(self.size):
			definition += "f "
			definition += str(self.vertIndxs[i])
			definition += "/"
			try:
				definition += str(self.txtrIndxs[i])
			except IndexError:
				pass
			definition += "/"
			try:
				definition += str(self.normIndxs[i])
			except IndexError:
				pass
		
		return definition	

class ObjModel:
	def __init__(self, filename):
		self.verts = []
		self.norms = []
		self.faces = []
		self.paramSVs = []
		self.txtrs = []
		
		lines = None
		
		#Read file
		with open(filename, "r") as f:
			lines = f.readlines()
		
		#Iterate through lines
		for ln in lines:
			splitln = ln.split()
			
			#If line is empty
			if not splitln:
				continue
			#If line is comment
			if splitln[0][0] == "#":
				continue
			#If line's arguments are three floats
			elif splitln[0] == "v" or splitln[0] == "vn" or splitln[0] == "vp":
				x = float(splitln[1])
				y = float(splitln[2])
				z = float(splitln[3])
				
				if splitln[0] == "v":
					self.verts.append(Point(x, y, z))
				elif splitln[0] == "vn":
					self.norms.append(Point(x, y, z))
				elif splitln[0] == "vp":
					self.paramSVs.append(Point(x, y, z))
			else:
				#Texture coordinate
				if splitln[0] == "vt":
					self.txtrs.append(UV(float(splitln[1]), float(splitln[2])))
				#Face
				elif splitln[0] == "f":
					self.faces.append(ObjFace(splitln[1:len(splitln)]))
				#Load material file
				elif splitln[0] == "mtllib":
					pass
				#Use material by name
				elif splitln[0] == "usemtl":
					pass
				#Object
				elif splitln[0] == "o":
					pass
				#Group
				elif splitln[0] == "g":
					pass
				#Smoothing group
				elif splitln[0] == "s":
					pass
				else:
					pass
	def export(self, filename):
		f = open(filename, "w")
		
		for v in self.verts:
			f.write("v %f %f %f\n" % (v.x, v.y, v.z))
		if self.norms:
			for n in self.norms:
				f.write("vn %f %f %f\n" % (n.x, n.y, n.z))
		if self.paramSVs:
			for p in self.paramSVs:
				f.write("vp %f %f %f\n" % (p.x, p.y, p.z))
		if self.faces:
			for face in self.faces:
				f.write(face.to_def() + "\n")
		f.close()
