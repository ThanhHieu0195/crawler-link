from Command.FakeLinkCommand import FakeLinkCommand
from Command.LinksCommand import LinksCommand


class CommandBuilder:
    def __init__(self):
        self.command = {
            str(LinksCommand.get_name()): LinksCommand(),
            str(FakeLinkCommand.get_name()): FakeLinkCommand()
        }

    def get_command(self, name):
        print(self.command)
        if name in self.command:
            return self.command[name]
        return None
