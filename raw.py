from p3dfi import Point
import re

class RawFace:
	def __init__(self, vertexIndices):
		self.vertIndxs = []
		self.size = len(vertexIndices)
		for i in vertexIndices:
			self.vertIndxs.append(i)

class RawModel:
	def __init__(self, filename):
		self.verts = []
		self.faces = []
		
		lines = None
			
		with open(filename, "r") as f:
			lines = f.readlines()
		
		for ln in lines:
			ptrn = re.compile(r"((\-?\d+(\.?\d)?\d*( |\t)+){2}(\-?\d+(\.?\d)?\d*))")
			ptsInLine = []
			vertIndxs = []
			
			for match in re.findall(ptrn, ln):
				xyz = match[0].split()
				ptsInLine.append(Point(float(xyz[0]), float(xyz[1]), float(xyz[2])))
			for p in ptsInLine:
				ptIsDup = False
				for v in self.verts:
					if p == v:
						vertIndxs.append(self.verts.index(v))
						ptIsDup = True
						break
				if not ptIsDup:
					self.verts.append(p)
					vertIndxs.append(self.verts.index(p))
			self.faces.append(RawFace(vertIndxs))
	def export(self, filename):
		f = open(filename, "w")
		
		for face in self.faces:
			for i in face.vertIndxs:
				v = self.verts[i]
				f.write("%f %f %f " % (v.x, v.y, v.z))
			f.write("\n")
		f.close()
