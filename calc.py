#!usr/bin/python

import re
import math

BINARY_FUNCTIONS = [
             "pow", 
             "log"
    ]
UNARY_FUNCTIONS = [
             "abs",
             "log10",
             "sin", 
             "cos", 
             "tan", 
             "ctg", 
             "acos", 
             "asin", 
             "atan", 
             "exp", 
             "sqrt"
]
FUNCTIONS = UNARY_FUNCTIONS + BINARY_FUNCTIONS

LOW_PRIORITY = ["+", "-"]
MIDDLE_PRIORITY = ["*", "/", "%", "//"]
HIGH_PRIORITY = ["^", "**"]
HIGHEST_PRIORITY = ["#"]
BINARY_OPERATORS = LOW_PRIORITY + MIDDLE_PRIORITY + HIGH_PRIORITY
UNARY_OPERATORS = HIGHEST_PRIORITY
OPERATORS = UNARY_OPERATORS + BINARY_OPERATORS

def is_function(token):
    return token in FUNCTIONS

def is_valuable(token):
    try:
        if token != "e":
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
        expression = process_unary_operators(expression)

    return expression.replace(" ", "").replace("(-","(#"). replace("(+", "(")

def process_spaces(expression):
    return expression.replace(" ", "")

def process_unary_operators(expression):
    return expression.replace("*-", "*#")\
        .replace("/-","/#") \
        .replace("^-", "^#")\
        .replace("**-", "**#")
#Replace "++" to "+", "-+" to "-" etc.
def process_repeated_signs(expression):
    rigth_signs = expression.replace("++", "+")\
        .replace("+-", "-")\
        .replace("-+", "-")\
        .replace("--", "+")
    while rigth_signs != expression:
        expression = rigth_signs
        rigth_signs = expression.replace("--", "+")\
            .replace("++", "+")\
            .replace("+-", "-")\
            .replace("-+", "-")
    return expression
 
#Replace '3(' to '3*(', and ')4' to ')*4'
def process_mult_bracket(expression):
    numb_mul_bracket = re.findall(r"\W+\d+\(|\)\d+|\.\d+\(|^\d+\(", expression)
    expression = expression.replace(")(", ")*(")
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
    if operation_stack and is_operator(operation_stack[-1]):
        if operation_priority(token) <= operation_priority(operation_stack[-1]) \
                and (token in LOW_PRIORITY \
                        or token in MIDDLE_PRIORITY \
                        or token in HIGHEST_PRIORITY):
            return True
        elif operation_priority(token) < operation_priority(operation_stack[-1]) \
                and (token in HIGH_PRIORITY \
                    or token in HIGHEST_PRIORITY):
            return True
    return False

def parse_to_postfix_form(token_list):
    operation_stack = []
    postfix_form_stack = []
    for token in token_list:
        if is_open_bracket(token):
            operation_stack.append(token)
        elif is_close_bracket(token):
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

    return postfix_form_stack

#This function calculate postfix form expression
def calculate_expression(expression_postfix_form):
    for token in expression_postfix_form:
        if is_operator(token) or is_function(token):
            operation_position = expression_postfix_form.index(token)
            try:
                expression_postfix_form = make_operation(expression_postfix_form, operation_position)
            except IndexError:
                raise ExpressionError

    if len(expression_postfix_form) == 1:
        return to_float(expression_postfix_form[0]) 
    else: 
        raise ExpressionError

def to_float(number):
    if number != "e":
        return float(number)
    else: 
        return math.exp(1)
    

def make_operation(expression_postfix_form, operation_position):
    operation = expression_postfix_form[operation_position]
    if operation in BINARY_FUNCTIONS or operation in BINARY_OPERATORS:
        expression_postfix_form = make_binary_operation(expression_postfix_form, operation_position)
    elif operation in UNARY_FUNCTIONS or operation in UNARY_OPERATORS:
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

    if operator == "abs":
        result = abs(to_float(operand))
    elif operator == "sqrt":
        result = math.sqrt(to_float(operand))
    elif operator == "sin":
        result = math.sin(to_float(operand))
    elif operator == "cos":
        result = math.cos(to_float(operand))
    elif operator == "tan":
        result = math.tan(to_float(operand))
    elif operator == "ctg":
        result = 1/math.tan(to_float(operand))
    elif operator == "atan":
        result = math.atan(to_float(operand))
    elif operator == "acos":
        result = math.acos(to_float(operand))
    elif operator == "asin":
        result = math.asin(to_float(operand))
    elif operator == "log10":
        result = math.log10(to_float(operand))
    elif operator == "exp":
        result = math.exp(to_float(operand))
    elif operator == "#":
        result = -to_float(operand)

    left_part.append(result)
    left_part.extend(right_part)
    
    return left_part


def make_binary_operation(expression_postfix_form, operation_position):
    operands = expression_postfix_form[operation_position-2: operation_position]

    left_part = expression_postfix_form[:operation_position-2]
    right_part = expression_postfix_form[operation_position+1:]
    result = 0.0

    operator = expression_postfix_form[operation_position]

    if operator == "+":
        result = to_float(operands[0]) + to_float(operands[1])           
    elif operator == "-":
        result = to_float(operands[0]) - to_float(operands[1])
    elif operator == "*":
        result = to_float(operands[0]) * to_float(operands[1])
    elif operator == "/":
        result = to_float(operands[0]) / to_float(operands[1])
    elif operator == "^" or operator == "**":
        if operands[0] == "e":
            result = math.exp(to_float(operands[1]))
        else:
            result = to_float(operands[0]) ** to_float(operands[1])
    elif operator == "%":
        result = to_float(operands[0]) % to_float(operands[1])
    elif operator == "//":
        result = to_float(operands[0]) // to_float(operands[1])
    elif operator == "pow":
        result = to_float(operands[0]) ** to_float(operands[1])
    elif operator == "log":
        result = math.log(to_float(operands[0]), to_float(operands[1]))

    left_part.append(result)
    left_part.extend(right_part)

    return left_part

def calculate(expression):
    if not expression.strip():
        raise EmptyExpressionError
    expression = prepare_expression(expression.lower())
    
    token_list = get_token_list(expression)

    postfix_form_stack = parse_to_postfix_form(token_list)

    calculated = calculate_expression(postfix_form_stack)

    return float(calculated)


class ExpressionError(Exception):
    def __str__(self):
        return "Expression has wrong format"

class UnknownFunctionError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "Expression has unknown function: " + str(self.value)

class EmptyExpressionError(Exception):
    def __str__(self):
        return "Expression is empty"


#9.30 gorodok 