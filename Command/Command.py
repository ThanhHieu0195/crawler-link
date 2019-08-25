from Command.FakeLinkCommand import FakeLinkCommand
from Command.LinksCommand import LinksCommand


class CommandBuilder:
    def __init__(self):
        self.command = {str(FakeLinkCommand.get_name()): FakeLinkCommand()}
        self.command = {str(LinksCommand.get_name()): LinksCommand()}

    def get_command(self, name):
        if name in self.command:
            return self.command[name]
        return None
