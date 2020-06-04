# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>
p=<3,0,0>, v=<-1,0,0>, a=<0,0,0>""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['125', '461'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #

max_accel = 10**6

if part_to_test == 1:
    part_nr = 0
    for string in puzzle_input.split('\n'):
        _, _, acceleration = string.split(' ')
        acceleration = list(map(int, acceleration[3:-1].split(',')))

        if max_accel > sum(map(abs, acceleration)):
            max_accel = sum(map(abs, acceleration))
            closest_part = part_nr

        part_nr += 1

    puzzle_actual_result = closest_part



else:
    particles = {}
    collisions = []
    part_nr = 0
    saved_len = 0
    for string in puzzle_input.split('\n'):
        position, speed, acceleration = string.split(' ')
        position = list(map(int, position[3:-2].split(',')))
        speed = list(map(int, speed[3:-2].split(',')))
        acceleration = list(map(int, acceleration[3:-1].split(',')))

        particles[part_nr] = [position, speed, acceleration]

        part_nr += 1

    for i in range(10**4):
        collisions = []
        for part_nr in particles:
            position, speed, acceleration = particles[part_nr]
            speed = [speed[x] + acceleration[x] for x in range (3)]
            position = [position[x] + speed[x] for x in range (3)]
            particles[part_nr] = [position, speed, acceleration]
            collisions.append(position)

        coordinates = [','.join(map(str, collision)) for collision in collisions]

        list_particles = list(particles.keys())
        for part_nr in list_particles:
            if collisions.count(particles[part_nr][0]) > 1:
                del particles[part_nr]

        if i % 10 == 0 and len(particles) == saved_len:
            break
        elif i % 10 == 0:
            saved_len = len(particles)

    puzzle_actual_result = len(particles)




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




