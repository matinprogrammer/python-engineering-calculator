import operator, math
from queue import LifoQueue
from typing import List, Union


class InvalidNumberOrOperator(Exception):
    pass


class Calculator:
    operators = {
        # operator: (Priority, function, input_count)
        '+': (8, operator.add, 2),
        '-': (8, operator.sub, 2),
        '*': (9, operator.mul, 2),
        '/': (9, operator.truediv, 2),
        '^': (10, operator.pow, 2),
        '%': (9, operator.mod, 2),
        'log': (11, math.log10, 1)
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
                numbers = []
                count_of_digits = Calculator.operators[string][2]
                for i in range(count_of_digits):
                    if numbers_stack.empty():
                        raise InvalidNumberOrOperator(
                            f"invalid numbers input, you have send {count_of_digits} number, you need to send "
                            f"{count_of_digits - i} number more"
                        )
                    numbers.append(numbers_stack.get())

                result = self.operators[string][1](*list(reversed(numbers)))
                numbers_stack.put(result)
            else:
                numbers_stack.put(int(string))

        if numbers_stack.empty():
            return 0
        else:
            return numbers_stack.get()

    @staticmethod
    def slice_infix_string_to_list(infix_string: str) -> List:
        infix_list = []

        current_number = ''
        current_string_operation = ''

        for string in infix_string:
            if string.isnumeric():
                current_number += string
            elif string.isalpha():
                current_string_operation += string
            elif string in list(Calculator.operators.keys()) + ['(', ')']:
                if current_number:
                    infix_list.append(current_number)
                if current_string_operation:
                    infix_list.append(current_string_operation)
                current_number = ''
                current_string_operation = ''
                infix_list.append(string)
            else:
                infix_list.append(string)

        if current_number:
            infix_list.append(current_number)
        if current_string_operation:
            infix_list.append(current_string_operation)

        return infix_list

    @staticmethod
    def convert_infix_to_postfix(infix_list: Union[str, List]) -> List[str]:
        if isinstance(infix_list, str):
            infix_list = Calculator.slice_infix_string_to_list(infix_list)

        stack = LifoQueue()
        postfix_result = []

        for string in infix_list:
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
                postfix_result.append(string)
            else:
                raise InvalidNumberOrOperator("your input invalid number or operator")

        # add remaining operator from stack in postfix_result
        while not stack.empty():
            postfix_result.append(stack.get())

        return postfix_result

