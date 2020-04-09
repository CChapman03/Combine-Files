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


    req_args = "-h --help -i --input_directory -I --input_filenames".split(" ")
    opt_args1 = "-o  -O  -l  -L  -p  -p -P".split("  ")
    opt_args2 = "--output_directory  --output_filename  --file_limit  --loop  --print_stats  --print_stats --stats_filename".split("  ")

    in_dirs = "../test/blends/ | ../test/blends/my blends/ | ../does/not/exist/ | with/w!@rd//ch#r$/ |  ".split(" | ")
    in_files = "../tests/blends/Blahh.blend ../tests/blends/Cool.blend | ../tests/blends/Blahh.blend ../tests/blends/Cool.blend ../tests/blends/default.blend ../blends/my blends/Nuts N Bolts.blend ../blends/Treee_Scene.blend | does/not/exist.blend | /with/w!@rd//ch#r$/,blend | myblend |  ".split(" | ")
    limits = "-1 0 1 2 5 25 a * ?  ".split(" ")
    out_dirs = "../ | ../test/blends/ | ../test/blends/my blends/ | ../doesnotexist/ | with/w!@rd//ch#r$/ |  ".split(" | ")
    out_files = "my out file | test.blend | out | cool!.blend | with-dashes.blend | with.dots.blend | with/slashes.blend | with~very*char'$,blend |  ".split(" | ")
    s_files = "my stat file | test.txt | wow?.txt | with.dots.txt | with/slashes.txt | with~very*char'$,txt |  "

    combos = " "
    for L in range(0, len(opt_args1)+1):
        for sub1 in itertools.combinations(opt_args1, L):
            for s1 in sub1:
                combos += "%s " % s1
            combos += " | "

    for L in range(0, len(opt_args2)+1):
        for sub1 in itertools.combinations(opt_args2, L):
            for s1 in sub1:
                combos += "%s " % s1
            combos += " | "

    print(combos)

    final_str = ""
    for r in req_args:
        for com in combos.split(" | "):
            for c in com:
                if r == "-i":
                    for in_dir in in_dirs:
                        i = "%s %s" % ("-i", in_dir)
                        cc = ""
                        for a in c.split(" "):
                            if a == "-o" or a == "--output_directory":
                                for out_d in out_dirs:
                                    cc += "%s %s" % (c, out_d)
                            if a == "-O" or a == "--output_filename":
                                for out_f in out_files:
                                    cc += "%s %s" % (c, out_f)
                            if a == "-l" or a == "--file_limit":
                                for fl in limits:
                                    cc += "%s %s" % (c, fl)
                            if a == "-P" or a == "--stats_filename":
                                for sf in s_files:
                                    cc += "%s %s" % (c, sf)

                        final_str += "python combine_blend_files.py %s %s\n" % (i, cc)

                if r == "--input_directory":
                    for in_dir in in_dirs:
                        i = "%s %s" % ("--input_directory", in_dir)
                        cc = ""
                        for a in c.split(" "):
                            if a == "-o" or a == "--output_directory":
                                for out_d in out_dirs:
                                    cc += "%s %s" % (c, out_d)
                            if a == "-O" or a == "--output_filename":
                                for out_f in out_files:
                                    cc += "%s %s" % (c, out_f)
                            if a == "-l" or a == "--file_limit":
                                for fl in limits:
                                    cc += "%s %s" % (c, fl)
                            if a == "-P" or a == "--stats_filename":
                                for sf in s_files:
                                    cc += "%s %s" % (c, sf)

                        final_str += "python combine_blend_files.py %s %s\n" % (i, cc)

                if r == "-I":
                    for in_f in in_files:
                        i = "%s %s" % ("-I", in_f)
                        cc = ""
                        for a in c.split(" "):
                            if a == "-o" or a == "--output_directory":
                                for out_d in out_dirs:
                                    cc += "%s %s" % (c, out_d)
                            if a == "-O" or a == "--output_filename":
                                for out_f in out_files:
                                    cc += "%s %s" % (c, out_f)
                            if a == "-l" or a == "--file_limit":
                                for fl in limits:
                                    cc += "%s %s" % (c, fl)
                            if a == "-P" or a == "--stats_filename":
                                for sf in s_files:
                                    cc += "%s %s" % (c, sf)

                        final_str += "python combine_blend_files.py %s %s\n" % (i, cc)
                        

                if r == "--input_filenames":
                    for in_dir in in_dirs:
                        i = "%s %s" % ("--input_filenames", in_dir)
                        cc = ""
                        for a in c.split(" "):
                            if a == "-o" or a == "--output_directory":
                                for out_d in out_dirs:
                                    cc += "%s %s" % (c, out_d)
                            if a == "-O" or a == "--output_filename":
                                for out_f in out_files:
                                    cc += "%s %s" % (c, out_f)
                            if a == "-l" or a == "--file_limit":
                                for fl in limits:
                                    cc += "%s %s" % (c, fl)
                            if a == "-P" or a == "--stats_filename":
                                for sf in s_files:
                                    cc += "%s %s" % (c, sf)

                        final_str += "python combine_blend_files.py %s %s\n" % (i, cc)

    return final_str

    #return str(subset)

    # for r in r_args:
    #     if r == "-h":
    #         s += "python combine_blend_files.py -h\n"

    #     if r == "--help":
    #         s += "python combine_blend_files.py --help\n"
                
    #     if r == "-i":
    #         for i in in_dirs:
    #             s += "python combine_blend_files.py -i %s\n" % i

    #         for o in o_args:
    #             if o == "-o":
    #                 s += "python combine_blend_files.py -i %s" % o

    #     if r == "--input_directory":
    #         for i in in_dirs:
    #             s += "python combine_blend_files.py --input_directory %s\n" % i
    #     if r == "-I":
    #         for i in in_files:
    #             s += "python combine_blend_files.py -I %s\n" % i
    #     if r == "--input_filenames":
    #         for i in in_files:
    #             s += "python combine_blend_files.py --input_filenames %s\n" % i

    #return s


def main():
    write_test_file("test_run_commands.txt")
main()