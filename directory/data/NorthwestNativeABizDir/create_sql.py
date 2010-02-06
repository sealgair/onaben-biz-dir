#! /usr/bin/python
from datetime import datetime
schema = "columnheadings_new.txt"

strcomma = "<<comma innna string!!!>>"

for line in file(schema):
    if (line.strip() == ""):
        continue
    tbl, incols = line.lower().split(':', 1)
    print('')
    incols = incols.split(',')
    for entry in file(tbl+".txt"):
        nentry = ""
        instr = False
        for c in entry:
            if c == '"':
                instr = not instr
            if instr and c == ",":
                nentry += strcomma
            else:
                nentry += c
        vals = nentry.split(",")
        
        z = zip(incols,vals)
        cols = []
        vals = []
        for c,v in z:
            c = c.strip()
            v = v.replace(strcomma, ",").strip().replace("'","''").replace('"',"'")
            if c == "null": #or v == "":
                continue
            if v == "": v = "''"
            cols.append(c)
            if v[0] != "'" and '/' in v: #it's a date
                v = datetime.strptime(v, '%m/%d/%Y %H:%M:%S')
                v = v.strftime("'%Y%m%d'")
            vals.append(v)
            #print c,v
    
        print("INSERT INTO {tbl}\n\t({cols})\n\tVALUES\n\t({vals});".format(tbl=tbl, cols=','.join(cols), vals=','.join(vals)))
      
