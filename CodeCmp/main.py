"""
在 Generator.py 中编写样例输入的生成器，运行 main.py 即可
"""

import os
import sys
import time

from Generator import test_case_generator as generator

if len(sys.argv) == 3:
    my_code_name = sys.argv[1]
    reference_code_name = sys.argv[2]
else:
    my_code_name = "mine"  # input("Input your code's file name(without .cpp): ")
    reference_code_name = "refer"  # input("Input reference code's file name(without .cpp): ")

for case in generator():
    # generate test.in
    with open("test.in", "w") as test:
        test.write(case)

    # execute g++ cmd
    os.system("g++ {0}.cpp -o {0}.exe".format(my_code_name))
    os.system("g++ {0}.cpp -o {0}.exe".format(reference_code_name))

    # get output
    start_timer = time.time_ns()
    with os.popen(my_code_name + '<' + 'test.in', 'r') as f:
        mine_output = f.read()
    end_timer = time.time_ns()
    mine_time = end_timer - start_timer

    start_timer = time.time_ns()
    with os.popen(reference_code_name + '<' + 'test.in', 'r') as f:
        reference_output = f.read()
    end_timer = time.time_ns()
    reference_time = end_timer - start_timer

    # output comparison
    if mine_output == reference_output:
        print("√ Input: \n" + case)
    else:
        print("× Input: \n" + case)
        print("  My output: " + mine_output)
        print("  Re output: " + reference_output)

    # output time
    print("My:", mine_time, "ns")
    print("Re:", reference_time, "ns")
