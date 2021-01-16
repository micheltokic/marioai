package de.lmu.parl;

import de.lmu.parl.proto.MarioProtos;

import java.util.HashMap;
import java.util.Map;

public class ActionMap {
    static Map<MarioProtos.Action, boolean[]> actionMap = new HashMap<MarioProtos.Action, boolean[]>();
    static {
        //        KEY_LEFT = 0;
        //        KEY_RIGHT = 1;
        //        KEY_DOWN = 2;
        //        KEY_JUMP = 3;
        //        KEY_SPEED = 4;
        //        KEY_UP = 5;

        actionMap.put(MarioProtos.Action.DOWN, new boolean[]{false, false, true, false, false, false});
        actionMap.put(MarioProtos.Action.JUMP, new boolean[]{false, false, false, true, false, false});

        actionMap.put(MarioProtos.Action.SPEED_JUMP, new boolean[]{false, false, false, true, true, false});
        actionMap.put(MarioProtos.Action.SPEED_RIGHT, new boolean[]{false, true, false, false, true, false});
        actionMap.put(MarioProtos.Action.SPEED_LEFT, new boolean[]{true, false, false, false, true, false});

        actionMap.put(MarioProtos.Action.JUMP_RIGHT, new boolean[]{false, true, false, true, false, false});
        actionMap.put(MarioProtos.Action.JUMP_LEFT, new boolean[]{true, false, false, true, false, false});
        actionMap.put(MarioProtos.Action.SPEED_JUMP_RIGHT, new boolean[]{false, true, false, true, true, false});
        actionMap.put(MarioProtos.Action.SPEED_JUMP_LEFT, new boolean[]{true, false, false, true, true, false});
    }
}
