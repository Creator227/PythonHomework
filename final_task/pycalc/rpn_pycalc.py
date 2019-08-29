"""
calculator() function evaluating base mathematical
options using reverse-polish-notation algorithm
"""
import operator
import re
from collections import namedtuple, OrderedDict
import operator
import re
import sys


def _import_modules(*_modules):
    """
    Importing users modules into global variable
    which is used by find_attribute function
    :param _modules - tuple of modules names
    """
    global modules
    modules = _modules
    for module in _modules:
        try:
            globals()[module] = __import__(module)
        except ImportError:
            raise ImportError("Module not found:" + module)


def _find_attribute(attribute_name):
    """
    Find attribute in _modules.
    If attribute don't have dot in it's name,
    function try to find attribute on top level of _modules
    If attribute have dot in it's name,
    then function will try to get exact attribute.
    :param attribute_name: Name of searching attribute
    :return Object of attribute
    """
    attribute_names = attribute_name.split('.')
    if len(attribute_names) == 1:
        for module in modules:
            attribute = getattr(sys.modules[module], attribute_names[0], None)
            if attribute:
                return attribute
    else:
        # search attribute im submodules
        if attribute_name[0] in modules:
            attribute = getattr(sys.modules[__name__], attribute_names[0], None)
            for part in attribute_names[1:]:
                attribute = getattr(attribute, part, None)
            if attribute:
                return attribute

    raise ArithmeticError("Unknown function or constant:" + str(attribute_names))


_handler = namedtuple('handler', 'regex, operator, precedence')
_token = namedtuple('token', 'type, value')

# Dict of handlers for all possible types of params
# provides regular expression to find this type in input expression
_HANDLERS_DICT = OrderedDict([
    ('Float', _handler(re.compile(r'\d*\.\d+'), float, 9)),
    ('Integer', _handler(re.compile(r'\d+'), int, 9)),
    ('Plus', _handler(re.compile(r'\+'), operator.add, 4)),
    ('Minus', _handler(re.compile(r'-'), operator.sub, 4)),
    ('Power', _handler(re.compile(r'(\^)|(\*\*)'), operator.pow, 7)),
    ('Multiply', _handler(re.compile(r'\*'), operator.mul, 5)),
    ('RemainderDivision', _handler(re.compile(r'%'), operator.mod, 5)),
    ('WholeDivision', _handler(re.compile(r'//'), operator.floordiv, 5)),
    ('Division', _handler(re.compile(r'/'), operator.truediv, 5)),
    ('Equal', _handler(re.compile(r'=='), operator.eq, 2)),
    ('Less-Equal', _handler(re.compile(r'<='), operator.le, 3)),
    ('Less', _handler(re.compile(r'<'), operator.lt, 3)),
    ('Greater-Equal', _handler(re.compile(r'>='), operator.ge, 3)),
    ('Greater', _handler(re.compile(r'>'), operator.gt, 3)),
    ('Non-Equal', _handler(re.compile(r'!='), operator.ne, 2)),
    ('LeftBracket', _handler(re.compile(r'\('), str, 0)),
    ('RightBracket', _handler(re.compile(r'\)'), str, 0)),
    ('Comma', _handler(re.compile(r','), str, 8)),
    ('Space', _handler(re.compile(r'\s+'), None, None)),
    ('Function', _handler(re.compile(r'[\w]+\('), _find_attribute, 1)),
    ('Constant', _handler(re.compile(r'[\w]+'), _find_attribute, 9)),
    ('Arguments', _handler(None, bool, 1)),
    ('UnaryMinus', _handler(None, lambda x: x * -1, 6)),
    ('UnaryPlus', _handler(None, lambda x: x, 6)),

])


def _get_handler(token):
    return _HANDLERS_DICT[token.type]


def _prepare_expression(expression: str) -> str:
    # for expressions with multiple unary operators
    # for -----2
    while re.search(r'(- )|( -)', expression):
        expression = re.sub(r'(- )|( -)', r'-', expression)
    while re.search(r'(\+ )|( \+)', expression):
        expression = re.sub(r'(\+ )|( \+)', r'+', expression)
    flag = False
    while not flag:
        flag = True
        while re.search(r'--', expression):
            expression = re.sub(r'--', r'-', expression)
            flag = False
        while re.search(r'(\+-)|(-\+)', expression):
            expression = re.sub(r'(\+-)|(-\+)', r'-', expression)
            flag = False
        while re.search(r'(-\(-)', expression):
            expression = re.sub(r'(-\(-)', r'+(', expression)
            flag = False

    return expression


def _tokenize(expression: str) -> list:
    """
    Takes mathematical expression and transforms it in list of tokens.
    Сharacter become tokens, order does not change.
    :parameter expression
    :return the list of tokens
    """
    tokens = list()
    while expression:
        # tokenize starts from left characters in expression
        for token_type, (regex, _, _) in _HANDLERS_DICT.items():
            if regex is not None:
                match = regex.match(expression)
                if match:
                    if token_type != 'Space':
                        tokens.append(_token(token_type, match.group()))
                    # cut the token appended from expression
                    expression = expression[match.end():]
                    break
    return tokens


def _find_unary(tokens: list) -> list:
    """ All pluses and minuses in input list of tokens are binary
    This function replace it with unary """
    no_unary = {'Integer', 'Float', 'Constant', 'RightBracket'}
    for token in tokens:
        index = tokens.index(token)
        if token.type in {'Plus', 'Minus'} and (index == 0 or tokens[index-1][0] not in no_unary):
            tokens[index] = _token('UnaryPlus', '+') if token.type == 'Plus' else _token('UnaryMinus', '-')
    return tokens


def _make_rpn(tokens: list):
    stack = list()
    rpn_queue = list()
    have_args = list()
    for index, token in enumerate(tokens):
        handler = _get_handler(token)
        if token.type in {'Float', 'Integer', 'Constant'}:
            rpn_queue.append(token)
        elif token.type == 'Function':
            stack.append(token)
            # If function have no arguments we append False before FUNC
            if tokens[index + 1].type == 'RightBracket':
                have_args.append(False)
            else:
                have_args.append(True)
        elif not stack:
            stack.append(token)
        elif token.type == 'Comma':
            while stack[-1].type != 'Function':
                rpn_queue.append(stack.pop())
            rpn_queue.append(token)
        elif token.type == 'LeftBracket':
            stack.append(token)
        elif token.type == 'RightBracket':
            while stack[-1].type not in {'LeftBracket', 'Function'}:
                rpn_queue.append(stack.pop())
                if not stack:
                    raise ArithmeticError("ERROR: brackets are not balanced")
            if stack[-1].type == 'Function':
                rpn_queue.append(_token('Arguments', have_args.pop()))
                rpn_queue.append(stack.pop())
            else:
                stack.pop()
        elif token.type in {'UnaryPlus', 'UnaryMinus'} and stack[-1].type == 'Power':
            # From Python docs: The power operator binds more tightly
            # than unary operators on its left;
            # it binds less tightly than unary operators on its right.
            stack.append(token)
        elif handler.precedence == _get_handler(stack[-1]).precedence and \
                token.type in {'Power', 'UnaryMinus', 'UnaryPlus'}:
            # Association for operators of power, UMinus & UPlus - Right right ^ is more important
            stack.append(token)
        elif handler.precedence <= _get_handler(stack[-1]).precedence:
            while stack:
                if handler.precedence <= _get_handler(stack[-1]).precedence:
                    rpn_queue.append(stack.pop())
                    continue
                else:
                    break
            stack.append(token)
        else:
            stack.append(token)
    while stack:
        rpn_queue.append(stack.pop())
    return rpn_queue


def _rpn_calculate(rpn_queue):
    rpn_stack = list()
    for token in rpn_queue:
        handler = _get_handler(token)
        if token.type in ('Integer', 'Float', 'Constant', 'Comma', 'Arguments'):
            rpn_stack.append(handler.operator(token.value))
        elif token.type == 'Function':
            function_args = list()
            if rpn_stack.pop() is True:
                function_args.append(rpn_stack.pop())
            while rpn_stack and rpn_stack[-1] == ',':
                rpn_stack.pop()
                function_args.append(rpn_stack.pop())
            function_args.reverse()
            rpn_stack.append(handler.operator(token.value[:-1])(*function_args))
        elif token.type in {'UnaryPlus', 'UnaryMinus'}:
            try:
                # operand = rpn_stack.pop()
                rpn_stack.append(handler.operator(rpn_stack.pop()))
            except IndexError:
                raise ArithmeticError('Calculation error')
        else:
            try:
                operand_2, operand_1 = rpn_stack.pop(), rpn_stack.pop()
                rpn_stack.append(handler.operator(operand_1, operand_2))
            except ZeroDivisionError:
                raise ArithmeticError('Division by zero')
            except IndexError:
                raise ArithmeticError('Calculation error')
    try:
        result = rpn_stack.pop()
    except IndexError:
        raise ArithmeticError('Calculation error')
    if rpn_stack:
            raise ArithmeticError("Calculation error")
    return result


def calculator(expression: str, modules=()):
    _import_modules(*modules, 'math', 'builtins')
    expression = _prepare_expression(expression)
    tokens_expression = _tokenize(expression)
    tokens_expression = _find_unary(tokens_expression)
    rpn_expression = _make_rpn(tokens_expression)
    return _rpn_calculate(rpn_expression)

