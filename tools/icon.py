from PIL import Image, ImageDraw, ImageFilter
S=720
bg=Image.new("RGBA",(S,S),(199,54,43,255))
d=ImageDraw.Draw(bg)
for y in range(S):  # soft vertical gradient
    t=y/S; d.line([(0,y),(S,y)],fill=(int(214-30*t),int(64-20*t),int(50-14*t),255))
card=Image.new("RGBA",(S,S),(0,0,0,0)); c=ImageDraw.Draw(card)
x0,y0,x1,y1=150,190,570,520
sh=Image.new("RGBA",(S,S),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([x0+10,y0+22,x1+10,y1+22],28,fill=(60,10,8,120))
sh=sh.filter(ImageFilter.GaussianBlur(18))
c.rounded_rectangle([x0,y0,x1,y1],28,fill=(255,253,249,255))
c.rectangle([x0,y0+92,x1,y0+102],fill=(210,59,48,255))
for k in range(4):
    yy=y0+150+k*52; c.rectangle([x0+40,yy,x1-40 if k<3 else x0+260,yy+8],fill=(150,178,226,255))
c.rounded_rectangle([x0+40,y0+38,x0+250,y0+66],14,fill=(34,32,30,255))
card=card.rotate(-6,resample=Image.BICUBIC,center=(S/2,S/2)); sh=sh.rotate(-6,resample=Image.BICUBIC,center=(S/2,S/2))
img=Image.alpha_composite(Image.alpha_composite(bg,sh),card).convert("RGB")
import sys; out=sys.argv[1]
img.resize((180,180),Image.LANCZOS).save(f"{out}/apple-touch-icon.png")
img.resize((64,64),Image.LANCZOS).save(f"{out}/favicon.png")
img.resize((360,360),Image.LANCZOS).save("/home/claude/site-build/icon-preview.png")
