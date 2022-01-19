import sys

class CommandLineInterface:
    """
    Hold a map of all functions. Decorating a function registers it.
    argv[1] - fn name
    argv[2:] - fn arguments: given as 'name=value'
    """
    commands = {}

    def command(self, f):
        self.commands[f.__name__] = f
        return f

    def main(self):
        if len(sys.argv) < 2 or sys.argv[1] not in self.commands:
            print('USAGE: python example.py <command> [<key>=<value>]*')
            return
        f = self.commands[sys.argv[1]]

        kwargs = {}
        for arg in sys.argv[2:]:
            k, v = arg.split('=')
            kwargs[k] = v
        print(kwargs)
        f(**kwargs)
