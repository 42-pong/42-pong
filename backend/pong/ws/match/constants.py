from ..share import constants as ws_constants


class Stage(ws_constants.BaseEnum):
    INIT = "INIT"
    READY = "READY"
    PLAY = "PLAY"
    END = "END"


class Mode(ws_constants.BaseEnum):
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"


class Team(ws_constants.BaseEnum):
    ONE = "1"
    TWO = "2"
    EMPTY = ""


class Move(ws_constants.BaseEnum):
    UP = "UP"
    DOWN = "DOWN"
