import re
from preparator import prepare_expression
from parser import get_expression_in_postfix_form
from evaluator import calculate_expression

def calculate(expression):
    calculated = 0.0
    if expression.strip():
        expression = prepare_expression(expression.lower())
        #print expression
        postfix_form = get_expression_in_postfix_form(expression)
        #print postfix_form
        calculated = calculate_expression(postfix_form)

    return float(calculated)