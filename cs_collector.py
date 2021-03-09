#crosssection generation framework still to be completely implemented
class cs_collection():
    """This is a collection of crossections."""

    #constructor creates four empty crosssection lists
    def __init__(self, initial_cs, current_cs = None, last_cs = None, best_cs = None):
        self.initial_cs = initial_cs
        self.current_cs = current_cs if current_cs is not None else initial_cs
        self.last_cs = last_cs if last_cs is not None else initial_cs
        self.best_cs = best_cs if best_cs is not None else initial_cs

    def in_from_optimizer(self, new_cs):
        pass

    def compare(self, new_cs):
        pass

    def update(self, new_cs, worsebetterbest):
        pass
