import json, subprocess, sys
P=sys.executable
def linie(args):
    out=subprocess.run([P,"-B","blob.py",*args],capture_output=True,text=True).stdout
    return json.loads(out)["linie"]
schritte=[
 {"op":"teilen","id":100075,"linie":linie(["100075","gt","145","tmp/s75.jpg","-","1","1"])},
 {"op":"teilen","id":100093,"linie":linie(["100093","gt","120","tmp/s93.jpg","-","1","1"])},
 {"op":"teilen","id":100099,"linie":linie(["100099","gt","110","tmp/s99.jpg","-","1","1"])},
 {"op":"teilen","id":100064,"linie":linie(["100064","gt","165","tmp/s64.jpg","-","1","1"])},
 {"op":"verschmelzen","ids":[100047,100052,100057,100058,100067,100068,100074],"ziel":100047},
]
json.dump({"schritte":schritte},open("eingriffe.json","w",encoding="utf-8"))
print(len(schritte))
