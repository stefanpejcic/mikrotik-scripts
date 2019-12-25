# -*- coding: utf-8 -*-
import csv

flines = []
cad = ''
n = 1
with open('firewall.rsc') as fp:
    for line in fp:
        if line.endswith('\\\n'):
            cad += line[:len(line) - 2].strip() + ' '
        else:
            cad += line[:len(line) - 1].strip()
            cad = cad.replace('= ', '=')
            # print cad
            if cad.startswith('#'):
                print "{} ERROR: {}".format(n, cad)
            else:
                flines.append(cad)
            cad = ''
        n += 1

rules = []
n = 1
in_quoted_str = False
for l in flines:
    l = l.split(' ')
    print "{} Analitzant {}".format(n, l)
    n += 1
    cad = ''
    in_quoted_str = False
    tokens = []  
    for t in l:
        if (('"' in t) and (not t.endswith('"'))):
            in_quoted_str = True
            cad += t
        elif t.endswith('"'):
            in_quoted_str = False
            cad += t
            print "\t{}".format(cad)
            cad = ''
        elif (not '"' in t) and (in_quoted_str):
            cad += t + ' '
        elif (not '"' in t) and (not in_quoted_str):
            if t.endswith('='):
                cad += t
            else:
                cad = t
                print "\t{}".format(cad)
                tokens.append(cad)
                cad = ''

    rules.append([n, l, tokens])
    n += 1

labels = {}
for r in rules:
    for t in r[2]:  # for each property
        if '=' in t:
            g = t.split('=')
            labels[g[0]] = 1

print "Labels -----"
labels = labels.keys()
labels.insert(0, 'rule')
for l in labels:
    print l

with open('firewall-rules.csv', 'wb') as csvfile:
    w = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    w.writerow(labels)

    for r in rules:
        line = []
        for l in labels:
            line.append('')
        line[0] = r[0]
        for t in r[2]:
            if '=' in t:
                g = t.split('=')
                line[labels.index(g[0])] = g[1]
        w.writerow(line)
