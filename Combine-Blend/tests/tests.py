import os
import subprocess
import platform
import time
import resource
import sys

# Files and Directory Tests -------------------------------------

def test_dir_exists(dir):
    res = os.path.isdir(dir)
    msg = "Directory '%s' exists!" % dir if res else "Directory '%s' does not exist :(" % dir
    print(msg)
    
def test_file_exists(file):
    res = os.path.isfile(file)
    msg = "File '%s' exists!" % file if res else "File '%s' does not exist :(" % file
    print(msg)

def test_file_in_dir(file, dir):
    is_dir = os.path.isdir(dir)
    is_file = os.path.isfile(file)

    msg = ""

    if is_dir and is_file:
        for f in os.listdir(dir)
            if file == f:
                msg = "File '%s' found in Directory '%s'! ;)" % (file, dir)

        else
            msg = "File '%s' exists, but was not found in Directory '%s'! :O" % (file, dir)

    elif is_dir and not is_file:
        msg = "No File Called '%s' was Found! :(" % file
    elif not is_dir and is_file:
        msg = "No Directory Called '%s' was Found! :(" % dir
    else:
        msg = "No File '%s' and Directory '%s' was Found! :(" % (file, dir)

    print(msg)

def test_file_type(file, f_type):
    is_file = os.path.isfile(file)

    msg = ""

    if is_file:
        fn, fe = os.path.splitext(file)

        if fe == f_type:
            msg = "Yes, File '%s' is of Type: '%s'! ;)" % (file, f_type)
        else:
            msg = "No, sorry, File '%s' is not of Type '%s'! :(" % (file, f_type)
    else:
        msg = "File '%s' was not found or does not exist! :(" % file

    print(msg)

def test_vaild_filename(filename):

    invaid_tokens = "/ % * @ # > < ; | &".split(" ")

    msg = ""

    valid = True
    for t in invaid_tokens:
        if t in filename:
            valid = False

    if valid:
        msg = "Congrats, the Filename '%s' is Vaild!" % filename
    else:
        msg = "Sorry, the Filename '%s' is NOT Vaild!" % filename

    print(msg)

def test_num_files(dir, amount):
    is_dir = os.path.isdir(dir)

    msg = ""

    if is_dir:
        a = 0
        for f in os.listdir(dir):
            a += 1
        
        if amount == a:
            msg = "Yes, The Directory '%s' has %d Files in it." % (file, amount)
        else:
            msg = "Error, the amount specified '%d' does NOT match the amount of files (%d) in Directoy '%s'!" % (amount, a, dir)

    elif isdir and amount < 0:
        msg = "Directory '%s' found, but there is no such thing as a negative amount of files!" % dir
    elif not is_dir:
        msg = "Directory '%s' not found! :(" % dir

    print(msg)

# Filesize Tests

def test_filesize(file, size):
    msg = ""

    filesize = os.path.getsize(file)

    if filesize == size:
        msg = "Yes, The file '%s' has a filesize of %d Bytes!" % (file, size)
    else:
        msg = "No, the file '%s' is does NOT have a filesize of %d bytes! The actual filesize is %d Bytes" % (file, size, filesize)

    print(msg)

def test_filesize_unit(file, unit):
    msg = ""

    filesize = os.path.getsize(file)

    if unit == "B":
        if filesize < 1024:
            msg = "Yes, the file '%s' has a filesize in %s! The filesize is %d %s" % (file, unit, filesize, unit)
        else:
            msg = "No, the file '%s' does NOT have a filesize in %s!" % (file, unit)

    elif unit == "KB":
        if filesize >= 1024 and filesize < 1024000:
            msg = "Yes, the file '%s' has a filesize in %s! The filesize is %d %s" % (file, unit, filesize, unit)
        else:
            msg = "No, the file '%s' does NOT have a filesize in %s!" % (file, unit)
    
    elif unit == "MB":
        if filesize >= 1024000 and filesize < 1024000000:
            msg = "Yes, the file '%s' has a filesize in %s! The filesize is %d %s" % (file, unit, filesize, unit)
        else:
            msg = "No, the file '%s' does NOT have a filesize in %s!" % (file, unit)

    elif unit == "GB":
        if filesize >= 1024000000 and filesize < 1024000000000:
            msg = "Yes, the file '%s' has a filesize in %s! The filesize is %d %s" % (file, unit, filesize, unit)
        else:
            msg = "No, the file '%s' does NOT have a filesize in %s!" % (file, unit)

    elif unit == "TB":
        if filesize >= 1024000000000 and filesize < 1024000000000000:
            msg = "Yes, the file '%s' has a filesize in %s! The filesize is %d %s" % (file, unit, filesize, unit)
        else:
            msg = "No, the file '%s' does NOT have a filesize in %s!" % (file, unit)

    print(msg)

# -----------------------------------------------------------------------


# Processes Tests -------------------------------------------------------

def test_process_running(proc):

    msg = ""

    pid = proc.pid

    if not proc == None:
        try:
            os.kill(pid, 0)
        except OSError:
            msg = "Process with id: %d is NOT running!" % pid
        else:
            msg = "Process with id: %d is running!" % pid

    else:
        msg = "Process does NOT exist or is None! :(" 

    print(msg)


def test_process_has_errors(proc):

    msg = ""

    pid = proc.pid
    no_err = b''

    if not proc == None:
        try:
            res = proc.communicate(timeout=15)

            if not res[1] == no_err:
                msg = "There were NO errors when running th command: \n'%s'" % proc.args
            else:
                msg = "There were errors when running the command: \n'%s'\n\nThe error was: \n'%s'" % (proc.args, res[1])

        except TimeoutExpired:
            proc.kill()
            res = proc.communicate()
            msg = "The process with command: \n'%s'\nTimed Out!\nErrors were: \n'%s'" % (proc.args, res[1])

    else:
        msg = "Process does NOT exist or is None! :(" 

    print(msg)


def test_process_returncode(proc):
    msg = ""

    no_err = b''

    if not proc == None:
        try:
            res = proc.communicate(timeout=15)

            if not res[1] == no_err:
                msg = "The process returned with return code: %d" % proc.returncode
            else:
                msg = "The process returned with return code: %d and there were errors! Errors were: \n'%s'" & (proc.returncode, res[1])

        except TimeoutExpired:
            proc.kill()
            res = proc.communicate()
            msg = "The process Timed Out with reurn code: %d!\nErrors were: \n'%s'" % (proc.returncode, res[1])

    else:
        msg = "Process does NOT exist or is None! :(" 

    print(msg)

def test_process_run_time(cmd, timeout):
    msg = ""

    start = time.time()
    proc = subprocess.Popen(cmd)
    running = test_process_running(proc)

    if not running:
        time_taken = time.time() - start

        if time_taken <= 0:
            msg = "Process with command: \n'%s'\nDidn't even run! Weird. :O" % cmd
        else:
            msg = "Process with comand: '%s' took %d second(s) to complete!" % (cmd, time_taken)

    elif running:
        time_taken = 0
        while running:
            
            time_taken += 1
            time.sleep(1)

            if time_taken > timeout:
                msg = "Process with command: '%s' is taking over %d second(s) to run and may stil be running!" % (cm, timeout)
                break

    print(msg)


def test_kill_process(proc):

    msg = ""

    if not proc == None:
        cmd = proc.args

        is_running = test_process_running(proc)

        if is_running:
            proc.kill()
            is_running = test_process_running(proc)

            if not is_running:
                msg = "Process with comand '%s' has been terminated! :)" % cmd
            else:
                msg = "Process with command '%s' is still running for some reason. Weird. ;)" % cmd

        else:
            msg = "Process with command '%s' is NOT Running, Therefore it cannot be killed! :(" % cmd

    else:
        msg = "Process does NOT exist or is None! :(" 

    print(msg)
# -----------------------------------------------------------------------


# None Value Tests -------------------------------------------------------

def test_check_none(value):
    msg = ""

    if value == None:
        msg = "The value: %s is of type None! :(" % str(value)
    else:
        msg = "Congrats, the value: %s is NOT None! :)" % str(value)

    print(msg)

# -----------------------------------------------------------------------


# Looping Tests ---------------------------------------------------------

def test_index_bounds(index, min, max):

    msg = ""

    if index < min:
        msg = "Index: %d is less than the minimum value %d, thus it's out of bounds!" % (index, min)
    elif index > max:
        msg = "Index: %d is greater than the maximum value %d, thus it's out of bounds!" % (index, max)
    else:
        msg = "Index: %d is between %d and %d, good, it's within the bounds!" % (index, min, max)

    print(msg)

def test_negative_index(index):
    msg = ""
    
    if index < 0:
        msg = "Error! Index of %d is negative! Indices can't be negative. :O" % index
    else:
        msg = "Great! The index is positive, so it's a vaild index! :)" % index 

    print(msg)

def test_index_incrementing(index, max):
    
    msg = ""

    indices = []

    while index < max:
        indices.append(index)
        next = index + 1 if index + 1 < max else max

        if not index == next and next > index:
            msg = "Good, Index has incremented!"
        else:
            msg = "Index hasn't incremented! It's stuck at %d!" % index

    msg += "\nList of Indices: \n"

    for i in indices:
        msg += "%d, " % i

    print(msg)

def test_index_deincrementing(index, min = 0):
    
    msg = ""

    indices = []

    while index >= min:
        indices.append(index)
        prev = index - 1 if index - 1 >= min else min

        if not index == prev and prev < index:
            msg = "Good, Index has deincremented!"
        else:
            msg = "Index hasn't deincremented! It's stuck at %d!" % index

    msg += "\nList of Indices: \n"

    for i in indices:
        msg += "%d, " % i

    print(msg)

# -----------------------------------------------------------------------


# Calculation Tests -----------------------------------------------------

# Operating System Tests

def test_is_linux_32():
    msg = ""

    plat = platform.system()
    bits = platform.architecture[0]

    if plat == "Linux" and bits == "32":
        msg = "Great! Your Operating System is indeed a 32 Bit version of Linux!"
    else:
        msg = "No, your Operating System is NOT a 32 Bit version of Linux!"

    print(msg)

def test_is_linux_64():
    msg = ""

    plat = platform.system()
    bits = platform.architecture[0]

    if plat == "Linux" and bits == "64":
        msg = "Great! Your Operating System is indeed a 64 Bit version of Linux!"
    else:
        msg = "No, your Operating System is NOT a 64 Bit version of Linux!"

    print(msg)

def test_is_windows_32():
    msg = ""

    plat = platform.system()
    bits = platform.architecture[0]

    if plat == "Windows" and bits == "32":
        msg = "Great! Your Operating System is indeed 32 Bit Windows!"
    else:
        msg = "No, your Operating System is NOT 32 Bit Windows!"

    print(msg)

def test_is_windows_64():
    msg = ""

    plat = platform.system()
    bits = platform.architecture[0]

    if plat == "Windows" and bits == "64":
        msg = "Great! Your Operating System is indeed 64 Bit Windows!"
    else:
        msg = "No, your Operating System is NOT 64 Bit Windows!"

    print(msg)

def test_is_mac_32():
    msg = ""

    plat = platform.system()
    is_64bits = sys.maxsize > 2**32

    if plat == "Darwin" and not is_64bits:
        msg = "Great! Your Operating System is indeed a 32 Bit Mac!"
    else:
        msg = "No, your Operating System is NOT a 32 Bit Mac!"

    print(msg)

def test_is_mac_64():
    msg = ""

    plat = platform.system()
    is_64bits = sys.maxsize > 2**32

    if plat == "Darwin" and is_64bits:
        msg = "Great! Your Operating System is indeed a 64 Bit Mac!"
    else:
        msg = "No, your Operating System is NOT a 64 Bit Mac!"

    print(msg)

# Dictionary TestS

def test_is_dict_is_none(dict):
    msg = ""

    if not dict == None:
        msg = "The specified Dictionary does exists! Yay!"
    else:
        msg = "The specified Dictionary does NOT exist!"

    print(msg)

def test_is_dict_updated(dict, key, val):
    msg = ""

    if not dict == None:
        if key in dict:
            before = dict.get(key)
            dict.update(key = val)
            after = dict.get(key)

            if not before == after:
                msg = "Updated Dictionary key '%s' to '%s'!" % (key, val)
            else:
                msg = "Failed to update Dictionary key '%s' to '%s'! to key '%s' still has a value of '%s'." % (key, val, key, val)

        else:
            msg = "The Dictionary specifed does NOT have a key called '%s'!" % key
    else:
        msg = "The specified Dictionary does NOT exist!"

    print(msg)

def test_dict_has_key(dict, key):
    msg = ""

    if not dict == None:
        if key in dict:
            msg = "Good! The Dictionary specified has a key of '%s'.  The value of the key '%s' is %s." % (key, key, dict.get(key))
        else:
            msg = "The Dictionary specifed does NOT have a key called '%s'!" % key
    else:
        msg = "The specified Dictionary does NOT exist!"

    print(msg)

def test_dict_has_value(dict, value):
    msg = ""

    if not dict == None:
       for keys in dict.keys():
            key_val = dict.get(key)

            if key_val == value:
                msg = "Yes, the dictionary specified has a key with the value of '%s'! The key is called '%s'." % (value, key)
            else:
                msg = "No, the specified dictionary does NOT have any value of '%s'!" % value
    else:
        msg = "The specified Dictionary does NOT exist!"

    print(msg)

def test_dict_key_has_val(dict, key, val):
    msg = ""

    if not dict == None:
        if key in dict:
            key_val = dict.get(key)

            if val == key_val:
                msg = "Yes, in the dictionary specified, the key '%s' has a value of '%s'!" % (key, val)
            else:
                msg = "No, in the dictionary specified, the key '%s' isn't a value of '%s'!" % (key, val)
        else:
            msg = "The Dictionary specifed does NOT have a key called '%s'!" % key
    else:
        msg = "The specified Dictionary does NOT exist!"

    print(msg)


# -----------------------------------------------------------------------


# Blender Specific Tests ------------------------------------------------



# -----------------------------------------------------------------------

