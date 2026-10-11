from PIL import Image,ImageDraw,ImageFont
for size in (192,512):
 im=Image.new('RGB',(size,size),'#4549c6');d=ImageDraw.Draw(im)
 f=ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf',int(size*.72));bb=d.textbbox((0,0),'G',font=f);d.text(((size-(bb[2]-bb[0]))/2-bb[0],(size-(bb[3]-bb[1]))/2-bb[1]),'G',font=f,fill='white');im.save(f'assets/icon-{size}.png')
