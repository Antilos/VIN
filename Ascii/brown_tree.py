import argparse, random, logging, time
import copy
# from PIL import Image, ImageDraw

class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.arr = [[0 for _ in range(height)] for _ in range(width)]

        self.cluster_prob_factor = 0.75

        # self._SHADES = ".:-=+*#%@$"
        # self._SHADES = " -=+*#"
        self._SHADES = " +#@X$"
        self._DIRECTIONS = [((0, 1), 1), ((1, 1), 1), ((1, 0), 1), ((1, -1), 1), ((0, -1), 1), ((-1, -1), 1), ((-1, 0), 1), ((-1, 1), 1)]
        # self_DIRECTION_WEIGHTS = [1, 1, 1, 1, 1, 1, 1, 1]

        self.steps = []

    def cluster_prob(self, new_val:int, old_val:int) -> float:
        return (1.0 - (old_val / len(self._SHADES))) * self.cluster_prob_factor

    def seed(self, x:int, y:int, val:int=1) -> None:
        self.arr[x][y] = val

    def introduce_particle(self, val=1, collision_avoidance_method = "regenerate"):
        x, y = random.choice(range(args.width)), random.choice(range(args.height))

        while self.arr[x][y] > 0:
            if collision_avoidance_method == "regenerate":
                x, y = random.choice(range(args.width)), random.choice(range(args.height))
            elif collision_avoidance_method == "shift":
                raise NotImplementedError()

        self.arr[x][y] = val
        self.random_walk(x, y)
        self.steps.append(copy.deepcopy(self.arr))

    def introduce_particle_at_pos(self, x, y, val=1):
        self.arr[x][y] = val
        self.random_walk(x, y)
        self.steps.append(copy.deepcopy(self.arr))

    def random_walk(self, start_x, start_y):
        x, y = start_x, start_y
        val = self.arr[x][y]
        self.arr[x][y] = 0

        while True:
            dirs = list(filter(lambda dir : not (0 > x + dir[0][0] or (self.width - 1)  < x + dir[0][0] or 0 > y + dir[0][1] or (self.height - 1) < y + dir[0][1]), self._DIRECTIONS))
            dir = random.choices([dir for (dir, _) in dirs], weights=[weight for (_, weight) in dirs])
            new_pos = x+dir[0][0], y+dir[0][1]
            # if 0 > new_pos[0] or self.width < new_pos[0] or 0 > new_pos[1] or self.height < new_pos[1]:
            #     continue

            # Collision
            if self.arr[new_pos[0]][new_pos[1]] > 0:
                # Combine
                # self.arr[new_pos[0]][new_pos[1]] <= len(self._SHADES) and
                if self.arr[new_pos[0]][new_pos[1]] <= len(self._SHADES) and random.random() < self.cluster_prob(val, self.arr[new_pos[0]][new_pos[1]]):
                    self.arr[new_pos[0]][new_pos[1]] = min(len(self._SHADES)-1, self.arr[new_pos[0]][new_pos[1]] + val)
                else: # Start new
                    self.arr[x][y] = val
                break
            else:
                x, y = new_pos

    

    def heat2ascii(self, val:int):
        # return 'x' if val > 0 else '.'
        # return str(val)
        return self._SHADES[val]

    def __str__(self) -> str:
        return '\n'.join([''.join([self.heat2ascii(cell) for cell in row]) for row in self.arr])

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('width', type=int)
    parser.add_argument('height', type=int)
    parser.add_argument('particles', type=int)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    # logging.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)
    
    field = Field(args.width, args.height)
    start_time = time.time()

    seed_x, seed_y = int(args.width/2), int(args.height/2)
    logging.info(f"Seeding at ({seed_x}, {seed_y})")
    field.seed(seed_x, seed_y)
    for i in range(args.particles):
        particle_start = time.time()
        field.introduce_particle()
        particle_end = time.time()
        logging.info(f"Particle {i+1}/{args.particles} ({(particle_end - particle_start):.3f}s)")

    end_time = time.time()

    logging.info(f"Simulating {args.particles} particles took {(end_time - start_time):.3f} seconds.")
    
    with open("test_out.txt", 'w') as fout:
        fout.write(str(field))

    for i, step in enumerate(field.steps):
        with open(f"test_steps/test_step_{i}.txt", 'w') as fout:
            fout.write('\n'.join([''.join([field.heat2ascii(cell) for cell in row]) for row in step]))