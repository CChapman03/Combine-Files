import os

def main():
    f_dir = "../txt/"

    num_files = 0
    for f in os.listdir(f_dir):
        fn, fe = os.path.splitext(f)
        if os.path.isfile(f) and fe == '.txt':
            num_files += 1

    first_file = os.listdir(f_dir)[0].split(".")[0]
    last_file = os.listdir(f_dir)[num_files].split(".")[0]

    out_f_name = first_file.join("-").join(last_file)

    for file in os.listdir(f_dir):

        fn, fe = os.path.splitext(file)
        if os.path.isfile(file) and fe == '.txt':

            out_f = open(out_f_name.join(".txt"), 'a')
            
            f = open(file, 'r')

            out_f.write(file + ": \n")
            out_f.write("-----------------------\n\n")
            for line in f.readlines():
                out_f.write(line + "\n")
            out_f.write("\n-----------------------\n\n")

            out_f.close()
            f.close()

main()