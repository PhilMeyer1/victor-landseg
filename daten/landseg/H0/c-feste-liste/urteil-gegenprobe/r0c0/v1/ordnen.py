import re,sys
t=open("urteile.py",encoding="utf-8").read()
start=t.index(" (100088,"); end=t.index(" (100249,")
block=t[start:end]; t=t[:start]+t[end:]
pos=t.index(" (100004,")
t=t[:pos]+block+t[pos:]
open("urteile.py","w",encoding="utf-8").write(t)
