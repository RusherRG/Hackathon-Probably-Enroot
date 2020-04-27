populations = [54265,73470,84799,95811,126222,131714,130955,143690,143465,134251,125651,117766,115382,112796,107990,99974,98079,94483,86356,81551,61546,62206,56715,48514,44109,30148,20168]
'''
n_trains = [35 for i in range(len(populations))]

for i in range(len(populations)):
    if populations[i]//35 <= 4000:
        n_trains[i] = populations[i]//4000
print(n_trains)
'''
n_trains = []
while len(populations)!=0:
    p = []
    for i in range(len(populations)):
        populations[i] -= 2000
        if populations[i] >= 0:
            p.append(i)
    if len(p)>=2:
        n_trains.append([p[0],p[-1]])
    n = len(populations)
    for i in range(n):
        if i not in p:
            populations.pop(i-1)
print(n_trains,len(n_trains))
'''
for i in html:
    try:
        i.select("tr")
        x = i.select("td")
        type = x[1]
        type = type.text
        s = x[3].text
        e = x[4].text
        bt = x[5].text
        dat = [s,e,bt,type]
        tab.append(dat)
    except:
        continue
'''