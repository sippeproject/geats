from abstract import AbstractVirtualMachine

class DummyVirtualMachine(AbstractVirtualMachine):
    def _define(self):
        print "DummyVirtualMachine: Defining", self.name
        self.state = "stopped"
    def _start(self):
        print "DummyVirtualMachine: Starting", self.name
        self.state = "running"
    def _stop(self):
        print "DummyVirtualMachine: Stopping", self.name
        self.state = "stopped"
    def _shutdown(self):
        print "DummyVirtualMachine: ShuttingDown", self.name
        self.state = "stopped"
    def _undefine(self):
        print "DummyVirtualMachine: Undefine", self.name
        self.state = "unknown"
    def get_state(self):
        try:
            return self.state, self.state
        except AttributeError:
            return "unknown", "unknown"
