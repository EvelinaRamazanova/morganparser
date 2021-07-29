class JAICPScript:
    def __init__(self):
        pass
    
    def __str__(self):
        raise NotImplementedError
    
    @staticmethod
    def from_tree(tree):
        """
        Used to construct a valid script from its AST
        """
        raise NotImplementedError
    
    def to_tree(self):
        """
        generates an AST from a string representation of a script
        """
        raise NotImplementedError