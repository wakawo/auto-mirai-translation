import re
import argparse

def arg_parse():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
                        prog="main.py", 
                        usage="main.py -i input_file -o --output_file", 
                        add_help = True 
                        )

    parser.add_argument("-i", "--input_path", 
                        help = "Input file name.",
                        type = str,
                        required = True)

    parser.add_argument("-o", "--output_path",
                        help = "Output file name",
                        type = str,
                        default = "output.txt")
    
    args = parser.parse_args()
    return args


def formatter(input_path, output_path):
    pattern = r"^Abstract$|^\d\..*$"
    first = True

    with open(output_path, mode='w') as f:
        pass

    with open(output_path, mode='a') as out_file:
        with open(input_path) as in_file:
            for in_line in in_file:
                if re.match(pattern, in_line):
                    if(first):
                        first = False
                        out_file.write(in_line)
                    else:    
                        out_file.write('\n'+in_line)
                else:
                    out_file.write(in_line.replace('\n', ' '))
            out_file.write('\n')


if __name__=='__main__':   
    args = arg_parse() 
    formatter(input_path=args.input_path, output_path=args.output_path)

