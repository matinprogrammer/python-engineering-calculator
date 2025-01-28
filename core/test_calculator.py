from unittest import TestCase
from core.calculator import Calculator, InvalidNumberOrOperator


class TestCalculator(TestCase):
    def test_valid_data(self):
        self.assertEqual(Calculator("2+3").string_input, "2+3")

    def test_blank_space_cleaner(self):
        self.assertEqual(Calculator("2+ 3").string_input, "2+3")

    def test_invalid_data(self):
        with self.assertRaises(InvalidNumberOrOperator) as e:
            Calculator("2+#")
        self.assertEqual(str(e.exception), "you use unexpected character")


class TestCalculatorEvaluate(TestCase):
    def test_empty(self):
        actual = Calculator("").evaluate()
        expected = 0
        self.assertEqual(actual, expected)

    def test_one_number(self):
        actual = Calculator("1").evaluate()
        expected = 1
        self.assertEqual(actual, expected)

    def test_one_operator_without_number(self):
        with self.assertRaises(InvalidNumberOrOperator) as e:
            Calculator("+").evaluate()
        self.assertEqual(str(e.exception), "invalid numbers input, didnt have any number")

    def test_one_operator_with_one_number(self):
        with self.assertRaises(InvalidNumberOrOperator) as e:
            Calculator("3+").evaluate()
        self.assertEqual(str(e.exception), "invalid numbers input, you have send one number")

    def test_invalid_character(self):
        with self.assertRaises(InvalidNumberOrOperator) as e:
            Calculator("#").evaluate()
        self.assertEqual(str(e.exception), "you use unexpected character")

    def test_simple_add(self):
        actual = Calculator("1+2").evaluate()
        expected = 3
        self.assertEqual(actual, expected)

    def test_multi_add(self):
        actual = Calculator("1+2+3+4").evaluate()
        expected = 10
        self.assertEqual(actual, expected)

    def test_priority_add_sub(self):
        actual = Calculator("1+2-3").evaluate()
        expected = 0
        self.assertEqual(actual, expected)

    def test_priority_sub_add(self):
        actual = Calculator("1-2+3").evaluate()
        expected = 2
        self.assertEqual(actual, expected)

    def test_priority_add_multi(self):
        actual = Calculator("1+2*3").evaluate()
        expected = 7
        self.assertEqual(actual, expected)

    def test_priority_multi_add(self):
        actual = Calculator("1*2+3").evaluate()
        expected = 5
        self.assertEqual(actual, expected)

    def test_parenthesis_add_multi(self):
        actual = Calculator("(1+2)*3").evaluate()
        expected = 9
        self.assertEqual(actual, expected)

    def test_parenthesis_multi_add(self):
        actual = Calculator("(1*2)+3").evaluate()
        expected = 5
        self.assertEqual(actual, expected)

    def test_two_digit_numbers_add(self):
        actual = Calculator("10+2").evaluate()
        expected = 12
        self.assertEqual(actual, expected)

    def test_three_digit_numbers_add(self):
        actual = Calculator("100+20").evaluate()
        expected = 120
        self.assertEqual(actual, expected)


class TestCalculatorPrefixToPostfix(TestCase):
    def test_empty(self):
        actual = Calculator.convert_infix_to_postfix('')
        expected = []
        self.assertEqual(actual, expected)

    def test_one_number(self):
        actual = Calculator.convert_infix_to_postfix('1')
        expected = ['1']
        self.assertEqual(actual, expected)

    def test_one_operator(self):
        actual = Calculator.convert_infix_to_postfix('+')
        expected = ['+']
        self.assertEqual(actual, expected)

    def test_invalid_character(self):
        with self.assertRaises(InvalidNumberOrOperator) as e:
            Calculator.convert_infix_to_postfix('#')
        self.assertEqual(str(e.exception), "your input invalid number or operator")

    def test_simple_add(self):
        actual = Calculator.convert_infix_to_postfix('1+2')
        expected = ['1', '2', '+']
        self.assertEqual(actual, expected)

    def test_multi_add(self):
        actual = Calculator.convert_infix_to_postfix('1+2+3+4')
        expected = ['1', '2', '+', '3', '+', '4', '+']
        self.assertEqual(actual, expected)

    def test_priority_add_sub(self):
        actual = Calculator.convert_infix_to_postfix('1+2-3')
        expected = ['1', '2', '+', '3', '-']
        self.assertEqual(actual, expected)

    def test_priority_sub_add(self):
        actual = Calculator.convert_infix_to_postfix('1-2+3')
        expected = ['1', '2', '-', '3', '+']
        self.assertEqual(actual, expected)

    def test_priority_add_multi(self):
        actual = Calculator.convert_infix_to_postfix('1+2*3')
        expected = ['1', '2', '3', '*', '+']
        self.assertEqual(actual, expected)

    def test_priority_multi_add(self):
        actual = Calculator.convert_infix_to_postfix('1*2+3')
        expected = ['1', '2', '*', '3', '+']
        self.assertEqual(actual, expected)

    def test_parenthesis_add_multi(self):
        actual = Calculator.convert_infix_to_postfix('(1+2)*3')
        expected = ['1', '2', '+', '3', '*']
        self.assertEqual(actual, expected)

    def test_parenthesis_multi_add(self):
        actual = Calculator.convert_infix_to_postfix('(1*2)+3')
        expected = ['1', '2', '*', '3', '+']
        self.assertEqual(actual, expected)

    def test_two_digit_numbers_add(self):
        actual = Calculator.convert_infix_to_postfix('10+2')
        expected = ['10', '2', '+']
        self.assertEqual(actual, expected)

    def test_three_digit_numbers_add(self):
        actual = Calculator.convert_infix_to_postfix('100+20')
        expected = ['100', '20', '+']
        self.assertEqual(actual, expected)

    # def test_logarithm(self):
    #     actual = Calculator.convert_infix_to_postfix('log(9)')
    #     expected = ['9', 'log']
    #     self.assertEqual(actual, expected)


class TestCalculatorSliceInfixStringToList(TestCase):
    def test_empty(self):
        actual = Calculator.slice_infix_string_to_list('')
        expected = []
        self.assertEqual(actual, expected)

    def test_one_number(self):
        actual = Calculator.slice_infix_string_to_list('1')
        expected = ['1']
        self.assertEqual(actual, expected)

    def test_two_digit_number(self):
        actual = Calculator.slice_infix_string_to_list('10')
        expected = ['10']
        self.assertEqual(actual, expected)

    def test_three_digit_number(self):
        actual = Calculator.slice_infix_string_to_list('123')
        expected = ['123']
        self.assertEqual(actual, expected)

    def test_simple_add(self):
        actual = Calculator.slice_infix_string_to_list('1+2')
        expected = ['1', '+', '2']
        self.assertEqual(actual, expected)

    def test_two_digit_number_add(self):
        actual = Calculator.slice_infix_string_to_list('10+59')
        expected = ['10', '+', '59']
        self.assertEqual(actual, expected)

    def test_logarithm(self):
        actual = Calculator.slice_infix_string_to_list('log(10)')
        expected = ['log', '(', '10', ')']
        self.assertEqual(actual, expected)

    def test_logarithm_with_add_in(self):
        actual = Calculator.slice_infix_string_to_list('log(10+3)')
        expected = ['log', '(', '10', '+', '3', ')']
        self.assertEqual(actual, expected)

    def test_logarithm_with_add_out(self):
        actual = Calculator.slice_infix_string_to_list('log(10)+11')
        expected = ['log', '(', '10', ')', '+', '11']
        self.assertEqual(actual, expected)

    def test_complex(self):
        actual = Calculator.slice_infix_string_to_list('1+2-3*4+log(5/6)*11-sin(9+4*9)')
        expected = ['1', '+', '2', '-', '3', '*', '4', '+', 'log', '(', '5', '/', '6', ')', '*', '11',
                    '-', 'sin', '(', '9', '+', '4', '*', '9', ')']
        self.assertEqual(actual, expected)
