import numpy as np
BLANK = -1
START = 0
WALL = 1
END = 2
GAMMA = 0.75
ALPHA = 0.9


class Runner:
    def __init__(self, maze, size):
        self.maze = maze
        self.map = [[0 for _ in range(size * size)] for _ in range(size * size)]
        self.actions = [0 for _ in range(size * size)]
        self.size = size
        self.start = 0
        self.end = 0
        self.playable = []

    def findVal(self, x, y):
        if self.maze[x][y] == WALL:
            return
        elif self.maze[x][y] == START:
            self.start = x * self.size + y
        elif self.maze[x][y] == END:
            self.end = x * self.size + y

        if x > 0:
            if self.maze[x - 1][y] != WALL:
                self.map[x * self.size + y][(x - 1) * self.size + y] = 1
                self.actions[x * self.size + y] += 1
        if x < self.size - 1:
            if self.maze[x + 1][y] != WALL:
                self.map[x * self.size + y][(x + 1) * self.size + y] = 1
                self.actions[x * self.size + y] += 1
        if y > 0:
            if self.maze[x][y - 1] != WALL:
                self.map[x * self.size + y][x * self.size + y - 1] = 1
                self.actions[x * self.size + y] += 1
        if y < self.size - 1:
            if self.maze[x][y + 1] != WALL:
                self.map[x * self.size + y][x * self.size + y + 1] = 1
                self.actions[x * self.size + y] += 1

    def mapSetUp(self):
        for x in range(self.size):
            for y in range(self.size):
                self.findVal(x, y)

    def startRunning(self):
        R = np.array(self.map)
        R[self.end, self.end] = 1000
        Q = np.array(np.zeros([self.size * self.size, self.size * self.size]))
        for _ in range(100):
            for i in range(self.size*self.size):
                current_state = i
                playable_actions = []
                for j in range(self.size*self.size):
                    if R[current_state, j] > 0:
                        playable_actions.append(j)
                for next_state in playable_actions:
                    TD = (R[current_state, next_state] + GAMMA * Q[next_state, np.argmax(Q[next_state,])] -
                          Q[current_state, next_state])
                    Q[current_state, next_state] = Q[current_state, next_state] + ALPHA * TD
        route = [self.start]
        next_location = self.start
        starting_location = self.start
        while next_location != self.end:
            next_location = np.argmax(Q[starting_location,])
            if route.__contains__(next_location) or Q[starting_location, next_location] == 0:
                return []
            route.append(next_location)
            starting_location = next_location
        print(route)
        return route
