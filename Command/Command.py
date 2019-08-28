from Command.FakeLinkCommand import FakeLinkCommand
from Command.InitDatabaseCommand import InitDatabaseCommand
from Command.LinksCommand import LinksCommand


class CommandBuilder:
    def __init__(self):
        self.command = {
            str(LinksCommand.get_name()): LinksCommand(),
            str(FakeLinkCommand.get_name()): FakeLinkCommand(),
            str(InitDatabaseCommand.get_name()): InitDatabaseCommand()
        }

    def get_command(self, name):
        if name in self.command:
            return self.command[name]
        return None
