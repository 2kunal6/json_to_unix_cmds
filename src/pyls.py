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


def print_format(files, args):
    output_list = []
    for file in files:
        output_list.append([file['permissions'], file['size'], file['time_modified'], file['name']])

    output_list.sort(key=lambda x:x[3])
    if('-t' in args):
        output_list.sort(key=lambda x: x[2])

    if('-r' in args):
        output_list.reverse()

    if('-h' in args):
        for val in output_list:
            val[1] = convert_size(val[1])

    print(output_list)


def ls(all_required):
    filename_list = []
    for filename in json_as_dict['contents']:
        if(all_required == True):
            filename_list.append(filename)
        else:
            if(filename['name'][0]!='.'):
                filename_list.append(filename)

    return filename_list


def get_filtered_files(all_files, arg):
    filtered_files = []
    for a_file in all_files:
        if(arg == '--filter=dir'):
            if('contents' in a_file):
                filtered_files.append(a_file)
        if (arg == '--filter=file'):
            if ('contents' not in a_file):
                filtered_files.append(a_file)
        return filtered_files


def get_required_files():
    if ('-A' in sys.argv):
        all_files = ls(True)
    else:
        all_files = ls(False)

    for arg in sys.argv:
        if (arg.startswith('--filter=')):
            if (('--filter=dir' in arg) or ('--filter=file' in arg)):
                all_files = get_filtered_files(all_files, arg)
            else:
                provided_name = arg.replace('--filter=')
                print(
                    f"error: '{provided_name}' is not a valid filter criteria. Available filters are 'dir' and 'file'")
                return

    return all_files
    '''
    for arg in sys.argv:
        if (arg[0] != '-'):
            for '''



def main():
    global json_as_dict
    json_as_dict = read_json_as_dict()

    required_files = get_required_files()

    print_format(required_files, sys.argv)



if __name__ == '__main__':
    main()