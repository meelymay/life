import sys, random

class Life:
    def __init__(self, n, shape=None, density=.2):
        self.n = n
        self.grid = [[] for i in range(n)]

        for r in range(n):
            self.grid[r] = [False if random.random() > density else True for i in range(n)]
        if shape:
            density = 0
            m = len(shape)
            n = len(shape[0])
            for i in range(m):
                self.grid[i][0:n] = shape[i]

    def show(self, limit=None, location=(0, 0)):
        y, x = location
        if not limit:
            limit = self.n
        for r in self.grid[y:y+limit]:
            for c in r[x:x+limit]:
                square = 'X' if c else ' '
                print square,
            print

    def neighbors(self, r, c):
        total = 0
        for i in range(-1, 2):
            x = (r+i) % self.n
#             if x < 0 or x >= self.n:
#                 continue
            for j in range(-1, 2):
                y = (c+j) % self.n
#                 if y < 0 or y >= self.n or 
                if (i == 0 and j == 0):
                    continue
                if self.grid[x][y]:
                    total += 1

        return total

    def step(self):
        new_grid = [self.grid[i][:] for i in range(self.n)]
        for r in range(self.n):
            for c in range(self.n):
                neighbors = self.neighbors(r, c)
                
                if neighbors == 3 or (neighbors == 2 and self.grid[r][c]):
                    new_grid[r][c] = True
                else:
                    new_grid[r][c] = False
        self.grid = new_grid

    def find_shape(self, shape):
        for i in range(self.n):
            for j in range(self.n):
                matched = True
                for y in range(len(shape)):
                    if i+y >= self.n:
                        matched = False
                        break
                    for x in range(len(shape[0])):
                        if j+x >= self.n or self.grid[i+y][j+x] != shape[y][x]:
                            matched = False
                            break
                    if not matched:
                        break
                if matched:
                    return (i, j)
        return False

def test_shape(shape, size=22, steps=37, period=10):
    game = Life(size, shape=shape, density=0)
    game.show(limit=5)

    for i in range(steps):
        if i == 1:
            if game.find_shape(shape) == (0, 0):
                print shape, 'stable'
                return False
        if i == 2:
            if game.find_shape(shape) == (0, 0):
                print shape, 'blinker'
                return False
#         if i % 10 == 0:
#             game.show()
        game.step()
    print 'finding location'
    moved = False
    for i in range(period):
        game.step()
        location = game.find_shape(shape)
        if location:
            print location
            game.show(limit=5, location=location)
            moved = True
    return moved

def discover_shapes():
    small = 4
    shape = [[] for i in range(small)]
    for i in range(small):
        shape[i] = [random.random() < .2 for j in range(small)]

    found = False
    while not found or (found and sum([sum([1 for i in row if i]) for row in shape]) == 5):
        x = random.randint(0, small-1)
        y = random.randint(0, small-1)
        shape[x][y] = not shape[x][y]
        found = test_shape(shape)

def main(n):
#     game = Life(50, shape=[
#             [True, False, False, True],
#             [True, False, False, True],
#             [True, True, True, False],
#             [False, False, False, False]
#           ], density=0)
    game = Life(50)
    game.show()
    while raw_input('continue? ') == '':
        game.step()
        game.show()    

#     discover_shapes()

if __name__ == '__main__':
    main(int(sys.argv[1]))
