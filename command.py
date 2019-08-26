from Command.Command import CommandBuilder
from CrawlerLib.helper import get_sys_params

commandBuilder = CommandBuilder()
params = get_sys_params()
if '--run' in params:
    c = commandBuilder.get_command(params['--run'])
    if c is not None:
        print('Running with command %s ...' % params['--run'])
        print(c.exec(params))
