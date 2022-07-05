from cgi import test
import SEQ
import gym
import os
from stable_baselines3 import PPO
#Critical: you'll need to rewrite gen_data.py yourself to load your own data instead of random ones.
len=10000
qlen=40
env=gym.make('sequence_mdp-v2',div=1,len=len,qlen=qlen,Rk=0.1)
#set len and qlen to the length of the data trajectory and query trajectory

name="PPO_seq_v2_c10"
test_pair_num=10 # number of test pairs


if os.path.exists(name+'.zip'):
    model=PPO.load(name,env=env)
    print("Load from" +name+ ".zip")
else:
    print(name+".zip does not exist")

for ep in range(test_pair_num):
    obs=env.reset()
    for i in range(len+5):
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        if dones:
            break
