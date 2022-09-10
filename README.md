# SubsearchRL

This is the code implementation of the thesis ***Co-Training Based 3D Animal Pose Estimation and Reinforcement Learning Based Sub-trajectory Search***

## Install the gym environment

1. Clone the repository

```bash
git clone https://github.com/Spartan859/CDCT-net_and_SubsearchRL
cd CDCT-net_and_SubsearchRL/python_module_SEQ
```

2. Install the environment
```bash
pip install -e .
```

## Train an agent
**train_ppo.py** is an example of training a PPO agent.
See python_module_SEQ/SEQ/sequence_mdp_v2.py for more details about environment arguments.

This implementation is based on stable-baselines3. See its doc for further usage.

## Pretrained weights
The pretrained weights are available in the repository in the "weights" folder.
They are trained on trajectory dataset randomly generated, and should work well on any trajectory dataset given by user.

## Environment arguments
The information in brackets is (Type,Default value)
```python
div #The calculated difference measure will be divided by this number. (Float,1)
#If you are using the pretrained weights, try tuning it until the difference measure is in the interval of (10,100).

obsz #The observed zone of the difference measure. Difference value above this number won't be taken into account. (Integer,300)

skip #Whether to enable "skip". If set to True, the agent will skip $delta nodes after each action. (Boolean,False)

delta #If $skip==enabled, the agent will skip $delta nodes after each action. (Integer,4)

dt_hs #The variable used to judge the agent and tell whether it has "cut" the sequence too soon. See the paper for further details (Integer,5)

Rk #Used to adjust the scale of the punishment. The bigger it is, the harder the agent will be punished for early "cut". (Float,0.1)

sim_tp #The comparison method. Two types available, namely Frechet and DTW. More can be added manually. (String,"Frechet")

testseed #The seed of random trajectory generation.(Integer,123)

len #The length of data trajectory

qlen #The length of query trajectory
```

## Use the agent to solve sub-trajectory search problems
1. Rewrite gen_data.py to load your own data instead of random ones.
2. See test_ppo.py for an example of using the agent.

## Output
The environment will automatically output the most similar sub-trajectory to the query trajectory to the folder whose name is seq+start_time.

The answer.csv contains the following information:
(l,r,dif,reward)

l,r: the left and right index of the sub-trajectory in the data trajectory.

dif: the difference measure between the sub-trajectory and query trajectory.

reward: the reward got by the agent.

By default, dif+reward+punishment=obsz.
"punishment" represents the punishment for early "cut".

If you are training and wants to get the input data, the default gen_data.py will write all of the generated trajectories and the accurate answer to "data" folder and "correct_ans.csv".




