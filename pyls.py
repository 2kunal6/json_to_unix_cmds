from datetime import datetime

import argparse
import math
import json
import sys

json_as_dict = {}

def read_json_as_dict():
    json_file = open('structure.json')
    json_str = json_file.read()
    json_dict = json.loads(json_str)
    return json_dict


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0"
   size_name = ("", "K", "M", "G", "T", "P", "E", "Z", "Y")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s%s" % (s, size_name[i])


def print_l_format(matrix):
    col_widths = [max(len(str(item)) for item in col) for col in zip(*matrix)]

    # Print each row with formatted columns
    for row in matrix:
        formatted_row = []
        for i, cell in enumerate(row):
            if i == 0 or i == len(row) - 1:  # Left-most and right-most columns
                formatted_row.append(f"{str(cell):<{col_widths[i]}}")  # Left-align
            else:  # Middle columns
                formatted_row.append(f"{str(cell):>{col_widths[i]}}")  # Right-align
        print("  ".join(formatted_row))


def print_format(files, args):
    output_list = []
    for file in files:
        output_list.append([file['permissions'], file['size'], file['time_modified'], file['name']])

    output_list.sort(key=lambda x:x[3])

    if(args.t):
        output_list.sort(key=lambda x: x[2])

    if(args.r):
        output_list.reverse()

    if(args.h):
        for val in output_list:
            val[1] = convert_size(val[1])

    for val in output_list:
        val[2] = datetime.fromtimestamp(val[2]).strftime('%b %d %H:%M')

    if(args.l):
        print_l_format(output_list)
    else:
        only_names = []
        for row in output_list:
            only_names.append(row[3])
        print(*only_names)



def ls(all_required, file_filter):
    filename_list = []
    all_files = []
    if(len(file_filter)>0):
        file_filter = file_filter[0]
        if('/' in file_filter):
            full_path = file_filter.split('/')
            curr = json_as_dict
            for i in range(len(full_path)):
                is_found = False
                for val in curr['contents']:
                    if(full_path[i] == val['name']):
                        curr=val
                        is_found = True
                        if(i==len(full_path)-1):
                            return [val]
                if(is_found == False):
                    print(f"error: cannot access '{file_filter}': No such file or directory")
                    sys.exit()
        else:
            for val in json_as_dict['contents']:
                if(val['name'] == file_filter[0]):
                    all_files = val['contents']
    else:
        all_files = json_as_dict['contents']

    for filename in all_files:
        if(all_required == True):
            filename_list.append(filename)
        else:
            if(filename['name'][0]!='.'):
                filename_list.append(filename)

    return filename_list


def get_filtered_files(all_files, arg):
    filtered_files = []
    for a_file in all_files:
        if(arg == 'dir'):
            if('contents' in a_file):
                filtered_files.append(a_file)
        if (arg == 'file'):
            if ('contents' not in a_file):
                filtered_files.append(a_file)
    return filtered_files


def get_required_files(args, file_filter):
    all_required = False
    if (args.A):
        all_required = True
    all_files = ls(all_required, file_filter)

    if ((args.filter=='dir') or (args.filter=='file')):
        all_files = get_filtered_files(all_files, args.filter)
    else:
        if(args.filter is not None):
            print(f"error: '{args.filter}' is not a valid filter criteria. Available filters are 'dir' and 'file'")
            sys.exit()

    return all_files

def set_and_get_argparse_values():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-A', action='store_true', help='show hidden files starting with .')
    parser.add_argument('-t', action='store_true', help='sort by timestamp modified')
    parser.add_argument('-r', action='store_true', help='reverse sort the result')
    parser.add_argument('-h', action='store_true', help='show the file/folder sizes in human readable format')
    parser.add_argument('--help', action="help")
    parser.add_argument('-l', action='store_true', help='show details')
    parser.add_argument('--filter', help='filter directory or files')

    args, file_filter = parser.parse_known_args()
    return args, file_filter


def main():
    global json_as_dict
    json_as_dict = read_json_as_dict()

    args, file_filter = set_and_get_argparse_values()

    required_files = get_required_files(args, file_filter)

    print_format(required_files, args)



if __name__ == '__main__':
    main()