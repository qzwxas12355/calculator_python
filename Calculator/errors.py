class SyntaxExpressionError(Exception):
    def __str__(self):
        return "Expression has wrong format"


class UnknownFunction(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "Expression has unknown function: " + str(self.value)
