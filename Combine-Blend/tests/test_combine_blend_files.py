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

    file.write(get_run_combinations())

    file.close()

def get_run_combinations():

    run_config = {}

    req_args = "-h -i -I".split(" ")
    long_req_args = "--help --input_directory --input_filenames".split(" ")
    opt_args = "-o  -O  -l  -L  -p  -P".split("  ")
    long_opt_args = "--output_directory  --output_filename  --file_limit  -loop  --print_stats  --stats_filename".split("  ")

    args = []
    long_args = []
    #print(args)

    help_vals = []
    in_dirs = "../test/blends/ | ../test/blends/my blends/ | ../does/not/exist/ | with/w!@rd//ch#r$/ |  ".split(" | ")
    in_files = "../tests/blends/Blahh.blend ../tests/blends/Cool.blend | ../tests/blends/Blahh.blend ../tests/blends/Cool.blend ../tests/blends/default.blend ../blends/my blends/Nuts N Bolts.blend ../blends/Treee_Scene.blend | does/not/exist.blend | /with/w!@rd//ch#r$/,blend | myblend |  ".split(" | ")
    limits = "-1 0 1 2 5 25 a * ?  ".split(" ")
    loop = []
    out_dirs = "../ | ../test/blends/ | ../test/blends/my blends/ | ../doesnotexist/ | with/w!@rd//ch#r$/ |  ".split(" | ")
    out_files = "my out file | test.blend | out | cool!.blend | with-dashes.blend | with.dots.blend | with/slashes.blend | with~very*char'$,blend |  ".split(" | ")
    print_stats = []
    s_files = "my stat file | test.txt | wow?.txt | with.dots.txt | with/slashes.txt | with~very*char'$,txt |  ".split(" | ")

    a = [] + req_args + opt_args + long_req_args + long_opt_args
    v = [] + [help_vals] + [in_dirs] + [in_files] + [out_dirs] + [out_files] + [limits] + [loop] + [print_stats] + [s_files]
    v += [help_vals] + [in_dirs] + [in_files] + [out_dirs] + [out_files] + [limits] + [loop] + [print_stats] + [s_files]

    #print(v)

    run_config = dict(zip(a, v))

    opt_args = "-o  -O  -l  -l -L  -p  -p -P".split("  ")
    long_opt_args = "--output_directory  --output_filename  --file_limit  --file_limit --loop  --print_stats  --print_stats --stats_filename".split("  ")

    combos = []

    for L in range(0, len(opt_args)+1):
        for combo in itertools.combinations(opt_args, L):
            combos.append(combo)

    for L in range(0, len(long_opt_args)+1):
        for combo in itertools.combinations(long_opt_args, L):
            combos.append(combo)

    #print(combos)

    s = ""
    for com in combos:
        s += "%s|" % str(com)
        for x in "( ) , '".split(" "):
            s = s.replace(x, "")
        #print(s)

    x = s.split("|")

    a = []
    for y in x:
        z = y.split(" ")
        z = list(dict.fromkeys(z))

        a += [z]

    combos_array = []
    
    for com in a:
        aa = "-i ".split(" ")  + com
        aa.remove("")
        combos_array.append(aa)
    for com in a:
        aa = "-I ".split(" ")  + com
        aa.remove("")
        combos_array.append(aa)
    for com in a:
        aa = "--input_directory ".split(" ")  + com
        aa.remove("")
        combos_array.append(aa)
    for com in a:
        aa = "--input_filenames ".split(" ")  + com
        aa.remove("")
        combos_array.append(aa)

    #print(combos_array)

    run_config["combos"] = combos_array

    #print(run_config)

    s = ""
    prog = "python combine_blend_files.py"
    s += "%s %s\n" % (prog, "-h")
    s += "%s %s\n" % (prog, "--help")
    for key, val in run_config.items():
        if key == "combos":
            for combo in run_config.get(key):
                s_combo = str(combo)
                #print(s_combo)
                for com in combo:

                    com_key = com
                    com_vals = run_config.get(com_key)
                    #print("com_key = %s" % com_key)
                    #print("com_val = %s" % com_vals)
                    s += "%s %s" % (prog, com_key)

                    i = 0
                    k = ""
                    if not com_vals == None:
                        for v in com_vals:
                            if i < len(com_vals):
                                if not com_key == k:
                                    if com_key == "-i":
                                        s += "\n%s %s " % (prog, com_key)
                                        #print(v)
                                        s += "%s" % v
                                    else:
                                        s += " %s " % com_key
                                        s += "%s" % v
                                else:
                                    s += "\n%s %s " % (prog, com_key)
                                    #print(v)
                                    s += "%s" % v

                            if i == len(com_vals) - 1:
                                s += "\n" if not "-i" in com_key else ""

                            k = com_key
                            i += 1

                    s += "\n"
                            #print("%s %s %s" % (prog, com_key, v))

                #print(s_combo)
                    

    print(s)
    return s


def main():
    write_test_file("test_run_commands.txt")
main()