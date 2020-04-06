from dataclasses import dataclass

# ----------------------------------------

# Currently NOT used!

#-----------------------------------------

@dataclass
class FileData:
    temp_filename: str = "output.blend"
    input_filename: str = ""
    input_directory: str = ""
    output_filename: str = ""
    input_file_size: int = 0
    output_file_size: int = 0

    def __str__(self):
        return "{'temp_filename' : %s, 'input_filename' : %s, 'input_directory' : %s, 'output_filename' : %s, 'input_file_size' : %d, 'output_file_size' : %d}" % (self.temp_filename, self.input_filename, self.input_directory, self.output_filename, self.input_file_size, self.output_file_size)

    def get_temp_filename(self):
        return self.temp_filename
    def set_temp_filename(self, temp_filename):
        self.temp_filename = temp_filename

    def get_input_filename(self):
        return self.input_filename
    def set_input_filename(self, input_filename):
        self.input_filename = input_filename

    def get_input_directory(self):
            return self.input_filename
    def set_input_directory(self, input_directory):
        self.input_directory = input_directory

    def get_output_filename(self):
            return self.output_filename
    def set_output_filename(self, output_filename):
        self.output_filename = output_filename

    def get_input_file_size(self):
            return self.input_file_size
    def set_input_file_size(self, input_file_size):
        self.input_file_size = input_file_size

    def get_output_file_size(self):
            return self.output_file_size
    def set_output_file_size(self, output_file_size):
        self.output_file_size = output_file_size

@dataclass
class StatData:
    time_taken: int = 0
    num_files_processed: int = 0

    def __str__(self):
        return "{'time_taken' : %d, 'num_files_processed' : %d}" % (self.time_taken, self.num_files_processed)

    def get_time_taken(self):
        return self.time_taken
    def set_time_taken(self, time_taken):
        self.time_taken = time_taken
    
    def get_num_files_processed(self):
        return self.num_files_processed
    def set_num_files_processed(self, num_files_processed):
        self.num_files_processed = num_files_processed

f_data = FileData()
s_data = StatData()