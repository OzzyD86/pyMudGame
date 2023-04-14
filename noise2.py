from PIL import Image, ImageFilter
import math as maths
import random
#import os
#import json

def makeNoiseImage(sz, maxrand = 255):
	image = Image.new('RGB', (sz, sz))
	px = image.load()

	for x in range(0, sz):
		for y in range(0, sz):
			q = int(random.random() * maxrand)
			p = int(random.random() * maxrand)
			r = int(random.random() * maxrand)
			px[x,y] = (q,p,r)
	return image

class mapper():
	d = {0: {}}
	pass

class noiseMachine():
	noise = [] 

	def __init__(self):
		self.scope = []
		
	def buildNoiseBase(self, sz, maxrand = 255):
		x = makeNoiseImage(sz, maxrand)
		self.noise.append(x)
		return x

	def addScope(self, scope = [0, 1, 0]):
		self.scope.append(scope)
		return self

	def locBuild(self, pos = (0,0), size = 1):
		scope = self.scope.copy() # [[0, 5, 0], [1, 19, 2]]
		nn = []
		out = {}
		for i in self.scope:
			nn.append(buildNoiseProfile(self.noise[i[0]], pos, i[1], size, (0, 0)).load())
			
		for x in range(0, size):
			for y in range(0, size):
				o = 0
				i = scope.pop(0)
				o = float(nn[i[0]][x,y][i[2]])
				
				for i in scope:
					o = (o + float(nn[i[0]][x,y][i[2]])) / 2
				
				#o = (float(nn[1][x,y][0]) / 16) * (float(nn[2][x,y][1] / 16))
				#o += ((float(nn[3][x,y][0])) / 8) 
				#o += (float(nn[4][x,y][0]) - 64) / (8) 
				#o += float(nn[0][x,y][1] * 2) - 8
				#o = int(o / 2) + 32
				out[x,y] = o
				
		return out
		
	def imgBuild(self, pos, size, opo = False):
		nn = []
		
		a = self.noise[0]
		b = self.noise[1]
		c = self.noise[3]
		z = buildNoiseProfile(b, pos, 1024, size, (129, 8))
		nn.append(buildNoiseProfile(c, pos, 4, size, (48,48)).load())
		nn.append(buildNoiseProfile(a, pos, 1023, size, (48, 48)).load())
		nn.append(buildNoiseProfile(a, pos, 257, size, (80, 80), (4096, 4096)).load())
		nn.append(buildNoiseProfile(b, pos, 64, size, (32, 32)).load())
		nn.append(buildNoiseProfile(b, pos, 32, size).load())
		# locbuild does up to here
		
		img = Image.new('RGB', (size, size))
		a1 = img.load()
		a4 = z.load()
		mh = 0
		lh = 255
		tr = Image.open('assets/cloop2.png')
		tr2 = tr.load()
	#	print("Compiling...")
		for x in range(0,size):
			for y in range(0,size):
				o = (float(nn[1][x,y][0]) / 16) * (float(nn[2][x,y][1] / 16))
				o += ((float(nn[3][x,y][0])) / 8) 
				o += (float(nn[4][x,y][0]) - 64) / (8) 
				o += float(nn[0][x,y][1] * 2) - 8
				o = int(o / 2) + 32
	#			mh = max(mh, o)
	#			lh = min(lh, o)
				if (o > 255):
					o = 255
				elif(o <0):
					o = 0

				if (opo == False):
					a1[x,y] = tr2[o,a4[x,y][1]]
				else:
					a1[x,y] = (o, a4[x,y][1],0)
					if (o > 64 and a1[x,y][1] > 32):
						a1[x,y] = (a1[x,y][0], a1[x,y][1], a1[x,y][2] + 128)
		return img

#	def buildNoise(self, a, coords = (0,0), sc = 4, size = 16, offset = (0, 0)):
#		self.noise.append(buildNoiseProfile(a, coords, sc, size, offset))
#		return self

    
def buildNoiseProfile(a, coords = (0,0), sc = 4, size = 16, offset = (0, 0), coffset = (0, 0)):

	#sc = 64
	img = Image.new('RGB', (size, size))
	opx = img.load()
	apx = a.load()
	coords = (coords[0]+coffset[0], coords[1]+coffset[1])
	for x in range(0, size):

		xt = (offset[0] + maths.floor((coords[0]+x) / sc)) % a.size[0]
		xtp = (xt + 1) % a.size[0]
		xp = ((coords[0]+x) % sc)

		for y in range(0, size):
			yt = (offset[1] + maths.floor((coords[1]+y) / sc)) % a.size[1]
			ytp = (yt + 1) % a.size[1]
	
			yp = ((coords[1]+y) % sc)
			op = [0] * 3
			for ch in range(0, 3):
				xr1 = float(apx[xt,yt][ch])
				xr2 = float(apx[xtp,yt][ch])

				xd = xr2 - xr1

				tmp = xd / sc * xp
				xm1 = xr1 + tmp
		
				xr1r = float(apx[xt,ytp][ch])
				xr2r = float(apx[xtp,ytp][ch])
				xdr = xr2r - xr1r
				tmpr = xdr / sc * xp
				xm2 = xr1r + tmpr
		
				xmd = xm2 - xm1
				o = xm1 + (xmd / sc * yp)
				op[ch] = int(o)

			opx[x,y] = (op[0],op[1],op[2])
	return img    

def buildMap(pos = (0, 0), size = 100, opo = False):
	return imgBuild(pos, size, opo)
