from Command.FakeLinkCommand import FakeLinkCommand


class CommandBuilder:
    def __init__(self):
        self.command = {str(FakeLinkCommand.get_name()): FakeLinkCommand()}

    def get_command(self, name):
        if name in self.command:
            return self.command[name]
        return None
