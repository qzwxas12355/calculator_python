#!usr/bin/python

import re
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

def is_valuable(token):
    try:
        if not token in CONSTANTS_DICT.keys():
            c = float(token)
        return True
    except:
        return False

def is_operator(token):
    return token in OPERATORS

def operation_priority(token):
    if token in LOW_PRIORITY:
        return 0
    elif token in MIDDLE_PRIORITY:
        return 1
    elif token in HIGH_PRIORITY:
        return 2
    elif token in HIGHEST_PRIORITY:
        return 3

#Prepare epression for calculation. 
#For it, delete all spaces, and give negative numbers good form.
def prepare_expression(expression):
    if len(expression) >= 0:
        if expression[0] == "+":
            expression = expression[1:]
        elif expression[0] == "-":
            expression = expression.replace("-", "#")
        expression = process_spaces(expression)
        expression = process_repeated_signs(expression)
        expression = process_mult_bracket(expression)
        expression = process_numb_before_func(expression)
        expression = process_unary_operators(expression)

    return expression.replace(" ", "").replace("(-","(#"). replace("(+", "(")

def process_numb_before_func(expression):
    numb_before_func = re.findall(r"\d+[a-z]+", expression)
    if numb_before_func:
        for i in numb_before_func:
            tmp = re.split('([\d]+)', i.strip())
            expression = expression.replace(i, tmp[1]+"*"+tmp[2])
    return expression

def process_spaces(expression):
    return expression.replace(" ", "")

def process_unary_operators(expression):
    return expression.replace("*-", "*#")\
        .replace("/-","/#") \
        .replace("^-", "^#")\
        .replace("**-", "**#")\
        .replace("++", "+")\
        .replace("-+", "-")\
        .replace("+-", "+#")\
        .replace("--", "-#")
        
#Replace "++" to "+", "-+" to "-" etc.
def process_repeated_signs(expression):
    sequences = find_sequences_signs(expression)
    need_to_replace = process_sequences_signs(sequences)
    return replace_sequences(expression, need_to_replace)

def find_sequences_signs(expression):
    return re.findall("[+-]{3,}", expression)

def process_sequences_signs(multiplied_signs):
    need_to_replace = {}
    for sequence in multiplied_signs:
        count = sequence[1:].count('-')
        if count % 2 == 0:
            need_to_replace[sequence] = sequence[:1]
        else:
            need_to_replace[sequence] = sequence[:1] + '-'
    return need_to_replace
def replace_sequences(expression, need_to_replace):
    for old, new in need_to_replace.iteritems():
         expression = expression.replace(old, new)
    return expression
 
#Replace '3(' to '3*(', and ')4' to ')*4'
def process_mult_bracket(expression):
    numb_mul_bracket = re.findall(r"[*+-/%#]\d+\(|\p\i\(|\e\(|\)\.\d+\(|\)\d+\.\(|\)\d+\(|\)\d+|^\d+\(|\)\w+", expression)
    expression = expression.replace(")(", ")*(")
    if numb_mul_bracket:
        multiplies = map(lambda a: (a, a.replace("(", "*(").replace(")", ")*")), numb_mul_bracket)
        multiplies = set(multiplies)
        for old, new in multiplies:
            expression = expression.replace(old, new)
    return expression

def get_token_list(expression):
    return re.findall(r"\l\o\g\w+|\/\/|\*\*|\.\w+|\W|\w+\.\w+|\w+\.|\w+", expression)

def is_open_bracket(token):
    return token == "("

def is_close_bracket(token):
    return token == ")"

def should_pop_oprations(token, operation_stack):
    should = False
    if operation_stack and is_operator(operation_stack[-1]):
        if operation_priority(token) <= operation_priority(operation_stack[-1]) \
                and (token in LOW_PRIORITY \
                        or token in MIDDLE_PRIORITY \
                        or token in HIGHEST_PRIORITY):
            should = True
        elif operation_priority(token) < operation_priority(operation_stack[-1]) \
                and (token in HIGH_PRIORITY \
                    or token in HIGHEST_PRIORITY):
            should = True
    return should

def parse_to_postfix_form(token_list):
    operation_stack = []
    postfix_form_stack = []
    brackets_counter = 0
    for token in token_list:
        if is_open_bracket(token):
            operation_stack.append(token)
            brackets_counter += 1
        elif is_close_bracket(token):
            brackets_counter -= 1
            if brackets_counter < 0:
                raise SyntaxExpressionError()
            while operation_stack and  not is_open_bracket(operation_stack[-1]):
                postfix_form_stack.append(operation_stack.pop())
            if operation_stack:
                operation_stack.pop()
            if operation_stack and operation_stack[-1] in FUNCTIONS:
                postfix_form_stack.append(operation_stack.pop())
        elif is_valuable(token):
            postfix_form_stack.append(token)
        elif is_operator(token):
            while should_pop_oprations(token, operation_stack):
                postfix_form_stack.append(operation_stack.pop())
            operation_stack.append(token)
        elif is_function(token):
            operation_stack.append(token)
        elif operation_stack \
            and not(is_open_bracket(operation_stack[-1])  
                    or is_close_bracket(operation_stack[-1])):
            if operation_stack:
                postfix_form_stack.append(operation_stack.pop())
    while operation_stack:
        postfix_form_stack.append(operation_stack.pop())

    if brackets_counter != 0:
        raise SyntaxExpressionError()

    return postfix_form_stack

#This function calculate postfix form expression
def calculate_expression(expression_postfix_form):
    for token in expression_postfix_form:
        if is_operator(token) or is_function(token):
            operation_position = expression_postfix_form.index(token)
            try:
                expression_postfix_form = make_operation(expression_postfix_form, operation_position)
            except IndexError:
                raise SyntaxExpressionError()

    if len(expression_postfix_form) == 1:
        return to_float(expression_postfix_form[0]) 
    else: 
        raise SyntaxExpressionError()

def to_float(number):
    if not number in CONSTANTS_DICT.keys():
        return float(number)
    else: 
        return CONSTANTS_DICT[number]
    

def make_operation(expression_postfix_form, operation_position):
    operation = expression_postfix_form[operation_position]
    if operation in BINARY_FUNCTIONS_DICT.keys() or operation in BINARY_OPERATORS:
        expression_postfix_form=make_binary_operation(expression_postfix_form, operation_position)
    elif operation in UNARY_FUNCTIONS_DICT.keys():
        expression_postfix_form = make_unary_operation(expression_postfix_form, operation_position)
    else:
        raise UnknownFunctionError(operation)
    return expression_postfix_form

def make_unary_operation(expression_postfix_form, operation_position):
    operand = expression_postfix_form[operation_position-1]

    left_part = expression_postfix_form[:operation_position-1]
    right_part = expression_postfix_form[operation_position+1:]
    result = 0.0

    operator = expression_postfix_form[operation_position]

    result = UNARY_FUNCTIONS_DICT[operator](to_float(operand))

    left_part.append(result)
    left_part.extend(right_part)
    
    return left_part


def make_binary_operation(expression_postfix_form, operation_position):
    operands = expression_postfix_form[operation_position-2: operation_position]

    left_part = expression_postfix_form[:operation_position-2]
    right_part = expression_postfix_form[operation_position+1:]
    result = 0.0
    operator = expression_postfix_form[operation_position]

#    if (operator == "^" or operator == "**") and operands[0] == "e":
#        result = math.exp(to_float(operands[1]))
    if operator in OPERATORS_DICT.keys():
        result = OPERATORS_DICT[operator](to_float(operands[0]), to_float(operands[1]))
    elif operator in BINARY_FUNCTIONS_DICT.keys():
        result = BINARY_FUNCTIONS_DICT[operator](to_float(operands[0]), to_float(operands[1]))

    left_part.append(result)
    left_part.extend(right_part)

    return left_part

def calculate(expression):
    if not expression.strip():
        return 0.0
    expression = prepare_expression(expression.lower())

    token_list = get_token_list(expression)

    postfix_form_stack = parse_to_postfix_form(token_list)

    calculated = calculate_expression(postfix_form_stack)

    return float(calculated)


class SyntaxExpressionError(Exception):
    def __str__(self):
        return "Expression has wrong format"


class UnknownFunctionError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "Expression has unknown function: " + str(self.value)

#9.30 gorodok 