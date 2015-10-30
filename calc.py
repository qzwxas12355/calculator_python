import re
import math

BINARY_FUNCTIONS = [
             "pow", 
             "log"
    ]
UNARY_FUNCTIONS = [
             "abs",
             "ln",
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
OPERATORS = LOW_PRIORITY + MIDDLE_PRIORITY + HIGH_PRIORITY

def is_function(token):
    return token in FUNCTIONS

def is_number(token):
    try:
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
    else:
        return 0.5

#Prepare epression for calculation. 
#For it, delete all spaces, and give negative numbers good form.
def prepare_expression(expression):
    if len(expression) >= 0:
        if expression[0] == "-" or expression[0] == "+":
            expression = "0" + expression
    return expression.replace(" ", "").replace("(-","(0-"). replace("(+", "(0+")

def get_token_list(expression):
    return re.findall(r"\/\/|\*\*|\.\w+|\W|\w+\.\w+|\w+\.|\w+", expression)

def is_open_bracket(token):
    return token == "("

def is_close_bracket(token):
    return token == ")"

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
        elif is_number(token):
            postfix_form_stack.append(token)
        elif is_operator(token):
            while operation_stack \
                  and is_operator(operation_stack[-1]) \
                  and operation_priority(token) <= operation_priority(operation_stack[-1]):
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
            expression_postfix_form = make_operation(expression_postfix_form, operation_position)
            
    return expression_postfix_form[0]

def make_operation(expression_postfix_form, operation_position):
    operation = expression_postfix_form[operation_position]
    if operation in BINARY_FUNCTIONS or operation in OPERATORS:
        expression_postfix_form = make_binary_operation(expression_postfix_form, operation_position)
    elif operation in UNARY_FUNCTIONS:
        expression_postfix_form = make_unary_operation(expression_postfix_form, operation_position)

    return expression_postfix_form

def make_unary_operation(expression_postfix_form, operation_position):
    operand = expression_postfix_form[operation_position-1]

    left_part = expression_postfix_form[:operation_position-1]
    right_part = expression_postfix_form[operation_position+1:]
    result = 0.0

    operator = expression_postfix_form[operation_position]

    if operator == "abs":
        result = math.abs(float(operand))
    elif operator == "sqrt":
        result = math.sqrt(float(operand))
    elif operator == "sin":
        result = math.sin(float(operand))
    elif operator == "cos":
        result = math.cos(float(operand))
    elif operator == "tan":
        result = math.tan(float(operand))
    elif operator == "ctg":
        result = 1/math.tan(float(operand))
    elif operator == "atan":
        result = math.atan(float(operand))
    elif operator == "acos":
        result = math.acos(float(operand))
    elif operator == "asin":
        result = math.asin(float(operand))
    elif operator == "ln":
        result = math.log10(float(operand))
    elif operator == "exp":
        result = math.exp(float(operand))

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
        result = float(operands[0]) + float(operands[1])           
    elif operator == "-":
        result = float(operands[0]) - float(operands[1])
    elif operator == "*":
        result = float(operands[0]) * float(operands[1])
    elif operator == "/":
        result = float(operands[0]) / float(operands[1])
    elif operator == "**":
        result = float(operands[0]) ** float(operands[1])
    elif operator == "^":
        result = float(operands[0]) ** float(operands[1])
    elif operator == "%":
        result = float(operands[0]) % float(operands[1])
    elif operator == "//":
        result = float(operands[0]) // float(operands[1])
    elif operator == "pow":
        result = float(operands[0]) ** float(operands[1])
    elif operator == "log":
        result = math.log(float(operands[1]), float(operands[0]))

    left_part.append(result)
    left_part.extend(right_part)
    
    return left_part

def calculate(expression):
    expression = prepare_expression(expression)

    token_list = get_token_list(expression)

    postfix_form_stack = parse_to_postfix_form(token_list)

    calculated = calculate_expression(postfix_form_stack)

    print "Result: %s" % (calculated)

expression = raw_input("Enter expression:")

calculate(expression)

#9.30 gorodok 