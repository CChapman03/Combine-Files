import os
import subprocess
import platform
import time
import resource
import sys
import itertools
from itertools import product

def read_test_file(filename):
    commands = []

    file = open(filename, 'r')

    for line in file.readlines:
        if line == "" or line == " " or line == None:
            # ignore, no command
            pass

        else:
            commands.append(line)

    file.close()

    return commands

def write_test_file(filename):
    file = open(filename, 'w')

    file.write(generate_test_run_file())

    file.close()

def get_combos(req_args, opt_args, dict):

    combos = []
    for L in range(0, len(opt_args)+1):
        for combo in itertools.combinations(opt_args, L):
            s = str(combo)
            s = s.replace("(", "")
            s = s.replace(")", "")
            s = s.replace("'", "")
            s = s.replace(",", "")
            combos.append(s)

    print(combos)
    real_args = []
    for arg in combos:
        vals = dict.get(arg)
        if not vals == None:
            if len(vals) > 0:
                for val in vals:
                    p = "%s %s" % (arg, val)
                    #print(p)
                    real_args.append(p)

            else:
                #print(arg)
                real_args.append(arg)

    print(real_args)

    return combos

def create_run_dict(prog, req_args, opt_args, long_req_args, long_opt_args, test_cases, exp_results):
    run_config = {}

    a = [] + req_args + opt_args
    v = [] + test_cases
    e = [] + exp_results
    #v += [help_vals] + [in_dirs] + [in_files] + [out_dirs] + [out_files] + [limits] + [loop] + [print_stats] + [s_files]

    run_config = dict(zip(a, v))
    run_config["expected_results"] = e

    #opt_args = "-o  -O  -l  -l -L  -p  -p -P".split("  ")
    #long_opt_args = "--output_directory  --output_filename  --file_limit  --file_limit --loop  --print_stats  --print_stats --stats_filename".split("  ")

    combos = get_combos("-h -i -I".split(" "), "-o -O -l -L -p -P".split(" "), run_config)
    
    return run_config

def generate_test_run_file():

    # Required Args
    short_req_args = "-h -i -I".split(" ")
    long_req_args = "--help --input_directory --input_filenames".split(" ")

    req_args = [] + short_req_args + long_req_args

    # Optional Args
    short_opt_args = "-o -O -l -L -p -P".split(" ")
    long_opt_args =  "--output_directory --output_filename --file_limit --loop --print_stats --stats_filename".split(" ")

    opt_args = [] + short_opt_args + long_opt_args

    # Test cases
    help_vals = []
    in_dirs = "../test/blends/ | ../test/blends/my blends/ | ../does/not/exist/ | with/w!@rd//ch#r$/ |  ".split(" | ")
    in_files = "../tests/blends/Blahh.blend ../tests/blends/Cool.blend | ../tests/blends/Blahh.blend ../tests/blends/Cool.blend ../tests/blends/default.blend ../blends/my blends/Nuts N Bolts.blend ../blends/Treee_Scene.blend | does/not/exist.blend | /with/w!@rd//ch#r$/,blend | myblend |  ".split(" | ")
    limits = "-1|0|1|2|5|25|a|*|?| ".split("|")
    loop = []
    out_dirs = "../ | ../test/blends/ | ../test/blends/my blends/ | ../doesnotexist/ | with/w!@rd//ch#r$/ |  ".split(" | ")
    out_files = "my out file | test.blend | out | cool!.blend | with-dashes.blend | with.dots.blend | with/slashes.blend | with~very*char'$,blend |  ".split(" | ")
    print_stats = []
    s_files = "my stat file | test.txt | wow?.txt | with.dots.txt | with/slashes.txt | with~very*char'$,txt |  ".split(" | ")

    test_cases = ([help_vals] + [in_dirs] + [in_files] + [out_dirs] + [out_files] + [limits] + [loop] + [print_stats] + [s_files]) + ([help_vals] + [in_dirs] + [in_files] + [out_dirs] + [out_files] + [limits] + [loop] + [print_stats] + [s_files])

    # Expected Results
    help_vals = ['True']
    in_dirs = "True | True | False | False | False".split(" | ")
    in_files = "True True | True True True True True | False | False | True | False".split(" | ")
    limits = "False True True True True False False False False False".split(" ")
    loop = ['True']
    out_dirs = "True | True | True | False | False | False".split(" | ")
    out_files = "True | True | False | True | True | False | False | False | False".split(" | ")
    print_stats = ['True']
    s_files = "True | True | True | False | False | False | False".split(" | ")

    exp_results = ([help_vals] + [in_dirs] + [in_files] + [out_dirs] + [out_files] + [limits] + [loop] + [print_stats] + [s_files]) + ([help_vals] + [in_dirs] + [in_files] + [out_dirs] + [out_files] + [limits] + [loop] + [print_stats] + [s_files])
    #print(exp_results)

    conf = create_run_dict("combine_blend_files.py", short_req_args, short_opt_args, long_req_args, long_opt_args, test_cases, exp_results)

    s = ""
    prog = "python combine_blend_files.py"
    s += "%s %s\n" % (prog, "-h")
    s += "%s %s\n" % (prog, "--help")


def main():
    write_test_file("test_run_commands.txt")
    
main()