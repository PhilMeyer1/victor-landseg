import sys
from pathlib import Path
from PIL import Image
ns=sys.argv[2].split(","); ims=[Image.open(f"ansicht/naht_{n}.jpg") for n in ns]
W=max(i.width for i in ims); H=sum(i.height for i in ims)
g=Image.new("RGB",(W,H),"white"); y=0
for i in ims: g.paste(i,(0,y)); y+=i.height
if max(g.size)>2000:
    f=2000/max(g.size); g=g.resize((int(g.width*f),int(g.height*f)))
g.save(f"blatt_{sys.argv[1]}.jpg",quality=88)
