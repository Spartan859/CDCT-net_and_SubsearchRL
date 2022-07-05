import sys
import os
import logging
import random
import gym
import math
import time
import numpy as np
from SEQ.gen_data import gendata
from gym import spaces
#Copyright: Xiangyu Li , Spartan117(github: dijkstra0x3)
logger = logging.getLogger(__name__)
INF=1e9
class SeqEnv1(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self,div=1,obsz=300,skip=False,delta=4,dt_hs=5,Rk=0.1,sim_tp="Frechet",testseed=123,len=1000,qlen=40):
        self.div=div #The calculated difference measure will be divided by this number. (Float)
        self.obsz=obsz #The observed zone of the difference measure. Difference value above this number won't be taken into account. (Integer) 
        self.skip=skip #Whether to enable "skip". If set to True, the agent will skip $delta nodes after each action. (Boolean)
        self.delta=delta #If $skip==enabled, the agent will skip $delta nodes after each action. (Integer)
        self.dt_hs=dt_hs #The variable used to judge the agent and tell whether it has "cut" the sequence too soon. See the paper for further details (Integer)
        self.Rk=Rk #Used to adjust the scale of the punishment. The bigger it is, the harder the agent will be punished. (Float)
        self.sim_tp=sim_tp #The comparison method. Two types available, namely Frechet and DTW. More can be added. (String)
        self.testseed=testseed #The seed of random trajectory generation.(Integer)

        self.len=len #The length of data trajectory
        self.qlen=qlen #The length of query trajectory

        if os.path.exists('seq'+self.tm)==0:
            os.mkdir('seq'+self.tm)
            os.mkdir('seq'+self.tm+'/data/')
        open(r'seq'+self.tm+'/correct_ans.csv','w')
        self.viewer=None
        self.itx=0
        self.filest=open(r'seq'+self.tm+'/answer.csv','w')
        self.filest.close()
        self.observation_space=spaces.Box(low=np.array([0,0,0,-100],dtype=np.float32),high=np.array([self.obsz,self.obsz,self.obsz,100],dtype=np.float32))
        self.action_space=spaces.Discrete(2)

    totalr=0 # the total punishment.
    testing=1
    testepoch=0
    
    #for new traj similarity measures.
    
    #sim_tp="DTW"
    #
    tm=time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    
    def geninput(self,seedx,testep): # the function to write data into the sequence.
        print("GEN!!?")
        self.n=self.len # The length of the data trajectory
        self.m=self.qlen # The length of the query trajectory
        self.traj,self.q=gendata(self.n,self.m,20,self.tm,seedx,testep)

    def sml_pre(self,l,r):
        if self.sim_tp=="DTW":
            if l!=self.nowl:
                self.nowl=l
                self.nowr=l
                self.dp.fill(0)
                #for i in range(0,self.m+1):
                #   self.dp[(l&1)^1,i]=INF
            if r<self.nowr :
                return self.sve[r]
            for i in range(self.nowr,r+1):
                #self.dp[i&1,0]=INF
                for j in range(1,self.m+1):
                    if j==1:
                        self.dp[i&1,j]=self.dist(i,j)+self.dp[(i&1)^1,j]
                    elif i==self.nowl:
                        self.dp[i&1,j]=self.dist(i,j)+self.dp[i&1,j-1]
                    else:
                        self.dp[i&1,j]=self.dist(i,j)+min(self.dp[(i&1)^1,j],self.dp[(i&1)^1,j-1],self.dp[i&1,j-1])
                self.sve[i]=min(self.dp[r&1,self.m]/self.div,self.obsz)
            self.nowr=r+1
            return min(self.dp[r&1,self.m]/self.div,self.obsz)
        
        if self.sim_tp=="Frechet":
            if l!=self.nowl:
                self.nowl=l
                self.nowr=l
                self.dp.fill(0)
                #for i in range(0,self.m+1):
                #   self.dp[(l&1)^1,i]=INF
            if r<self.nowr :
                return self.sve[r]
            for i in range(self.nowr,r+1):
                #self.dp[i&1,0]=INF
                for j in range(1,self.m+1):
                    if j==1:
                        self.dp[i&1,j]=max(self.dist(i,j),self.dp[(i&1)^1,j])
                    elif i==self.nowl:
                        self.dp[i&1,j]=max(self.dist(i,j),self.dp[i&1,j-1])
                    else:
                        self.dp[i&1,j]=max(self.dist(i,j),min(self.dp[(i&1)^1,j],self.dp[(i&1)^1,j-1],self.dp[i&1,j-1]) )
                
                self.sve[i]=min(self.dp[r&1,self.m]/self.div,self.obsz)
            
            self.nowr=r+1
            return min(self.dp[r&1,self.m]/self.div,self.obsz)
        
        print("No matching similarity measure")
        exit()
      
    def reinit(self):
        self.pt=0
        self.lp=1
        self.nowl=0
        self.nowr=0
        self.bl=0
        self.br=0
        self.gamma=0.8
        self.dp=np.zeros((2,self.m+1))
        self.sufsim=np.zeros((self.n+5,2))
        self.sve=np.zeros(self.n+5)

        if self.sim_tp=="DTW":

            for j in range(self.m,0,-1):
                for i in range(self.n,0,-1):
                    if i==self.n:
                        self.sufsim[i,j&1]=self.dist(i,j)+self.sufsim[i,(j&1)^1]
                    elif j==self.m:
                        self.sufsim[i,j&1]=self.dist(i,j)+self.sufsim[i+1,j&1]
                    else:
                        self.sufsim[i,j&1]=self.dist(i,j)+min(self.sufsim[i,(j&1)^1],self.sufsim[i+1,j&1],self.sufsim[i+1,(j&1)^1])
            self.state=np.array([self.obsz,self.sml_pre(1,1),min(self.sufsim[1,1]/self.div,self.obsz),0],dtype=np.float32)
        
        if self.sim_tp=="Frechet":
            for j in range(self.m,0,-1):
                for i in range(self.n,0,-1):
                    if i==self.n:
                        self.sufsim[i,j&1]=max(self.dist(i,j),self.sufsim[i,(j&1)^1])
                    elif j==self.m:
                        self.sufsim[i,j&1]=max(self.dist(i,j),self.sufsim[i+1,j&1])
                    else:
                        self.sufsim[i,j&1]=max(self.dist(i,j),min(self.sufsim[i,(j&1)^1],self.sufsim[i+1,j&1],self.sufsim[i+1,(j&1)^1]) )
            self.state=np.array([self.obsz,self.sml_pre(1,1),min(self.sufsim[1,1]/self.div,self.obsz),0],dtype=np.float32)

    def dist(self,a,b):
        rt=0
        for i in range(0,3):
            rt+=(self.traj[a-1][i]-self.q[b-1][i])*(self.traj[a-1][i]-self.q[b-1][i])
        return math.sqrt(rt)
    
    def _seed(self, seed=None):
        self.np_random, seed = random.seeding.np_random(seed)
        return [seed]

    def getGamma(self):
        return self.gamma

    def getStates(self):
        return self.states

    def getAction(self):
        return self.actions
    
    def step(self, action):
        r=0.0
        self.pt=self.pt+1
        prebest=self.state[0]
        if self.state[1]<self.state[0]:
            self.state[0]=self.state[1]
            self.bl=self.lp
            self.br=self.pt
        if self.state[2]<self.state[0]:
            self.state[0]=self.state[2]
            self.bl=self.pt
            self.br=self.n
        r=prebest-self.state[0]
        if action==1:
            self.lp=self.pt+1
            if self.state[3]>0:
                r-=self.state[3]*self.Rk
        self.totalr+=r
        isterminated=False
        if self.pt>=self.n:
            isterminated=True
            self.filest=open(r'seq'+self.tm+'/answer.csv','a')
            self.filest.write(str(self.bl)+','+str(self.br)+','+str(self.state[0])+','+str(self.totalr)+'\n')
            self.filest.close()
            print(self.totalr)
            print(str(self.bl)+' '+str(self.br)+' '+str(self.state[0])+'\n')
            return self.state,float(r),isterminated,{}
        
        self.state[1]=self.sml_pre(self.lp,self.pt+1)
        self.state[2]=min(self.sufsim[self.pt+1,1]/self.div,self.obsz)
        if self.pt<=self.n-10:
            self.state[3]=min(self.sml_pre(self.lp,self.pt+1)-self.sml_pre(self.lp,self.pt+1+self.dt_hs),100)
            self.state[3]=max(self.state[3],-100)
            #self.state[3]=0
        else:
            self.state[3]=0
        if self.skip:
            self.pt=self.pt+self.delta
        return self.state,float(r),isterminated,{}

    def reset(self):
        self.testepoch+=1
        if self.testing!=1:
            self.geninput(random.randint(),self.testepoch)
        else:
            self.geninput(self.testepoch*self.testseed%(1000000007),self.testepoch)
        self.reinit()
        self.totalr=0
        print("reset!!!")
        return self.state

    def render(self, mode='human'):
        return None
        # Do nothing

    def close(self):
        if self.viewer:
            self.viewer.close()
