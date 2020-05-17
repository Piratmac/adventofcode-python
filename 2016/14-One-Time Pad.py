# -------------------------------- Input data -------------------------------- #
import os, hashlib

test_data = {}

test = 1
test_data[test]   = {"input": """abc""",
                     "expected": ['22728', '22551'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
test_data[test] = {"input": 'qzyelonm',
                     "expected": ['15168', '20864'],
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

if part_to_test == 1:
    index = 0
    found_keys = 0
    while True:
        index += 1
        init_hash = hashlib.md5((puzzle_input + str(index)).encode('utf-8')).hexdigest()
        triplets = [x for x in '0123456789abcdef' if x*3 in init_hash]

        if triplets:
            first_triplet_position = min ([init_hash.find(x*3) for x in triplets])
            triplet = init_hash[first_triplet_position]

            for i in range (1, 1000):
                new_hash = hashlib.md5((puzzle_input + str(index + i)).encode('utf-8')).hexdigest()
                if triplet * 5 in new_hash:
                    found_keys += 1
                    print (init_hash, triplet, index, index + i, found_keys)
                    break

        if found_keys == 64:
            puzzle_actual_result = index
            break


else:
    hashes = []
    hashes_first_triplet = {}
    hashes_quintuplets = {}
    index = -1
    found_keys = 0

    for i in range (30000):
        hash_text = puzzle_input + str(i)
        for y in range (2017):
            hash_text = hashlib.md5(hash_text.encode('utf-8')).hexdigest()
        hashes.append(hash_text)

        triplets = [x for x in '0123456789abcdef' if x*3 in hash_text]

        if triplets:
            first_triplet_position = min ([hash_text.find(x*3) for x in triplets])
            hashes_first_triplet[i] = hash_text[first_triplet_position]

        quintuplets = [x for x in '0123456789abcdef' if x*5 in hash_text]

        if quintuplets:
            hashes_quintuplets[i] = quintuplets

        if i % 100 == 0:
            print ('calculated', i)

    print ('Calculated hashes')


    print (hashes_first_triplet)
    print (hashes_quintuplets)

    for index, triplet in hashes_first_triplet.items():
        for i in range (1, 1000):
            if index + i in hashes_quintuplets:
                if triplet in hashes_quintuplets[index + i]:
                    found_keys += 1
                    print (hashes[index], triplet, index, index + i, found_keys)
                    break

        if found_keys == 64:
            puzzle_actual_result = index
            break



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




