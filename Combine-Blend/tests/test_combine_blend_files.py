import os
import subprocess
import platform
import time
import resource
import sys

def execute_comine_blend_files(cmd, time_limit = 60*5, stop = False, capture_out = False):

    # Create Log Files Per Subprocess

    out = open("logs/out.txt", "w")
    err = open("logs/err.txt", "w")

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

def test_args(args):
    execute_comine_blend_files(args)
    passed = True

    err = open("logs/err.txt", 'r')
    out = open("logs/out.txt", 'r')

    if len(err.readlines()) > 0:
        passed = False

    err.close()
    out.close()

    return passed


def main():
    tests = []

    # -h and --help
    tests.append({"print_help" : test_args("cd ../src/ && python combine_blend_files.py -h") and test_args("cd ../src/ && python combine_blend_files.py --help")})
    
    # -i
    tests.append({"input_directory_exists" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/")})
    tests.append({"input_directory_does_NOT_exist" : not test_args("cd ../src/ && python combine_blend_files.py -i ../does/NOT/exist/")})
    tests.append({"input_directory_with_spaces" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/my blends/")})
    tests.append({"input_directory_not_provided" : not test_args("cd ../src/ && python combine_blend_files.py -i")})
    tests.append({"input_directory_none" : not test_args("cd ../src/ && python combine_blend_files.py -i ")})
    tests.append({"input_directory_valid" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/")})
    tests.append({"input_directory_NOT_valid" : not test_args("cd ../src/ && python combine_blend_files.py -i with/w!@rd//ch#r$/")})

    # -I
    tests.append({"input_filenames_exist" : test_args("cd ../src/ && python combine_blend_files.py -I ../tests/blends/Blahh.blend ../tests/blends/Cool.blend")})
    tests.append({"input_filenames_do_NOT_exist" : not test_args("cd ../src/ && python combine_blend_files.py -I does/not/exist.blend ../tests/blends/Cool.blend")})
    tests.append({"input_filenames_with_spaces" : test_args("cd ../src/ && python combine_blend_files.py -I blends/Nuts N Bolts.blend blends/Treee_Scene.blend")})
    tests.append({"input_filenames_not_provided" : not test_args("cd ../src/ && python combine_blend_files.py -I")})
    tests.append({"input_filenames_none" : not test_args("cd ../src/ && python combine_blend_files.py -I ")})
    tests.append({"input_filenames_valid" : test_args("cd ../src/ && python combine_blend_files.py -I ../tests/blends/Blahh.blend ../tests/blends/Cool.blend")})
    tests.append({"input_filenames_NOT_valid" : not test_args("cd ../src/ && python combine_blend_files.py -I /with/w!@rd//ch#r$/,blend ../test/blends/Blahh.blend")})
    tests.append({"input_filenames_from_different_directories" : test_args("cd ../src/ && python combine_blend_files.py -I ../tests/blends/Blahh.blend blends/Default_Blend.blend")})
    tests.append({"input_filenames_no_file_extension" : test_args("cd ../src/ && python combine_blend_files.py -I ../tests/blends/Blahh ../tests/blends/Cool.blend")})
    tests.append({"input_filenames_only_one_filename" : not test_args("cd ../src/ && python combine_blend_files.py -I ../tests/blends/Cool.blend")})

    # -o
    tests.append({"output_directory_exists" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -o ../")})
    tests.append({"output_directory_does_NOT_exist" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -o ../does/not/exist/")})
    tests.append({"output_directory_with_spaces" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -o ../tests/blends/my blends/")})
    tests.append({"output_directory_not_provided" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -o")})
    tests.append({"output_directory_none" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -o ")})
    tests.append({"output_directory_valid" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -o ../")})
    tests.append({"output_directory_NOT_valid" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -o with/w!@rd//ch#r$/")})

    # -O
    tests.append({"output_filename_with_spaces" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -O my output blend.blend")})
    tests.append({"output_filename_not_provided" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -O")})
    tests.append({"output_filename_none" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -O ")})
    tests.append({"output_filename_valid" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -O output.blend")})
    tests.append({"output_filename_NOT_valid" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -O w!@rd.out.blend")})
    tests.append({"output_filename_no_file_extension" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -O out")})
    tests.append({"output_filename_multiple_filenames" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -O out.txt output2.txt")})
    

    # -l
    tests.append({"file_limit_zero" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -l 0")})
    tests.append({"file_limit_not_provided" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -l")})
    tests.append({"file_limit_none" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -l ")})
    tests.append({"file_limit_negative" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -l -1")})
    tests.append({"file_limit_valid" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -l 2")})
    tests.append({"file_limit_NOT_valid" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -l a")})
    tests.append({"file_limit_multiple_values" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -l 2 5")})
    tests.append({"file_limit_greater_then_num_input_files" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -l %d" % len(os.listdir("../tests/blends/") + 1))})

    # -L
    tests.append({"loop_valid" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -l 1 -L")})
    tests.append({"loop_without_file_limit" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -L")})
    tests.append({"loop_value_provided" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -l 1 -L 1")})
    tests.append({"loop_none_value_provided" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -l 1 -L ")})
    tests.append({"loop_bool_value_provided" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -l 1 -L True")})

    # -p
    tests.append({"print_stats_valid" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -p")})
    tests.append({"print_stats_value_provided" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -p yes")})
    tests.append({"print_stats_none_value_provided" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -p ")})
    tests.append({"print_stats_bool_value_provided" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -p True")})

    # -P
    tests.append({"stats_filename_with_spaces" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -p -P my stats.txt")})
    tests.append({"stats_filename_not_provided" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -p -P")})
    tests.append({"stats_filename_none" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -p -P ")})
    tests.append({"stats_filename_valid" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -p -P stats.txt")})
    tests.append({"stats_filename_NOT_valid" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -p -P w!@rd.stats.txt")})
    tests.append({"stats_filename_no_file_extension" : test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -p -P stats")})
    tests.append({"stats_filename_without_print_stats" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -P stats.txt")})
    tests.append({"stats_filename_multiple_filenames" : not test_args("cd ../src/ && python combine_blend_files.py -i ../tests/blends/ -p -P stats.txt stats2.txt")})
    

    # --input_directory
    tests.append({"input_directory_exists" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/")})
    tests.append({"input_directory_does_NOT_exist" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../does/NOT/exist/")})
    tests.append({"input_directory_with_spaces" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/my blends/")})
    tests.append({"input_directory_not_provided" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory")})
    tests.append({"input_directory_none" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ")})
    tests.append({"input_directory_valid" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/")})
    tests.append({"input_directory_NOT_valid" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory with/w!@rd//ch#r$/")})

    # --input_filenames
    tests.append({"input_filenames_exist" : test_args("cd ../src/ && python combine_blend_files.py --input_filenames ../tests/blends/Blahh.blend ../tests/blends/Cool.blend")})
    tests.append({"input_filenames_do_NOT_exist" : not test_args("cd ../src/ && python combine_blend_files.py --input_filenames does/not/exist.blend ../tests/blends/Cool.blend")})
    tests.append({"input_filenames_with_spaces" : test_args("cd ../src/ && python combine_blend_files.py --input_filenames blends/Nuts N Bolts.blend blends/Treee_Scene.blend")})
    tests.append({"input_filenames_not_provided" : not test_args("cd ../src/ && python combine_blend_files.py --input_filenames")})
    tests.append({"input_filenames_none" : not test_args("cd ../src/ && python combine_blend_files.py --input_filenames ")})
    tests.append({"input_filenames_valid" : test_args("cd ../src/ && python combine_blend_files.py --input_filenames ../tests/blends/Blahh.blend ../tests/blends/Cool.blend")})
    tests.append({"input_filenames_NOT_valid" : not test_args("cd ../src/ && python combine_blend_files.py --input_filenames /with/w!@rd//ch#r$/,blend ../test/blends/Blahh.blend")})
    tests.append({"input_filenames_from_different_directories" : test_args("cd ../src/ && python combine_blend_files.py --input_filenames ../tests/blends/Blahh.blend blends/Default_Blend.blend")})
    tests.append({"input_filenames_no_file_extension" : test_args("cd ../src/ && python combine_blend_files.py --input_filenames ../tests/blends/Blahh ../tests/blends/Cool.blend")})
    tests.append({"input_filenames_only_one_filename" : not test_args("cd ../src/ && python combine_blend_files.py --input_filenames ../tests/blends/Cool.blend")})

    # --output_directory
    tests.append({"output_directory_exists" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_directory ../")})
    tests.append({"output_directory_does_NOT_exist" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_directory ../does/not/exist/")})
    tests.append({"output_directory_with_spaces" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_directory ../tests/blends/my blends/")})
    tests.append({"output_directory_not_provided" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_directory")})
    tests.append({"output_directory_none" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_directory ")})
    tests.append({"output_directory_valid" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_directory ../")})
    tests.append({"output_directory_NOT_valid" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_directory with/w!@rd//ch#r$/")})

    # --output_filename
    tests.append({"output_filename_with_spaces" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_filename my output blend.blend")})
    tests.append({"output_filename_not_provided" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_filename")})
    tests.append({"output_filename_none" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_filename ")})
    tests.append({"output_filename_valid" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_filename output.blend")})
    tests.append({"output_filename_NOT_valid" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_filename w!@rd.out.blend")})
    tests.append({"output_filename_no_file_extension" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_filename out")})
    tests.append({"output_filename_multiple_filenames" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --output_filename out.txt output2.txt")})
    

    # --file_limit
    tests.append({"file_limit_zero" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --file_limit 0")})
    tests.append({"file_limit_not_provided" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --file_limit")})
    tests.append({"file_limit_none" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --file_limit ")})
    tests.append({"file_limit_negative" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --file_limit -1")})
    tests.append({"file_limit_valid" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --file_limit 2")})
    tests.append({"file_limit_NOT_valid" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --file_limit a")})
    tests.append({"file_limit_multiple_values" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --file_limit 2 5")})
    tests.append({"file_limit_greater_then_num_input_files" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --file_limit %d" % len(os.listdir("../tests/blends/") + 1))})

    # --loop
    tests.append({"loop_valid" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --file_limit 1 --loop")})
    tests.append({"loop_without_file_limit" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --loop")})
    tests.append({"loop_value_provided" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --file_limit 1 --loop 1")})
    tests.append({"loop_none_value_provided" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --file_limit 1 --loop ")})
    tests.append({"loop_bool_value_provided" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --file_limit 1 --loop True")})

    # --print_stats
    tests.append({"print_stats_valid" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --print_stats")})
    tests.append({"print_stats_value_provided" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --print_stats yes")})
    tests.append({"print_stats_none_value_provided" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --print_stats ")})
    tests.append({"print_stats_bool_value_provided" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --print_stats True")})

    # --stats_filename
    tests.append({"stats_filename_with_spaces" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --print_stats --stats_filename my stats.txt")})
    tests.append({"stats_filename_not_provided" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --print_stats --stats_filename")})
    tests.append({"stats_filename_none" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --print_stats --stats_filename ")})
    tests.append({"stats_filename_valid" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --print_stats --stats_filename stats.txt")})
    tests.append({"stats_filename_NOT_valid" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --print_stats --stats_filename w!@rd.stats.txt")})
    tests.append({"stats_filename_no_file_extension" : test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --print_stats --stats_filename stats")})
    tests.append({"stats_filename_without_print_stats" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --stats_filename stats.txt")})
    tests.append({"stats_filename_multiple_filenames" : not test_args("cd ../src/ && python combine_blend_files.py --input_directory ../tests/blends/ --print_stats --stats_filename stats.txt stats2.txt")})

    num_passed = 0
    num_failed = 0
    for test in tests:
        for key, val in test.items():
            s = "%s %s" % (key, "Passed!" if val else "Failed!")
            print(s)
            num_passed += 1 if val else 0
            num_failed += 1 if not val else 0
            f = open("tests.txt", 'w')
            f.write("Running Tests for: combine_blend_files.py\n")
            f.write("----------------------------------------------\n\n")
            f.write("Test: %s\n" % s)
            f.write("----------------------------------------------\n")
            f.write("Number of Tests Passed: %d\n" % num_passed)
            f.write("Number of Tests Failed: %d\n" % num_failed)
            f.write("----------------------------------------------\n")
            f.write("Yay! All the Tests Passed! combine_blend_files.py is ready for Production Use!" if len(num_failed) == 0 else "Sorry! Some of the Tests Failed. combine_blend_files.py is NOT ready for Production Use yet.")
            f.close()


main()