from Robot import Robot
class PlayerRobot(Robot):

    def getMove(self, arr):

        move = int(input("Give me a move"))
        col = move % 3
        row = math.floor(move / 3)
        return row,  col
