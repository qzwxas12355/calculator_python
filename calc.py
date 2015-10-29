import re

BINARY_FUNCTIONS = [
             "pow", 
             "log"
    ]
UNARY_FUNCTIONS = [
             "abs",
             "ln",
             "sin", 
             "cos", 
             "tg", 
             "ctg", 
             "acos", 
             "asin", 
             "atan", 
             "exp", 
             "sqrt", 
             "sqr",
]
FUNCTIONS = UNARY_FUNCTIONS + BINARY_FUNCTIONS
LOW_PRIORITY = ["+", "-"]
MIDDLE_PRIORITY = ["*", "/", "%", "//"]
HIGH_PRIORITY = ["^", "**"]
OPERATORS = LOW_PRIORITY + MIDDLE_PRIORITY + HIGH_PRIORITY

operation_stack = []

numbers_stack = []

postfix_form_stack = []

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
        return 3

#Prepare epression for calculation. 
#For it, delete all spaces, and give negative numbers good form.
def prepare_expression(expression):
    if len(expression) >= 0:
        if expression[0] == "-" or expression[0] == "+":
            expression = "0" + expression
    return expression.replace(" ", "").replace("(-","(0-"). replace("(+", "(0+")

def get_token_list(expression):
    return re.findall(r"\.\w+|\W|\w+\.\w+|\w+\.|\w+", expression)

def is_open_bracket(token):
    return token == "("

def is_close_bracket(token):
    return token == ")"

def parse_to_postfix_form(token_list, operation_stack, numbers_stack, postfix_form_stack):
    for token in token_list:
        
        if is_open_bracket(token):
            operation_stack.append(token)
        elif is_close_bracket(token):
            while operation_stack and  not is_open_bracket(operation_stack[-1]):
                postfix_form_stack.append(operation_stack.pop())
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
    for operation in operation_stack:
        postfix_form_stack.append(operation_stack.pop())

def calculate(expression):
    del operation_stack[:]
    del numbers_stack[:]
    del postfix_form_stack[:]

    expression = prepare_expression(expression)

    token_list = get_token_list(expression)

    parse_to_postfix_form(token_list, operation_stack, numbers_stack, postfix_form_stack)


expression = raw_input("Enter expression:")

calculate(expression)
print '|'.join(postfix_form_stack)

