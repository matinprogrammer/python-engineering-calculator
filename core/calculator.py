import operator
from queue import LifoQueue
from typing import List


class InvalidNumberOrOperator(Exception):
    pass


class Calculator:
    operators = {
        # operator: (Priority, function)
        '+': (8, operator.add),
        '-': (8, operator.sub),
        '*': (9, operator.mul),
        '/': (9, operator.truediv),
        '^': (10, operator.pow),
        '%': (9, operator.mod)
    }

    def __init__(self, string_input: str):
        self.string_input = string_input

    @property
    def string_input(self):
        return self._string_input

    @string_input.setter
    def string_input(self, value: str):
        # check validate value
        value = value.replace(" ", "")
        if not self.check_validate_input(value):
            raise InvalidNumberOrOperator("you use unexpected character")

        self._string_input = value

    @staticmethod
    def check_validate_input(value):
        for string in value:
            if not any([
                string in list(Calculator.operators.keys()) + ['(', ')'],
                string.isnumeric(),
                string.isalpha()
            ]):
                return False
        return True

    def evaluate(self):
        postfix_string = self.convert_infix_to_postfix(self.string_input)
        numbers_stack = LifoQueue()
        for string in postfix_string:
            if string in self.operators.keys():
                if numbers_stack.empty():
                    raise InvalidNumberOrOperator("invalid numbers input, didnt have any number")
                number_2 = numbers_stack.get()
                if numbers_stack.empty():
                    raise InvalidNumberOrOperator("invalid numbers input, you have send one number")
                number_1 = numbers_stack.get()
                result = self.operators[string][1](number_1, number_2)
                numbers_stack.put(result)
            else:
                numbers_stack.put(int(string))

        if numbers_stack.empty():
            return 0
        else:
            return numbers_stack.get()

    @staticmethod
    def convert_infix_to_postfix(infix_string: str) -> List[str]:
        stack = LifoQueue()
        postfix_result = []

        if infix_string:
            postfix_result.append("")

        for string in infix_string:
            if string in Calculator.operators.keys():
                while not stack.empty():
                    last_operator = stack.get()
                    if (
                            last_operator == '('
                            or Calculator.operators[string][0] > Calculator.operators[last_operator][0]
                    ):
                        stack.put(last_operator)
                        stack.put(string)
                        break
                    else:
                        postfix_result.append(last_operator)
                if stack.empty():
                    stack.put(string)
            elif string == '(':
                stack.put('(')
            elif string == ')':
                stack_value = stack.get()
                while stack_value != '(':
                    postfix_result.append(stack_value)
                    stack_value = stack.get()
            elif string.isnumeric():
                postfix_result[-1] += string
                continue
            else:
                raise InvalidNumberOrOperator("your input invalid number or operator")

            # add blank cell in postfix_result to concatenate number together
            if postfix_result[-1] != '':
                postfix_result.append("")

        # add remaining operator from stack in postfix_result
        while not stack.empty():
            if postfix_result[-1] == '':
                postfix_result[-1] = stack.get()
            else:
                postfix_result.append(stack.get())

        return postfix_result
