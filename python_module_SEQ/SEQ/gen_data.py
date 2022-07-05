import random
import os
def gendata(n,m,stp,tm,seedx,testep):
    random.seed(seedx)
    file=open("seq"+tm+'/data/'+str(testep)+".csv","w")#qqqqqqqqqqqqqq
    ansf=open('seq'+tm+'/correct_ans.csv',"a")
    file.write(str(n)+'\n')#qqqqqqqqqqqqqqqq
    traj=list()
    q=list()
    a=random.randint(1,500)
    b=random.randint(1,500)
    c=random.randint(1,500)
    for i in range(0,n):
        a=a+(random.random()-0.5)*stp
        b=b+(random.random()-0.5)*stp
        c=c+(random.random()-0.5)*stp
        file.write(str(a)+',')#QQQQQQQQQQQQ
        file.write(str(b)+',')#qqqqqqqqqqqqqq
        file.write(str(c)+'\n')#qqqqqqqqqqqq
        traj.append([a,b,c])

    file.write(str(m)+'\n')#qqqqqqqqqqqqqqqqqq
    st=random.randint(0,n-m-5)
    ansf.write(str(st)+','+str(st+m)+'\n')
    ansf.close()
    for i in range(st,st+m):
        a=traj[i][0]+(random.random()-0.5)*stp
        b=traj[i][1]+(random.random()-0.5)*stp
        c=traj[i][2]+(random.random()-0.5)*stp
        file.write(str(a)+',')#qqqqqqqqqqqqqqqqq
        file.write(str(b)+',')#qqqqqqqqqqqqqqqqq
        file.write(str(c)+'\n')#qqqqqqqqqqqqqqqqq
        q.append([a,b,c])
    file.close()#qqqqqqqqqqqqqq
    return [traj,q]
#gendata(1000,40)
