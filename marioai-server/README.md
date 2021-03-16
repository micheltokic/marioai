# MarioAI: Protobuf-Interface

This project allows interfacing the MarioAI engine with a python gym environment.
It is based on Google Protobuf messages to and from the engine.

Messages types include:
- Init (level initialization)
- Action (action to be performed by the agent on the environment)
- State (resulting state information after taking action)

## Message specifications
### Init
- Level difficulty (int32)
- Level seed (int32)
- Receptive field width (int32)
- Receptive field height (int32)
- Level length (int32)

### Action
- 
