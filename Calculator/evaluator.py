from shared import *
from errors import *

#This function calculate postfix form expression
def calculate_expression(expression_postfix_form):
    for token in expression_postfix_form:
        #print expression_postfix_form
        if is_operator(token) or is_function(token):
            operation_position = expression_postfix_form.index(token)
            if operation_position == 0:
                raise SyntaxExpressionError()
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
        expression_postfix_form = make_binary_operation(expression_postfix_form, operation_position)
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

    #print operands
    if operator in OPERATORS_DICT.keys():
        result = OPERATORS_DICT[operator](to_float(operands[0]), to_float(operands[1]))
    elif operator in BINARY_FUNCTIONS_DICT.keys():
        result = BINARY_FUNCTIONS_DICT[operator](to_float(operands[0]), to_float(operands[1]))

    left_part.append(result)
    left_part.extend(right_part)

    return left_part