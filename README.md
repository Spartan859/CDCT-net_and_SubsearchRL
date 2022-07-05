# SubsearchRL

This is the code implementation of the thesis ***3D Tracking of Dynamic Objects with Co-training and Sub-trajectory Search with Deep Reinforcement Learning***

## Install the gym environment

1. Clone the repository

```bash
git clone https://github.com/Spartan859/SubsearchRL
cd SubsearchRL/python_module_SEQ
```

2. Install the environment
```bash
pip install -e .
```

## Train an agent
**train_ppo.py** is an example of training a PPO agent.
See python_module_SEQ/SEQ/sequence_mdp_v2.py for more details about environment arguments.

This implementation is based on stable-baselines3. See its doc for further usage.


