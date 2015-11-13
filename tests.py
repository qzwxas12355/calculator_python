#!usr/bin/python
    
import calc
import unittest
import math

class CalculateCheckResults(unittest.TestCase):
    results = (
        ("2+2", 2+2),
        ("1", 1),
        ("4*4", 4*4),
        ("5**4", 5**4),
        ("100/20", 100/20),
        ("19- 2", 19 -2),
        ("-14 + 5", -14 + 5),
        ("-2*2", -2**2),
        ("(-5)^2", (-5)**2),
        ("4+log(4,2)", 4+math.log(4,2)),
        ("log(log(8,64), 128)", math.log(math.log(8,64), 128)),
        ("sin(0)", math.sin(0)),
        ("sin(0.5)^2 + cos(0.5)^2", math.sin(0.5)**2 + math.cos(0.5)**2),
        ("tan(2)", math.tan(2)),
        ("pow(2,4)", 2**4),
        ("1/4 * (4 - 1/2)", 1.0/4 * (4 - 1.0/2)),
        ("sqrt(1801)", math.sqrt(1801)),
        ("exp(-100)", math.exp(-100)),
        ("log10(1000)", math.log10(1000)),
        ("abs(-14)", abs(-14)),
        ("asin(0.2)", math.asin(0.2)),
        ("asin(-0.5)", math.asin(-0.5)),
        ("16^(1/2)", 16**(1.0/2)),
        ("54**(-1/3)", 54**(-1.0/3)),
        ("tan(-1.5)", math.tan(-1.5)),
        ("(928*10**(-2)/0.8-0.6)/((42*(3+5.0/6)+3.3/0.03)/(1.0/15)/(((3+3.0/4)/0.625-0.84/0.8)/0.03))**(-1)", 
            (928*10**(-2)/0.8-0.6)/((42*(3+5.0/6)+3.3/0.03)/(1.0/15)/(((3+3.0/4)/0.625-0.84/0.8)/0.03))**(-1)),
        ("((7-6.35)/6.5+9.9)/(1.2/36+1.2/0.25-(1+5.0/16)/(169.0/24))", 
            ((7-6.35)/6.5+9.9)/(1.2/36+1.2/0.25-(1+5.0/16)/(169.0/24))),
        ("(sqrt(6.3*1.7)*(sqrt(6.3/1.7)-sqrt(1.7/6.3)))/sqrt((6.3+1.7)**2-4*6.3*1.7)",
            (math.sqrt(6.3*1.7)*(math.sqrt(6.3/1.7)-math.sqrt(1.7/6.3)))/math.sqrt((6.3+1.7)**2-4*6.3*1.7)),
        ("1+ + 4+2", 1++4+2),
        ("1 +- 5", 1+-5),
        ("65 - - 53", 65--53),
        ("639 - +23", 639 -+ 23),
        ("5+-4+++1---5+2+-+-6", 5+-4+++1---5+2+-+-6),
        ("100(+100-43)", 100*(+100 -43)),
        ("5-6(5+1)", 5-6*(5+1)),
        ("2(2+1)", 2*(2+1)),
        ("2(43+56)41", 2*(43+56)*41),
        ("e^2", math.e**2),
        ("e^(23)", math.e**(23)),
        ("e**(3)", math.e**(3)),
        ("e^(log(10,4))", math.e**(math.log(10,4))),
        ("3+ 3.-1", 3+3.-1),
        ("e", math.e),
        ("e^e", math.e**math.e),
        ("3**2**4", 3**2**4),
        ("e^e^e", math.e**math.e**math.e),
        ("4^ -2", 4** -2),
        ("-53//10", -53//10), 	
        ("5*e**2", 5*math.e**(2)),
        ("pi", math.pi),
        ("8pi(43+1)", 8*math.pi*(43+1)),
        ("e**-2**4", math.e**((-2)**4)),
        ("exp(exp(exp(1)))", math.exp(math.exp(math.exp(1)))),
        ("(2+2)(4+23)", (2+2)*(4+23)),
        ("1*4+3.3/(3+.3)*3(sqrt(4))/(sin(0)+1)", 1*4+3.3/(3+.3)*3*(math.sqrt(4))/(math.sin(0)+1)),
        ("10*e^0*log10(.4* -5/ -0.1-10) - -abs(-53//10) + -5", 10*math.exp(0)*math.log10(.4* -5/ -0.1-10) - -abs(-53//10) + -5),
        ("(1+2)3(4+5)", (1+2)*3*(4+5)),
        ("(1+2).3(4+5)", (1+2)*0.3*(4+5)),
        ("(1+2)3.3(4+5)", (1+2)*3.3*(4+5)),
        ("(4+3)log(4,2)", (4+3)*math.log(4,2)),
        ("log(9,3)(4+3)log(4,2)", math.log(9,3)*(4+3)*math.log(4,2)),
        ("(6+2)3.(4+5)", (6+2)*3.0*(4+5)),
        ("8e^5", 8*math.e**(5)),
        ("", 0.0),
        (" ", 0.0),
        ("          ", 0.0),
        ("atan2(4,2)", math.atan2(4,2)),
        ("hypot(4,2)", math.hypot(4,2)),
        ("degrees(34)", math.degrees(34)),
        ("radians(65)", math.radians(65)),
        ("cosh(2)", math.cosh(2)),
        ("sinh(54)", math.sinh(54)),
        ("tanh(10)", math.tanh(10)),
        ("acosh(92)", math.acosh(92)),
        ("asinh(72)", math.asinh(72)),
        ("atanh(.43)", math.atanh(.43)),
        ("0+-11//10", 0+-11/10),
        ("0-+-+-11//10", 0-+-+-11/10),
        ("0+--11//10", 0+--11/10),
        ("0-+-11//10", 0-+-11//10),
        ("0--+11//10", 0--+11//10),
        ("0++++11//10", 0+-+-11//10),
        ("0+++-11//10", 0+++-11//10),
        ("0++-+11//10", 0++-+11//10),
        ("0+-++11//10", 0+-++11//10),
        ("0-+++11//10", 0-+++11//10),
        ("0++--11//10", 0++--11//10),
        ("0+-+-11//10", 0+-+-11//10),
        ("0-++-11//10", 0-++-11//10),
        ("0+--+11//10", 0+--+11//10),
        ("0-+-+11//10", 0-+-+11//10),
        ("0--++11//10", 0--++11//10),
        ("0+---11//10", 0+---11//10),
        ("0-+--11//10", 0-+--11//10),
        ("0--+-11//10", 0--+-11//10),
        ("0---+11//10", 0---+11//10),
        
    )

    def test_calculate(self):
        for expression, result in self.results:
            evaluated = calc.calculate(expression)
            self.assertEqual(result, evaluated)

class CalculateBadInput(unittest.TestCase):
    wrong_expressions = (
        "3***7",
        "65///2",
        "2+",
        "3/",
        "54/+",
        "55*+*",
        "dad",
        "23+4+as+4",
        "exp+5-1",
        "log+3+6+2",
        "log(5)+1+5+7",
        "(56+7))*(7+6)",
        "((143+4)+3(4)",
    )

    def testBadExpression(self):
        for expression in self.wrong_expressions:
            self.assertRaises(calc.SyntaxExpressionError, calc.calculate, expression)

if __name__ == '__main__':
    unittest.main()