zerorange = [(2060379, 2060501), (2060403, 2060501), (2060436, 2060501), (2060476, 2060501), (2060525, 2060583), (2060568, 2060583), (2060649, 2060730), (2060678, 2060730), (2060718, 2060730), (2060803, 2060838), (2060828, 2060838), (2060922, 2060998), (2060948, 2060998), (2060988, 2060998), (2061130, 2061199), (2061161, 2061199), (2061178, 2061199), (2061192, 2061199), (2061264, 2061271), (2061303, 2061342)]
tmpzerorange = []
threshold = 20
i ,overlap = 0,0
while 1:
	flag = 0
	if zerorange[i+1][0] - zerorange[i][1]<threshold:
                tmpzerorange.append((zerorange[i][0],zerorange[i+1][1]))
                overlap,flag = 1,1
		i += 1
        else:
                tmpzerorange.append(zerorange[i])
        i += 1
        if i == len(zerorange) - 1:
                if flag == 0:
                        tmpzerorange.append(zerorange[i])
                i = 0
                zerorange = tmpzerorange
                tmpzerorange = []
                if overlap == 0:
                        break
                else:
                        overlap = 0
                        print zerorange

