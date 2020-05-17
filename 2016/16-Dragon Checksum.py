# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": ('110010110100', 12),
                     "expected": '100',
                    }

test += 1
test_data[test]   = {"input": ('10000', 20),
                     "expected": '01100',
                    }

test = 'real'
test_data[test] = {"input": ('10001110011110000', 272),
                     "expected": '10010101010011101',
                    }
test = 'real2'
test_data[test] = {"input": ('10001110011110000', 35651584),
                     "expected": '01100111101101111',
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real2'
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected']
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #

disk_contents = puzzle_input[0]
while len(disk_contents) < puzzle_input[1]:
    disk_contents += '0' + disk_contents[::-1].replace('1', 'a').replace('0', '1').replace('a', '0')

disk_contents = disk_contents[:puzzle_input[1]]



new_checksum = disk_contents
while len(new_checksum) % 2 == 0:
    old_checksum = new_checksum
    new_checksum = ''

    for i in range (len(old_checksum) // 2):

        if old_checksum[i*2] == old_checksum[i*2+1]:
            new_checksum += '1'
        else:
            new_checksum += '0'

puzzle_actual_result = new_checksum



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




