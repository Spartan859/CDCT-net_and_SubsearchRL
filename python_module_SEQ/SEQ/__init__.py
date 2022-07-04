from gym.envs.registration import register

register(
    id='sequence_mdp-v0',                                   # Format should be xxx-v0, xxx-v1....
    entry_point='SEQ.sequence_mdp_v0:SeqEnv1',              # Expalined in envs/__init__.py
)

register(
    id='sequence_mdp-v1',                                   # Format should be xxx-v0, xxx-v1....
    entry_point='SEQ.sequence_mdp_v1:SeqEnv1',              # Expalined in envs/__init__.py
)

register(
    id='sequence_mdp-v2',                                   # Format should be xxx-v0, xxx-v1....
    entry_point='SEQ.sequence_mdp_v2:SeqEnv1',              # Expalined in envs/__init__.py
)