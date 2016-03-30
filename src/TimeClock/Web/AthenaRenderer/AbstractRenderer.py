from TimeClock.ITimeClock.ICommand import ICommand
from TimeClock.Web.ActionItem import path
from TimeClock.Web.LiveFragment import LiveFragment
from nevow.loaders import xmlfile


class ActionItem(LiveFragment):
    docFactory = xmlfile(path + '/Pages/ActionItem.xml', 'ActionItemPattern', ignoreDocType=True)
    def __init__(self, parent, command: ICommand):
        self.parent=parent
        self.setFragmentParent(parent.parent)
        self.command = command
    def render_formArguments(self, ctx, idata):
        o = []
        for arg in self.command.getArguments():
            if arg is 'caller':
                continue
            t = input(type='text')
            if isinstance(arg, dict):
                arg, comment = list(arg.items())[0]
            else:
                comment = None
            t(id=arg)
            t.value = arg if not comment else (arg + "(%s)" % comment)
            t[arg]
            o.append(t)
            o.append(br())

        return o
