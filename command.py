import sys

from Command.Command import CommandBuilder

commandBuilder = CommandBuilder()
params = {}
for argv in sys.argv:
    a = str(argv).split('=')
    if len(a) >= 2:
        params[a[0]] = a[1]
if '--run' in params:
    c = commandBuilder.get_command(params['--run'])
    if c is not None:
        print('Running with command %s ...' % params['--run'])
        print(c.exec(params))
