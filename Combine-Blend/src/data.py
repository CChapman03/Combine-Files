# data structs
file_data = {"temp_filename" : "output.blend", "output_filename" : "", "input_filename" : "", "input_directory" : "", "input_file_size" : 0, "output_file_size" : 0}
stat_data = {"time_taken" : 0, "num_files_processed" : 0}

def update_data(data_dict, data_key, new_val):
    if not data_dict == None:
        data_dict.update(data_key = new_val)
    else:
        print("Error! Could NOT get data from specified Dictionary! Dictionary does NOT exist! NOT Updating key '%s' with value '%s'" % (data_key, new_val))
        return

def append_data(data_dict, data_key, val):
    if not data_dict == None:
        if not data_key in data_dict.keys():
            data_dict[data_key] = val
        else:
            print("Error! Could NOT Append key '%s' with value '%s'! Key '%s' already exists in specified Dictionary!" % (data_key, val, data_key))
    else:
        print("Error! Could NOT get data from specified Dictionary! Dictionary does NOT exist! NOT Appending key '%s' with value '%s'" % (data_key, val))
        return

def get_data(data_dict, data_key):
    if not data_dict == None:
        if data_key in data_dict.keys():
            val = data_dict.get(data_key)
            return val
        else:
            print("Error! The Dictionary specified has NO key called '%s'! Returning a value of None." % data_key)
            return None
    else:
        print("Error! Could NOT get data from specified Dictionary! Dictionary does NOT exist! Returning a value of None.")
        return None