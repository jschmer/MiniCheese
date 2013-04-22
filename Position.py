class Position(object):
    """description of class"""
    cols = "abcde"
    rows = "123456"

    # col, row
    # origin is left lower corner, starts with 1
    def __init__(self, x, y):
        if x not in range(1, 6) or y not in range(1, 7):
            raise ValueError

        self.x = x
        self.y = y

    def from_string(msg):
        if len(msg) > 2: raise ValueError
        if msg[0] not in Position.cols: raise ValueError
        if msg[1] not in Position.rows: raise ValueError

        x = Position.cols.index(msg[0])+1
        y = int(msg[1])
        return Position(x, y)

    def __str__(self):
        return Position.cols[self.x-1]+str(self.y)