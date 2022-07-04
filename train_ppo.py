import SEQ
import gym
import os
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy

env=gym.make('sequence_mdp-v2',div=1,len=1000,qlen=40) # see python_module_SEQ/SEQ/sequence_mdp_v2.py for variable list

name="PPO_seq_v2_c10"
len=1000
qlen=40
train_ep=1000


#'''
if os.path.exists(name+'.zip'):
    model=PPO.load(name,env=env,verbose=0)
    print("Load from" +name+ ".zip")
else:
    model=PPO('MlpPolicy',env)
    print("New Start as "+name)

model.learn(train_ep*len)
model.save(name)
#'''

