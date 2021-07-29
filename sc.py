"""
High-level interface concept
"""

class Theme:
    """
    A Python wrapper for JAICP themes
    """
    def __init__(self, name = None, states = None):
        self.name = name
        self.states = states
    
    def add_state(self, state):
        raise NotImplementedError

    @staticmethod
    def from_tree(tree):
        raise NotImplementedError


class State:
    """
    A Python wrapper for JAICP states
    """
    def __init__(self, name, examples, transitions):
        self.name = name
        self.examples = examples
        self.transitions = transitions

    def __str__(self):
        return f"State(name={self.name}, {self.examples[0]})"
        
    @staticmethod
    def from_tree(tree):
        """
        Constructs a representation from an AST of a state.
        """
        names = list(tree.find_data("state_name"))
        assert len(names) == 1
        name = names[0].children[0].value
        examples = [example.children[0].value for example in list(
            tree.find_data("ex"))]
        qpatterns = [qpattern.children[0].value for qpattern in list(
            tree.find_data("qpattern"))]
        
        #TODO: optimize the extraction of script transitions
        transitions = [transition.children[0].value for transition in list(
            tree.find_data("transition"))]
        return State(name, examples, transitions)