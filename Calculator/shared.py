import math

UNARY_FUNCTIONS_DICT = {
    "abs" : abs,
    "log10" : math.log10,
    "sin" : math.sin,
    "cos" : math.cos,
    "tan" : math.tan,
    "acos" : math.acos,
    "asin" : math.asin,
    "atan" : math.atan,
    "exp" : math.exp,
    "sqrt" : math.sqrt,
    "#" : float.__neg__,
    "degrees" : math.degrees,
    "radians" : math.radians,
    "cosh" : math.cosh,
    "sinh" : math.sinh,
    "tanh" : math.tanh,
    "acosh" : math.acosh,
    "asinh" : math.asinh,
    "atanh" : math.atanh,
}

CONSTANTS_DICT = {
    "e" : math.e,
    "pi" : math.pi,
}

BINARY_FUNCTIONS_DICT = {
    "pow" : float.__pow__,
    "log" : math.log,
    "atan2" : math.atan2,
    "hypot" : math.hypot,
}

OPERATORS_DICT = {
    "+" : float.__add__,
    "-" : float.__sub__,
    "*" : float.__mul__,
    "/" : float.__div__,
    "//" : float.__floordiv__,
    "%" : float.__mod__,
    "**" : float.__pow__,
    "^" : float.__pow__,
}

FUNCTIONS = tuple(UNARY_FUNCTIONS_DICT.keys() + BINARY_FUNCTIONS_DICT.keys())

LOW_PRIORITY = ("+", "-",)
MIDDLE_PRIORITY = ("*", "/", "%", "//",)
HIGH_PRIORITY = ("^", "**",)
HIGHEST_PRIORITY = ("#",)
BINARY_OPERATORS = LOW_PRIORITY + MIDDLE_PRIORITY + HIGH_PRIORITY
UNARY_OPERATORS = HIGHEST_PRIORITY
OPERATORS = UNARY_OPERATORS + BINARY_OPERATORS

def is_function(token):
    return token in FUNCTIONS

def is_operator(token):
    return token in OPERATORS