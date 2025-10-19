from enum import Enum

class RecapState(Enum):
    INIT = 0
    # LEAF_UP = 1
    # LEAF_JUDGE_DONE = 2
    # LEAF_UP_FAIL = 3
    # NONLEAF_UP = 4
    # NONLEAF_JUDGE_DONE = 5
    DOWN = 6

    ACTION_TAKEN = 7
    UP = 8
