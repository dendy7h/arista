'''
2. Using Arista's eapilib, create a script that allows you to add a VLAN (both
the VLAN ID and the VLAN name).  Your script should first check that the VLAN ID
is available and only add the VLAN if it doesn't already exist.  Use VLAN IDs
between 100 and 999.  You should be able to call the script from the command
line as follows:

   python eapi_vlan.py --name blue 100     # add VLAN100, name blue

If you call the script with the --remove option, the VLAN will be removed.

   python eapi_vlan.py --remove 100          # remove VLAN100

Once again only remove the VLAN if it exists on the switch.  You will probably
want to use Python's argparse to accomplish the argument processing.

Note, in the lab environment, if you want to directly execute your script, you
will need to use '#!/usr/bin/env python' at the top of the script (instead of
'!#/usr/bin/python').
'''

import eapilib
import sys
import getopt

DEBUG = True
sw4_params = {'username': 'user',
              'password': 'passwd',
              'hostname': 'ip.addr',
              'port': 8543
             }
help_message = '''
USAGE:
    python eapi_vlan.py --name blue 100     # add VLAN100, name blue
    python eapi_vlan.py --remove 100          # remove VLAN100
    python eapi_vlan.py 200     # add VLAN200, name VLAN200

OPTIONS:
    -h, --help                  display help
    -n, --name                  adds vlan
    -r, --remove                removes vlan

DEFAULT:
    Default adds the vlan
'''


class Arista_Sw(object):
    '''
       uses eapilib connections object to create add/delete vlan methods
    '''
    def __init__(self, **kwargs):
        self.connection = eapilib.create_connection(**kwargs)
        self.vlans = {}

    def add_vlan(self, vlan_num, vlan_name=None):
        '''
            get all the vlans, add the vlan if not listed

        '''
        if not vlan_name:
            vlan_name = 'VLAN{}'.format(vlan_num)

        self.vlans = self.connection.run_commands(['show vlan']).pop()
        vlan_list = self.vlans['vlans'].keys()
        if str(vlan_num) not in vlan_list:
            command = ['vlan {}'.format(vlan_num), 'name {}'.format(vlan_name)]
            output = self.connection.config(command)
            if DEBUG:
                print output
        else:
            if DEBUG:
                print 'vlan {} is already here'.format(vlan_num)
            return 'vlan {} is already here'.format(vlan_num)

    def remove_vlan(self, vlan_num):
        '''
            get all the vlans, del the vlan if listed

        '''
        self.vlans = self.connection.run_commands(['show vlan']).pop()
        vlan_list = self.vlans['vlans'].keys()
        if str(vlan_num) in vlan_list:
            command = ['no vlan {}'.format(vlan_num)]
            output = self.connection.config(command)
            if DEBUG:
                print output
        else:
            if DEBUG:
                print 'vlan {} is not here'.format(vlan_num)
            return 'vlan {} is not here'.format(vlan_num)


def verify_vlan(vlan):
    '''
        Verifies a vlan is a number in the range of 1 to 4096
    '''
    while True:
        if not vlan.isdigit():
            print "Vlan provided is not an integer"
            sys.exit()
        elif int(vlan) <= 1:
            print "VLAN ID must be greater than 1 and less than 4096"
            sys.exit()
        elif int(vlan) >= 4096:
            print "VLAN ID must be greater than 1 and less than 4096"
            sys.exit()
        else:
            return True


def get_options():
    '''
        gets the command line arguments and parses through them returning
        vlan id and vlan name
    '''
    if len(sys.argv) < 2:
        print help_message
        sys.exit()
    try:
        # getopt : and = means the argument is required
        opts, args = getopt.getopt(sys.argv[1:], "hrn:", ['help', 'name=', 'remove'])
        if DEBUG:
            print 'Options: {}'.format(opts)
            print 'Args: {}'.format(args)
    except getopt.GetoptError, err:
        print str(err)
        print help_message
        sys.exit()

    vlan_name = None
    vlan_id = args.pop()

    verify_vlan(vlan_id)

    for o, a in opts:
        if o in ("-n", '--name'):
            vlan_name = a
        elif o in ("-r", 'remove'):
            vlan_name = 'remove'
        elif o in ("-h"):
            print help_message
            sys.exit()
        else:
            assert False, "unhandled option"

    return(vlan_id, vlan_name)


def main():
    vlan_id, vlan_name = get_options()
    pynet4 = Arista_Sw(**sw4_params)
    if vlan_name == 'remove':
        pynet4.remove_vlan(vlan_id)
    else:
        pynet4.add_vlan(vlan_id, vlan_name)


if __name__ == '__main__':
    main()
