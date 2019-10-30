class PyDoom:
    def __init__(self):
        pass

    def draw(self, surface, clock=None):
        pass

    def run(self):
        pass

    def update(self):
        pass

    def event(self, event, event_timer, pydoomobj=None):
        """

        :param event:
        :param event_timer:
        :param pydoomobj: Does this need to be here? It's used to allow the menu class to modify the
        current state of the game, be it switching from menu to game, or menu to another menu if that
        becomes a need
        :return:
        """
        pass
