from PIL import Image, ImageDraw, ImageFont
import math as maths

font = ImageFont.truetype("game/core/arial.ttf", 12)	

def doTime(time = 0): # Taken from somewhere else - main.py apparently
	out = ""
	mo = (time // (1440 * 28)) 
	out += str(mo + 1) + "mo, "

	w = (time // (1440 * 7)) % 4
	out += str(w + 1) + "w, "

	d = (time // 1440) % 7
	out += str(d + 1) + "d, "

	#if (time >= 60):
	h = (time // 60) % 24
	out += str(h) + "h, "

	m = time % 60
	out += str(m) + "m"
	return out
	
def moonph(num):
  e = num
  print(e)
  a = maths.radians(e)
  b = abs(maths.sin(a) * 7.5)
  print(b)
  x = Image.new("RGBA", (25,25), (0,0,0,0))
  y = ImageDraw.Draw(x)
  if (e<180):
    y.ellipse((1,1,23,23), fill=(0,0,0))
    y.chord((1,1,23,23), start=90, end=270, fill=(255,255,255))
  else:
    y.ellipse((1,1,23,23), fill=(255,255,255))
    y.chord((1,1,23,23), start=90, end=270, fill=(0,0,0))
    
  if (e > 90 and e <= 270):
    c=(255,255,255,255)
  else:
    c=(0,0,0)
  if (b< 13):
    y.ellipse((1+b,1,23-b,23), fill=c)
  return x
  
#z = Image.new("RGB", (25*6,25*6))
#for j in range(6):
# for i in range(6):
#    z.paste(moonph(((j * 6) + i) *10), (25*i,25*j))
#z.save("mn16.png")
  
#moonph(4/12).save("mph.png")

bgs = {
	0: (16, 16, 63),
	(4*60): (16,16,63),
	(6*60): (127, 255, 192),
	(9*60): (255, 255, 192),
	(13*60): (192, 255, 255),
	(18*60): (192, 127, 192),
	(22*60): (16, 16, 63),
	(24*60): (16, 16, 63)
}

def mkColour(colours, time = 0):
	under = None
	above = None
	
	if (time in colours):
		return colours[time]
	
	for i,j in colours.items():
		if (i <= time):
			if (under is None or under < i):
				under = i
		elif (i > time):
			if (above is None or above > i):
				above = i
				
	p = (time - under) / (above - under)
#	print(time, under, above, p)
	
	out = []
	for i in range(0, 3):
		out.append(int(colours[under][i] + ((colours[above][i]-colours[under][i]) * p)))
	
#	print(tuple(out))
	return tuple(out)

def day(time):

	
	t = time % 1440
	ph = (time % (27.1 * 1400)) / (27.1 * 1400) * 360
	print(ph)
	
	h = maths.cos(maths.radians(t/144*36))
	w = maths.sin(maths.radians(t/144*36))
	
		

	img = Image.new("RGB", (200,200))
	d = ImageDraw.Draw(img)
	
	bgc = mkColour(bgs, t)
	d.rectangle((0,0,199,199), outline=(255,255,255))
	d.rectangle((2,2,197,197), fill=bgc)
	F = moonph(ph)
	img.paste(F, (int(100+(150*w)-13),int(200+(150*-h)-13)), F)

#	for i in range(0, 200-4):
#		d.line((2+i, 2, 2+i, 18), fill=mkColour(bgs, i/196*1440))
		
	d.ellipse((int(100+(100*-w)-13), int(200+(100*h)-13), int(100+(100*-w)+13), int(200+(100*h)+13)), fill=(255,255,0))

	for i in range(12):
		p = maths.cos(maths.radians(i * 30))
		q = maths.sin(maths.radians(i * 30))
		
		d.ellipse((int(100+(q*70)-3),int(100+(-p*70)-3),int(100+(q*70)+3),int(100+(-p*70)+3)), outline=(0,0,0), fill=mkColour(bgs, ((i)%12)/12*1440))

	p = maths.cos(maths.radians(((time / 1) % 60) * 6))
	q = maths.sin(maths.radians(((time / 1) % 60) * 6))
	h = maths.cos(maths.radians(((time / 60) % 12) * 30))
	w = maths.sin(maths.radians(((time / 60) % 12) * 30))

	d.line((100,100,100+(40*w),100+(40*-h)), width=5, fill=(255,0,0))
	d.line((100,100,100+(60*q),100+(60*-p)), fill=(255,127,127))
	d.text((4, 4), doTime(time), (255,255,255), font) 
	return img
	
#day(0).save("0.png")
#day(720).save("720.png")
#n = 1403+1439+93897+1

#day(int(n)).save(str(n) + ".png")