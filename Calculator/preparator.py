#Prepare epression for calculation. 
#For it, delete all spaces, and give negative numbers good form.

import re
from shared import *
from errors import *

def prepare_expression(expression):
    if len(expression) >= 0:
        wrong_functions = is_good(expression)
        if wrong_functions:
            raise UnknownFunction(', '.join(wrong_functions))
        if not is_valuable(expression[0]):
            expression = "(" + expression + ")"
        expression = process_spaces(expression)
        expression = process_repeated_signs(expression)
        expression = process_mult_bracket(expression)
        expression = process_numb_before_func(expression)
        expression = process_unary_operators(expression)
        expression = process_logarithm(expression)

    return expression.replace(" ", "").replace("(-","(#"). replace("(+", "(")

def is_good(expression):
    return re.findall("[^\d\w\+\*\-\/\.\(\)\s\^\,\%]", expression)

def process_logarithm(expression):
    return expression.replace("log10", "lg").replace("log", "ln")

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
    replaced = replace_sequences(expression, need_to_replace)
    result = process_brackets(replaced) 
    return result

def process_brackets(expression):
    return expression.replace("(-+", "(-")\
        .replace("(+-", "(-")\
        .replace("(--", "(")\
        .replace("(++", "(")

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


