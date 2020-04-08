import os
import subprocess
import platform
import time
import signal
import sys
import shlex
from shutil import copyfile
import getopt
import argparse

#from data import *

class combine_blend_files:

    # variables

    in_dir = ""
    in_files = []
    out_file = ""
    out_dir = ""
    limit = 0
    loop = False
    stats = True
    s_file = ""
    s_cont = ""
    temp_filename = "output.blend"
    
    first_file = [0]
    last_file = [0]
    start_time = [0]
    time_taken = [0]

    debug = True

    def __init__(self):
        self.in_dir = ""
        self.in_files = []
        self.out_file = ""
        self.out_dir = ""
        self.limit = 0
        self.loop = False
        self.stats = True
        self.s_file = ""
        self.temp_filename = "output.blend"
        self.start_time[0] = 0
        self.first_file[0] = ""
        self.last_file[0] = ""
        self.time_taken[0] = 0

        self.debug = True

    def get_num_files(self, path, is_dir = True):
        num_files = [0]
        for f in os.listdir(path):
            fe = os.path.splitext(f)[1]

            if fe == ".blend":
                num_files[0] += 1

        if is_dir:
            return num_files[0]

        else: 
            return len(path)

    def get_platform(self):
        return platform.system()

    def execute_blender(self, cmd, time_limit = 60*5, stop = False, capture_out = False):
        fn = cmd.split("-P ")[1].split(".")[0]

        # Craete Log Files Per Subprocess

        start_time = 0
        p = None

        if self.debug:
            out = open("../logs/%s_out.txt" % fn, "w")
            err = open("../logs/%s_err.txt" % fn, "w")

            p = subprocess.Popen(cmd.split(" "), stdout=out, stderr=err, text=True)
            start_time = time.time()
        else:
            if self.stats:
                out = open("%s/%s" % (self.out_dir, self.s_file), 'w')

                p = subprocess.Popen(cmd.split(" "), stdout=out, text=True)
                start_time = time.time()

        #is_running = True
        while p.returncode == None:
            p.poll()

            if time.time() - start_time > time_limit:
                if stop:
                    p.kill()
                    raise Exception("Process with command '%s' has failed to do its job" % cmd)
                
                p.kill()
                raise Exception("Process with command '%s' has failed to do its job" % cmd)
            
        p.wait()

        if capture_out:
            return p.stdout
        else:
            return None


    def init(self, file):

        # Initailize/Create Temporary Output Blend and Delete Everything in it

        self.start_time[0] = time.time()
        fn = os.path.splitext(file)[0]

        if fn.find(" "):
            self.first_file[0] = fn.replace(" ", "_")
        else:
            self.first_file[0] = fn

        # Create temp output.blend file
        linux_mac_cmd = "blender -b -P create.py -- %s %s" % (self.out_dir, self.temp_filename)
        win_cmd = "blender.exe -b -P create.py -- %s %s" % (self.out_dir, self.temp_filename)

        cmd = linux_mac_cmd if self.get_platform() == 'Linux' else win_cmd
        f = "%s/%s" % (self.out_dir, self.temp_filename)
        stop_condition = os.path.isfile(f) and os.path.getsize(f) == 0
        self.execute_blender(cmd, 20, stop_condition)
        
        # Clean temp output.blend file
        linux_mac_cmd = "blender -b %s/%s -P clean.py -- %s %s" % (self.out_dir, self.temp_filename, self.out_dir, self.temp_filename)
        win_cmd = "blender.exe -b %s/%s -P clean.py -- %s %s" % (self.out_dir, self.temp_filename, self.out_dir, self.temp_filename)

        cmd = linux_mac_cmd if self.get_platform() == 'Linux' else win_cmd
        f = "%s/%s" % (self.out_dir, self.temp_filename)
        stop_condition = os.path.isfile(f) and os.path.getsize(f) == 0
        self.execute_blender(cmd, 20, stop_condition)

        # Remove duplicate output.blend (Created By Cleaning Temporary Output Blend)
        os.remove("%s/%s1" % (self.out_dir, self.temp_filename))

    def run(self, file, i):

        # Run Per Input Blend File
        in_filesize = os.path.getsize("%s/%s" % (self.in_dir, file))

        #Execute Blender
        linux_mac_cmd = "blender -b %s/%s -P combine.py -- %s %s %s %d %s" % (self.out_dir, self.temp_filename, self.temp_filename, file, self.in_dir, in_filesize, self.out_dir)
        win_cmd = "blender.exe -b %s/%s -P combine.py -- %s %s %s %d %s" % (self.out_dir, self.temp_filename, self.temp_filename, file, self.in_dir, in_filesize, self.out_dir)
        #portable_cmd = "blender -b %s/%s -P combine.py -- $s %s %s %d" % (in_dir, file, in_dir, file, temp_filename, in_filesize)

        cmd = linux_mac_cmd if self.get_platform() == 'Linux' or self.get_platform() == 'Darwin' else win_cmd
        #stop_condition = False
        self.execute_blender(cmd)

        # Remove duplicate output.blend
        #os.remove("%s/%s1" % (self.in_dir, self.temp_filename))

    def terminate(self, file, num_files):

        # Save, Print Statistics, and Rename Output Blend

        fn = os.path.splitext(file)[0]

        if fn.find(" "):
            self.last_file[0] = fn.replace(" ", "_")
        else:
            self.last_file[0] = fn

        out_file = "%s-%s" % (self.first_file[0], self.last_file[0])
        
        self.time_taken[0] = time.time() - self.start_time[0]
        filesize = os.path.getsize("%s/%s" % (self.out_dir, self.temp_filename))

        linux_mac_cmd = "blender -b %s/%s -P statistics.py -- %s %s %f %d %d" % (self.out_dir, self.temp_filename, self.out_dir, out_file, self.time_taken[0], num_files, filesize)
        win_cmd = "blender.exe -b %s/%s -P statistics.py -- %s %s %f %d %d" % (self.out_dir, self.temp_filename, self.out_dir, out_file, self.time_taken[0], num_files, filesize)

        cmd = linux_mac_cmd if self.get_platform() == 'Linux' else win_cmd
        self.execute_blender(cmd, capture_out=True)

        # Remove Temporary Output Blend (To Be Replaced by: '<First_Blend_File>-<Last_Blend_File>.blend')
        os.remove("%s/%s" % (self.out_dir, self.temp_filename))
        os.remove("%s/%s1" % (self.out_dir, self.temp_filename))
        #os.remove(os.path.join(self.in_dir, "%s" % self.temp_filename)

        if not self.debug:
            # cleanup stat file
            # TODO Cleanup output Stat File
            pass


    def combine_to(self, i, file, amount, once = False):
        
        # Combine Blend Files Up To Set Amount (In Case There are Too Many Blends in Input Directory)
        
        if i == 0:
            self.init(file)

        if i < amount:
            self.run(file, i)
        
        if i == amount - 1:
            self.terminate(file, self.limit)

            if not once:
                i = -1

    def combine(self, i, file, num_files):

        # Combine ALL Blend Files in Input Directory

        if i == 0:
            self.init(file)

        if i < num_files:
            self.run(file, i)
            print(file)
        
        if i == num_files - 1:
            self.terminate(file, num_files)

    
    def is_file_vaild(self, filename):

        invaid_tokens = []

        if os.path.isfile(filename):
            invaid_tokens = "/ % * @ # > < ; | &".split(" ")

        elif os.path.isdir(filename):
            invaid_tokens = "% * @ # > < ; | &".split(" ")

        valid = True
        for t in invaid_tokens:
            if t in filename and " " in filename:
                valid = False

        if not valid:
            msg = "Please Specifiy a Valid Filename!" % filename
            print(msg)
            print("Filename was: %s" % filename)

            sys.exit(1)

    def create_stat_file(self, filename):
        f = open(filename, 'w')

        parse = False
        i0 = self.s_cont.index("----------------------------------------")
        i1 = self.s_cont.rfind("----------------------------------------")
        i = 0
        for line in self.s_cont.split("\n"):
            if i == i0:
                parse = True

            if i > i1:
                parse = False

            # if parse:
            f.write("%s\n" % line)

            i += 1
        f.close()

    def main(self, args):

        use_in_files = args.input_directory == None

        self.in_files = args.input_filenames if not args.input_filenames == None else []
        
        in_file_array = self.in_files if use_in_files else []
        use_in_files = use_in_files and not len(in_file_array) == 0
        print(in_file_array)
        
        use_in_dir = not use_in_files and len(in_file_array) == 0
        use_limit = not args.file_limit == 0
        use_looping = args.loop

        self.in_dir = os.path.abspath(args.input_directory[0]) if use_in_dir else ""
        self.out_dir = os.path.abspath(os.path.relpath(args.output_directory[0]))
        #print(self.out_dir)
        self.out_file = args.output_filename[0]
        self.limit = args.file_limit
        self.stats = args.print_stats
        self.s_file = args.stats_filename[0] if args.print_stats else ""

        if use_in_dir:
            # Using input directory for input files
            #print("Using input directory")
            
            if use_limit:
                # Use Limit

                if use_looping:
                    # Use Looping
                    
                    #------------------------------------
                    # RUN COMBINE TO MULTIPLE TIMES
                    #------------------------------------

                    i = [0]
                    for file in os.listdir(self.in_dir):
                        fe = os.path.splitext(file)[1]

                        if fe == ".blend":
                            self.combine_to(i[0], file, self.limit)

                            i[0] += 1

                else:
                    # DONT use Looping

                    #------------------------------------
                    # RUN COMBINE TO ONCE
                    #------------------------------------

                    i = [0]
                    for file in os.listdir(self.in_dir):
                        fe = os.path.splitext(file)[1]

                        if fe == ".blend":
                            self.combine_to(i[0], file, self.limit, once=True)

                            i[0] += 1

            else:
                # DONT use Limit

                #------------------------------------
                # RUN COMBINE
                #------------------------------------

                #print("Running without limit")

                i = [0]
                for file in os.listdir(self.in_dir):
                    fe = os.path.splitext(file)[1]

                    num_files = len(os.listdir(self.in_dir))
                    
                    #print("Number of files = %d" % num_files)
                    #print(self.in_dir)

                    if fe == ".blend":
                        self.combine(i[0], file, num_files)

                        i[0] += 1
                
        elif use_in_files:
            # Using Speciic Input Files

            if use_limit:
                # Use Limit

                if use_looping:
                    # Use Looping

                    #------------------------------------
                    # RUN COMBINE TO MULTIPLE TIMES
                    #------------------------------------

                    i = [0]
                    for file in in_file_array:
                        fe = os.path.splitext(file)[1]

                        if fe == ".blend":
                            self.combine_to(i[0], file, self.limit)

                            i[0] += 1
                    
                else:
                    # DONT use Looping

                    #------------------------------------
                    # RUN COMBINE TO ONCE
                    #------------------------------------

                    i = [0]
                    for file in in_file_array:
                        fe = os.path.splitext(file)[1]

                        if fe == ".blend":
                            self.combine_to(i[0], file, self.limit, once=True)

                            i[0] += 1

            else:
                # DONT use Limit

                #------------------------------------
                # RUN COMBINE
                #------------------------------------

                i = [0]
                for file in in_file_array:
                    fe = os.path.splitext(file)[1]

                    if fe == ".blend":
                        num_files = len(in_file_array)
                        self.combine(i[0], file, num_files)

                        i[0] += 1

        else:
            print("Please specify either an input directory or a set of input files!")
            sys.exit(1)


if __name__ == "__main__":
    # arg_list = sys.argv[1:]
    # options = "hiIoOlLpP"
    # long_options = "help input_directory input_filenames output_filename output_directory file_limit loop print_stats stats_filename".split(" ")
    
    # is_vaild_run = False
    c = combine_blend_files()

    try: 

        parser = argparse.ArgumentParser(description='A script to combine two or more Blender (.blend) files together.')

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--input_directory', "-i", type=str, nargs=1,
                    help='the directory where the input blender files are stored.')

        group.add_argument('--input_filenames', '-I', type=str, nargs='+',
                    help='combine specific blender files together.')

        out_dir_default = c.in_dir
        parser.add_argument('--output_directory', '-o', type=str, nargs=1, default=out_dir_default,
                    help='the path to store the generated/combined output blend file(s) (uses INPUT_DIRECTORY if not specified).')

        out_file_default = "%s-%s" % (c.first_file, c.last_file)
        parser.add_argument('--output_filename', '-O', type=str, nargs=1, default=out_file_default,
                    help="the name of the generated/combined output blend file (uses '<FIRST_FILENAME>-<LAST_FILENAME>.blend' if not specified).")  

        parser.add_argument('--file_limit', '-l', type=int, nargs=1, default=0,
                    help='the number of blend files to combine from the specifed files (used to prevent very large output blend files).')

        parser.add_argument('--loop', '-L', action='store_true',
                    help='continue combining blend files after file limit is reached until the last input file is processed (# OF OUTPUT BLENDS = # of INPUT BLENDS / FILE LIMIT)')

        parser.add_argument('--print_stats', '-p', action='store_true',
                    help="print the combine process results/statistics to a text file ('<OUTPUT_FILE>_Stats.txt' will be used if not specified).")

        s_file_default = "%s/%s-%s_Stats.txt" % (c.out_dir, c.first_file, c.last_file)
        parser.add_argument('--stats_filename', '-P', type=str, nargs=1, default=s_file_default,
                    help="the filename of the results/statistics text file (to be used in conjunction with the --print_stats command).")          

        args = parser.parse_args()
        c.main(args)

    except:
        sys.exit(2)

    #     # Parse args
    #     args, values = getopt.getopt(arg_list, options, long_options) 
        
    #     #run_main = False

    #     # checking each argument 
    #     for currentArgument, currentValue in args:
    
    #         if currentArgument in ("-h", "--help"): 
    #             print("usage: combine_blend_files.py [-h] [-i INPUT_DIRECTORY | -I INPUT_FILES]")
    #             print("")
    #             print("Description: ")
    #             print("A script to combine two or more Blender (.blend) files together.")
    #             print("")
    #             print("optional arguments: ")
    #             print("-h, --help\tshow help message and exit")
    #             print("-i, --input_directory\tthe directory where the input blender files are stored.")
    #             print("-I, --input_filenames\tcombine specific blender files together.")
    #             print("-o, --output_directory\tthe path to store the generated/combined output blend file(s) (uses INPUT_DIRECTORY by default).")
    #             print("-O, --output_filename\tthe name of the generated/combined output blend file (uses '<FIRST_FILENAME>-<LAST_FILENAME>.blend' by default).")
    #             print("-l, --file_limit\tthe number of blend files to combine from the specifed files (used to prevent very large output blend files).")
    #             print("-L, --loop\tcontinue combining blend file after file limit is reached until the last input file is processed (# OF OUTPUT BLENDS = # of INPUT BLENDS / FILE LIMIT)")
    #             print("-p, --print_stats\tprint the combine process results/statistics to a text file ('<OUTPUT_FILE>_Stats.txt' will be used as default).")
    #             print("-P, --stats_filename\tthe filename of the results/statistics text file (to be used in conjunction with the --print_stats command).")

    #         elif currentArgument in ("-i", "--input_directory"):
    #             #c.in_dir = os.path.relpath(currentValue) + "/"
    #             is_vaild_run = True
    #             print(currentValue)
                
    #         elif currentArgument in ("-o", "--output_directory"): 
    #             c.out_dir = os.path.abspath(currentValue) + "/"

    #         elif currentArgument in ("-I", "--input_filenames"):
    #             c.in_files = shlex.split(currentValue)
    #             is_vaild_run = True
                
    #         elif currentArgument in ("-O", "--output_filename"): 
    #             c.out_file = os.path.abspath(currentValue)

    #         elif currentArgument in ("-l", "--file_limit"):
    #             c.limit = int(currentValue)
                
    #         elif currentArgument in ("-L", "--loop"): 
    #             c.loop = True

    #         elif currentArgument in ("-p", "--print_stats"):
    #             c.stats = True
                
    #         elif currentArgument in ("-P", "--stats_filename"): 
    #             c.s_file = os.path.abspath(currentValue)

    #         # elif currentArgument in ("-r", "--run"):

    #         #     # ---------------------------------------------------------------

    #         #     # TODO: Get combine_blend_files.py to run using Command line Arguments.
                
    #         #     # ---------------------------------------------------------------
    #         #     if is_vaild_run:
    #         #         c.main() # NOT Working!
    #         #     else:
    #         #         sys.exit(1)
            
    # except getopt.error as err: 
    #     # output error, and return with an error code 
    #     print (str(err))
    #     sys.exit(2)

    # if is_vaild_run:
    #     c.main()
    # else:
    #     sys.exit(1)