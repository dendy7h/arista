'''
1. Use Arista's eAPI to obtain 'show interfaces' from the switch.  Parse the
'show interfaces' output to obtain the 'inOctets' and 'outOctets' fields for
each of the interfaces on the switch.  Accomplish this directly using
jsonrpclib.

'''


from jsonrpclib import Server

user = 'user'
passwd = 'passwd'
host = 'ip.addr'
port = 8543


class Arista_Sw(object):
    '''
        Takes username, password, hostname and port (default = 22) as inputs
    '''
    def __init__(self, un, pw, hn, p=22):
        self.url = "https://{}:{}@{}:{}/command-api".format(un, pw, hn, p)
        self.interfaces = {}

    def run_cmd(self, cmd):
        '''
            Runs the command on the switch and returns the results
        '''
        self.sw = Server(self.url)
        return self.sw.runCmds(1, cmd)

    def int_oct(self):
        '''
            Parse the 'show interfaces' output to obtain the 'inOctets' and
            'outOctets' fields for each of the interfaces on the switch.
        '''
        output = self.run_cmd(['show interfaces'])[0]

        for int in output['interfaces'].itervalues():
            try:
                name = int['name']
                inOct = int['interfaceCounters']['inOctets']
                outOct = int['interfaceCounters']['outOctets']

                yield(name, inOct, outOct)

            except KeyError:
                pass


pynet4 = Arista_Sw(user, passwd, host, port)

for name, inOct, outOct in pynet4.int_oct():
    print "Interface: {}\n\tinOctets: {}\n\toutOctets: {}".format(name, inOct, outOct)
