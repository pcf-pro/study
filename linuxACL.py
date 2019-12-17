r"""
Usage example
for help
$ python linuxACL.py -h
"""

import argparse
import os
import re


def create(file):  # create file
    os.system('>' + file)
    print('File ' + file + ' is create!')


def sets(name, permission, file):  # set permission
    temps = os.popen('sudo useradd ' + name)
    if temps.read() is not None:  # check new user
        os.system('setfacl -m u:' + name + ':' + permission + ' ' + file)
        print('Sucsessful!')
    else:
        print('User ' + name + ' create')
        os.system('setfacl -m u:' + name + ':' + permission + ' ' + file)
        print('Sucsessful!')


def pars(file):  # parsing
    diction = {}
    temp = os.popen('getfacl ' + file).read().split('\n')  # temp string
    for i in temp:
        if '# file:' in i:  # name file
            diction['name_file'] = i[8:]
        if '# owner' in i:
            diction[i[9:]] = [j[6:] for j in temp if 'user::' in j]  # name  + permission
            temps = os.popen('grep ' + i[9:] + ' /etc/passwd').read()
            diction[i[9:]].append(
                re.findall(r':\d+:', os.popen('grep ' + i[9:] + ' /etc/passwd').read())[0].replace(':',
                                                                                                   ''))  # name users
            diction[i[9:]].append(temps[temps[:temps.index(',,,')].rindex(':') + 1:temps.index(',,,')])  # gecos
        if '# group' in i:
            if i[9:] not in diction.keys():  # check users on diction
                diction[i[9:]] = [j[7:] for j in temp if 'group::' in j]  # name group + permission
                diction[i[9:]].append(
                    re.findall(r':\d+:', os.popen('grep ' + i[9:] + ': /etc/group').read())[0].replace(':', ''))

        if 'user:' in i and i[5:] not in diction and 'user::' not in i:
            temps = os.popen('grep ' + i[5:i.rindex(':')] + ' /etc/passwd').read()
            if i[5:i.rindex(':')] not in diction.keys():  # check users
                diction[i[5:i.rindex(':')]] = [i[i.rindex(':') + 1:]]  # name + permission
                diction[i[5:i.rindex(':')]].append(
                    re.findall(r':\d+:', os.popen('grep ' + i[5:i.rindex(':')] + ' /etc/passwd').read())[0].replace(':',
                                                                                                                    ''))  # uin
                try:
                    diction[i[5:i.rindex(':')]].append(
                        temps[temps[:temps.index(',,,')].rindex(':') + 1:temps.index(',,,')])  # gecos
                except:
                    continue

    print(diction)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parsing ACL',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-c', "--create", required=False, action="store_true",
                        help='Create file with rule')
    parser.add_argument("-s", "--sets", required=False, action="store_true", help='set rule')
    parser.add_argument('-p', '--pars', required=False, action='store_true',
                        help='Parsing and print')
    parser.add_argument('-f', '--file', required=False, type=str, default='file',
                        help='additional params. That file is create (-c=words.dot or --create --file=words.pdf)')
    parser.add_argument('-n', '--name', required=False, type=str, default='adinim',
                        help='additional params name of user, permission, file(-s -n=Den -pr=rw- -f=file.txt or--set --name=Denis --permission=rw- --file=file.txt ')
    parser.add_argument('-pr', '--permission', required=False, type=str, default='rw-',
                        help='permission for user (--set --permission=rwx')
    args = parser.parse_args()

    if args.create:
        create(args.file)

    elif args.sets:
        sets(args.name, args.permission, args.file)
    elif args.pars:
        pars(args.file)
