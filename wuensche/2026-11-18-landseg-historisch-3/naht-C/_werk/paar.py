import sys
from PIL import Image
a,b,z=sys.argv[1:4]
A=Image.open(f"streifen/{a}.jpg"); B=Image.open(f"streifen/{b}.jpg")
W=max(A.width,B.width); g=Image.new("RGB",(W,A.height+B.height+10),"white"); g.paste(A,(0,0)); g.paste(B,(0,A.height+10))
if max(g.size)>2000:
    f=2000/max(g.size); g=g.resize((int(g.width*f),int(g.height*f)))
g.save(f"paar_{z}.jpg",quality=88)
