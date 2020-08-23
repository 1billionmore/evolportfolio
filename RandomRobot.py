from Robot import Robot
class RandomRobot(Robot):

    def getMove(self, arr):
        n_rows = len(arr)
        n_cols = len(arr[0])
        l = []
        for i in range(n_rows):
            for j in range(n_cols):
                if arr[i][j] == None:
                    l.append((i, j))
        return random.choice(l)
