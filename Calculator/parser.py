import re
import math
import errors

from shared import *
from errors import *

def get_expression_in_postfix_form(expression):
    token_list = get_token_list(expression)
    return parse_to_postfix_form(token_list)

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
            while should_pop_operations(token, operation_stack):
                postfix_form_stack.append(operation_stack.pop())
            operation_stack.append(token)
        elif is_function(token):
            operation_stack.append(token)
        elif len(operation_stack) > 2 and operation_stack[-2] == "ln" and token== ",":
            operation_stack[-2] = "log"
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

def get_token_list(expression):
    return re.findall(r"\/\/|\*\*|\.\w+|\W|\w+\.\w+|\w+\.|\w+", expression)

def is_open_bracket(token):
    return token == "("

def is_close_bracket(token):
    return token == ")"

def should_pop_operations(token, operation_stack):
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

def operation_priority(token):
    if token in LOW_PRIORITY:
        return 0
    elif token in MIDDLE_PRIORITY:
        return 1
    elif token in HIGH_PRIORITY:
        return 2
    elif token in HIGHEST_PRIORITY:
        return 3








