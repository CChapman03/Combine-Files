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
    in_files = None
    out_file = ""
    out_dir = ""
    limit = None
    loop = False
    stats = True
    s_file = ""
    s_cont = ""
    temp_filename = "output.blend"
    
    first_file = [0]
    last_file = [0]
    start_time = [0]
    time_taken = [0]

    def __init__(self):
        self.in_dir = ""
        self.in_files = []
        self.out_file = ""
        self.out_dir = ""
        self.limit = None
        self.loop = False
        self.stats = True
        self.s_file = ""
        self.temp_filename = "output.blend"
        self.start_time[0] = 0
        self.first_file[0] = ""
        self.last_file[0] = ""
        self.time_taken[0] = 0

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
        out = open("../logs/%s_out.txt" % fn, "w")
        err = open("../logs/%s_err.txt" % fn, "w")

        p = subprocess.Popen(cmd.split(" "), stdout=out, stderr=err, text=True)
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
        linux_mac_cmd = "blender -b -P create.py -- '%s' '%s'" % (self.in_dir, self.temp_filename)
        win_cmd = "blender.exe -b -P create.py -- '%s' '%s'" % (self.in_dir, self.temp_filename)

        cmd = linux_mac_cmd if self.get_platform() == 'Linux' else win_cmd
        stop_condition = os.path.isfile(os.path.join(self.in_dir, self.temp_filename)) and os.path.getsize(os.path.join(self.in_dir, self.temp_filename)) == 0
        self.execute_blender(cmd, 20, stop_condition)

        # Clean temp output.blend file
        linux_mac_cmd = "blender -b %s/%s -P clean.py -- '%s' '%s'" % (self.in_dir, self.temp_filename, self.in_dir, self.temp_filename)
        win_cmd = "blender.exe -b %s/%s -P clean.py -- '%s' '%s'" % (self.in_dir, self.temp_filename, self.in_dir, self.temp_filename)

        cmd = linux_mac_cmd if self.get_platform() == 'Linux' else win_cmd
        stop_condition = os.path.isfile(os.path.join(self.in_dir, self.temp_filename)) and os.path.getsize(os.path.join(self.in_dir, self.temp_filename)) == 0
        self.execute_blender(cmd, 20, stop_condition)

        # Remove duplicate output.blend (Created By Cleaning Temporary Output Blend)
        os.remove("%s/%s1" % (self.in_dir, self.temp_filename))

    def run(self, file, i):

        # Run Per Input Blend File

        in_filesize = os.path.getsize("%s/%s" % (self.in_dir, file))

        filename = file
        # check for filename spaces
        if file.find(" "):
            filename = file.replace(" ", "_")

            if not file == filename:
                #Copy File to File without Spaces
                copyfile("%s/%s" % (self.in_dir, file), "%s/%s" % (self.in_dir, filename))

                #Execute Blender
                linux_mac_cmd = "blender -b %s/%s -P combine.py -- %s %s %s %d" % (self.in_dir, self.temp_filename, self.temp_filename, filename, self.in_dir, in_filesize)
                win_cmd = "blender.exe -b %s/%s -P combine.py -- %s %s %s %d" % (self.in_dir, self.temp_filename, self.temp_filename, filename, self.in_dir, in_filesize)
                #portable_cmd = "blender -b %s/%s -P combine.py -- $s %s %s %d" % (in_dir, file, in_dir, file, temp_filename, in_filesize)

                cmd = linux_mac_cmd if self.get_platform() == 'Linux' or self.get_platform() == 'Darwin' else win_cmd
                #stop_condition = False
                self.execute_blender(cmd)

                #os.remove("%s/%s" % (in_dir, filename))

                # Remove duplicate output.blend
                os.remove("%s/%s1" % (self.in_dir, self.temp_filename))

        elif not file.find(" "):
            #filename = file

            #Execute Blender
            linux_mac_cmd = "blender -b %s/%s -P combine.py -- %s %s %s %d" % (self.in_dir, self.temp_filename, self.temp_filename, filename, self.in_dir, in_filesize)
            win_cmd = "blender.exe -b %s/%s -P combine.py -- %s %s %s %d" % (self.in_dir, self.temp_filename, self.temp_filename, filename, self.in_dir, in_filesize)
            #portable_cmd = "blender -b %s/%s -P combine.py -- $s %s %s %d" % (in_dir, file, in_dir, file, temp_filename, in_filesize)

            cmd = linux_mac_cmd if self.get_platform() == 'Linux' or self.get_platform() == 'Darwin' else win_cmd
            #stop_condition = False
            self.execute_blender(cmd)

            # Remove duplicate output.blend
            #os.remove("%s/%s1" % (in_dir, temp_filename))

    def terminate(self, file, num_files):

        # Save, Print Statistics, and Rename Output Blend

        fn = os.path.splitext(file)[0]

        if fn.find(" "):
            self.last_file[0] = fn.replace(" ", "_")
        else:
            self.last_file[0] = fn

        out_file = "%s-%s" % (self.first_file[0], self.last_file[0])
        
        self.time_taken[0] = time.time() - self.start_time[0]
        filesize = os.path.getsize("%s/%s" % (self.in_dir, self.temp_filename))

        linux_mac_cmd = "blender -b %s/%s -P statistics.py -- %s %s %f %d %d" % (self.in_dir, self.temp_filename, self.in_dir, out_file, self.time_taken[0], num_files, filesize)
        win_cmd = "blender.exe -b %s/%s -P statistics.py -- %s %s %f %d %d" % (self.in_dir, self.temp_filename, self.in_dir, out_file, self.time_taken[0], num_files, filesize)

        cmd = linux_mac_cmd if self.get_platform() == 'Linux' else win_cmd
        self.s_cont = self.execute_blender(cmd, capture_out=True)

        # Remove Temporary Output Blend (To Be Replaced by: '<First_Blend_File>-<Last_Blend_File>.blend')
        os.remove(os.path.join(self.in_dir, "%s" % self.temp_filename))


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

    def main(self):

        if not self.in_dir == None: #and self.is_file_vaild(self.in_dir):
            if ((len(self.in_files) == 0 and self.in_files == None)):
                # Using input directory for input files

                if (not self.out_dir == "" or not self.out_dir == None): #and self.is_file_vaild(self.out_dir):
                    # use output directory
                    print(self.out_dir)

                    if (not self.out_file == None or not self.out_file == "") and self.is_file_vaild(self.out_file):
                        # Vaild out file, use it.

                        if not self.limit == None or not self.limit <= 0:
                            # use limit

                            if not self.loop == None and self.loop:
                                # looping enabled.

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
                                # don't loop.

                                #------------------------------------
                                # RUN COMBINE TO ONCE
                                #------------------------------------

                                i = [0]
                                for file in os.listdir(self.in_dir):
                                    fe = os.path.splitext(file)[1]

                                    if fe == ".blend":
                                        self.combine_to(i[0], file, self.limit, once=True)

                                        i[0] += 1

                            if not self.stats == None and self.stats: 
                                # Print Stats
                                if not self.s_file == None or not self.s_file == "" and self.is_file_vaild(self.s_file):
                                    # use spcified stat file

                                    if not os.path.isfile(self.s_file):
                                        fo = open(self.s_file, "w")

                                        for line in str(self.s_cont[0]).split("\n"):
                                            fo.write(line + "\n")

                                        fo.close()

                                else:
                                    # use default stat file '<OUTPUT_FILE>_Stats.txt'
                                    self.s_file = "%s/%s_Stats.txt" % (self.in_dir, self.out_file)
                                    if not os.path.isfile(self.s_file):
                                        fo = open(self.s_file, "w")

                                        for line in str(self.s_cont).split("\n"):
                                            fo.write(line + "\n")

                                        fo.close()

                        else:
                            # don't use limit. combine all blend files in input directory.
                            i = [0]
                            for file in os.listdir(self.in_dir):
                                fe = os.path.splitext(file)[1]

                                num_files = len(os.listdir(self.in_dir))
                                if fe == ".blend":
                                    self.combine(i[0], file, num_files)

                                    i[0] += 1


                            #------------------------------------
                            # STATS
                            #------------------------------------

                            if not self.stats == None and self.stats: 
                                # Print Stats
                                if not self.s_file == None or not self.s_file == "" and self.is_file_vaild(self.s_file):
                                    # use spcified stat file

                                    if not os.path.isfile(self.s_file):
                                        fo = open(self.s_file, "w")

                                        for line in str(self.s_cont).split("\n"):
                                            fo.write(line + "\n")

                                        fo.close()

                                else:
                                    # use default stat file '<OUTPUT_FILE>_Stats.txt'
                                    self.s_file = "%s/%s_Stats.txt" % (self.in_dir, self.out_file)
                                    if not os.path.isfile(self.s_file):
                                        fo = open(self.s_file, "w")

                                        for line in str(self.s_cont).split("\n"):
                                            fo.write(line + "\n")

                                        fo.close()

                    else:
                        # use default output file '<FIRST_FILENAME>-<LAST_FILENAME>.blend'
                        self.out_file = "%s/%s" % (self.out_dir, self.out_file)
                else:
                    # DONT use output directory (default to input directory)
                    self.out_dir = self.in_dir
            else:
                # combining specific input files

                if (not self.out_dir == "" or not self.out_dir == None) and self.is_file_vaild(self.out_dir):
                    # use output directory

                    if (not self.out_file == None or not self.out_file == "") and self.is_file_vaild(self.out_file):
                        # Vaild out file, use it.

                        if not self.limit == None or not self.limit <= 0:
                            # use limit

                            if not self.loop == None and self.loop:
                                # looping enabled.

                                # parse in_files
                                in_file_array = shlex.split(self.in_files)

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
                                # don't loop.
                                
                                # parse in_files
                                in_file_array = shlex.split(num_files)

                                #------------------------------------
                                # RUN COMBINE TO ONCE
                                #------------------------------------

                                i = [0]
                                for file in in_file_array:
                                    fe = os.path.splitext(file)[1]

                                    if fe == ".blend":
                                        self.combine_to(i[0], file, self.limit, once=True)

                                        i[0] += 1

                            #------------------------------------
                            # STATS
                            #------------------------------------

                            if not self.stats == None and self.stats: 
                                # Print Stats
                                if not self.s_file == None or not self.s_file == "" and self.is_file_vaild(self.s_file):
                                    # use spcified stat file

                                    if not os.path.isfile(self.s_file):
                                        fo = open(self.s_file, "w")

                                        for line in str(self.s_cont).split("\n"):
                                            fo.write(line + "\n")

                                        fo.close()

                                else:
                                    # use default stat file '<OUTPUT_FILE>_Stats.txt'
                                    self.s_file = "%s/%s_Stats.txt" % (self.in_dir, self.out_file)
                                    if not os.path.isfile(self.s_file):
                                        fo = open(self.s_file, "w")

                                        for line in str(self.s_cont).split("\n"):
                                            fo.write(line + "\n")

                                        fo.close()

                        else:
                            # don't use limit. combine all blend files in input directory.

                            # parse in_files
                            in_file_array = shlex.split(self.in_files)

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
                            
                            #------------------------------------
                            # STATS
                            #------------------------------------

                            if not self.stats == None and self.stats: 
                                # Print Stats
                                if not self.s_file == None or not self.s_file == "" and self.is_file_vaild(self.s_file):
                                    # use spcified stat file

                                    if not os.path.isfile(self.s_file):
                                        fo = open(self.s_file, "w")

                                        for line in str(self.s_cont).split("\n"):
                                            fo.write(line + "\n")

                                        fo.close()

                                else:
                                    # use default stat file '<OUTPUT_FILE>_Stats.txt'
                                    self.s_file = "%s/%s_Stats.txt" % (self.in_dir, self.out_file)
                                    if not os.path.isfile(self.s_file):
                                        fo = open(self.s_file, "w")

                                        for line in str(self.s_cont).split("\n"):
                                            fo.write(line + "\n")

                                        fo.close()

                    else:
                        # use default output file '<FIRST_FILENAME>-<LAST_FILENAME>.blend'
                        self.out_file = "%s/%s" % (self.out_dir, self.out_file)
                else:
                    # DONT use output directory (default to input directory)
                    self.ut_dir = self.in_dir                    

        else:
            print("Error! Must Specify a Vaild Input Directory!")
            print("Filename was: %s" % self.in_dir)
            sys.exit(1)

if __name__ == "__main__":
    arg_list = sys.argv[1:]
    options = "hriIoOlLpP"
    long_options = "help run in_directory input_files output_file output_directory file_limit loop print_stats stats_filename".split(" ")
    
    c = combine_blend_files()

    try: 
        # Parse args
        args, values = getopt.getopt(arg_list, options, long_options) 
        
        #run_main = False

        # checking each argument 
        for currentArgument, currentValue in args:
    
            if currentArgument in ("-h", "--Help"): 
                print("usage: combine_blend_files.py [-h] [-r RUN] [-i INPUT_DIRECTORY] [-o OUTPUT_DIRECTORY]")
                print("")
                print("Description: ")
                print("A script to combine two or more Blender (.blend) files together.")
                print("")
                print("optional arguments: ")
                print("-h, --help\tshow help message and exit")
                print("-I, --input-filenames\tcombine specific blender files together.")
                print("-O, --output_filename\tthe name of the generated/combined output blend file (uses '<FIRST_FILENAME>-<LAST_FILENAME>.blend' by default).")
                print("-l, --file_limit\tthe number of blend files to combine from the specifed files (used to prevent very large output blend files).")
                print("-L, --loop\tcontinue combining blend file after file limit is reached until the last input file is processed (# OF OUTPUT BLENDS = # of INPUT BLENDS / FILE LIMIT)")
                print("-p, --print_stats\tprint the combine process results/statistics to a text file ('<OUTPUT_FILE>_Stats.txt' will be used as default).")
                print("-P, --stats_filename\tthe filename of the results/statistics text file (to be used in conjunction with the --print_stats command).")

            elif currentArgument in ("-i", "--in_directory"):
                c.in_dir = os.path.realpath(currentValue) + "/"
                
            elif currentArgument in ("-o", "--output_directory"): 
                c.out_dir = os.path.abspath(currentValue) + "/"

            elif currentArgument in ("-I", "--input_files"):
                c.in_files = currentValue
                
            elif currentArgument in ("-O", "--output_file"): 
                c.out_file = os.path.abspath(currentValue)

            elif currentArgument in ("-l", "--file_limit"):
                c.limit = int(currentValue)
                
            elif currentArgument in ("-L", "--loop"): 
                c.loop = True

            elif currentArgument in ("-p", "--print_stats"):
                c.stats = True
                
            elif currentArgument in ("-P", "--stats_filename"): 
                c.s_file = os.path.abspath(currentValue)

            elif currentArgument in ("-r", "--run"):

                # ---------------------------------------------------------------

                # TODO: Get combine_blend_files.py to run using Command line Arguments.
                
                # ---------------------------------------------------------------

                c.main() # NOT Working!
            
    except getopt.error as err: 
        # output error, and return with an error code 
        print (str(err))
        sys.exit(2)