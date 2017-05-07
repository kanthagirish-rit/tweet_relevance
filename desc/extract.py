file = open( "crawledHandlesw:Desc26.txt", "r" )
list_ = []


for line in file:
    val = line.split('\n')
    list_.append(val)
    
for i in range(len(list_)):
    f = open('file'+str(i)+'.txt','w')
    f.write(str(list_[i]))
    f.close()


print list_[20]
