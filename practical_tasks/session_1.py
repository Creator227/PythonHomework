import typing
from typing import Tuple, List, Optional


def replace_symbols(input_message: str) ->str:
    """Replaces symbols " with ' and vice versa."""
    return input_message.translate(input_message.maketrans({"'":'"','"':"'"}))


def palindrom_check(input_message: str) ->bool:
    for i in range(len(input_message) // 2):
        if input_message[i] != input_message[-i-1]:
            return False
    return True


def my_split(input_message: str) -> List[str]:
    word = ''
    splited_message = list()
    for i in range(len(input_message)):
        if input_message[i] != ' ':
            word += input_message[i]
        elif word:
            splited_message.append(word)
            word = ''
    if word:
        splited_message.append(word)
    return splited_message


def split_by_index(input_message: str, index_list: List[int]) -> List[str]:
    start = 0
    index_list.append(len(input_message))
    index_list.sort()
    splited_message = list()
    for finish in index_list:
        if finish > len(input_message):
            break
        splited_message.append(input_message[start:finish])
        start = finish
    return splited_message


def get_digits(num: int) -> Tuple[int]:
    return tuple(int(digit) for digit in str(num))


def get_shorted_words(input_message: str) -> str:
    '''Returns the shortest word in inputed message.'''
    words = input_message.split(' ')
    return min(words, key= len)


def foo(num_array: List[int]) -> List[int]:
    new_num_array = list()
    '''Returns to each position the product of all array elements except the element on position itself.'''
    for i in range(len(num_array)):
        mult = 1
        for j in range(len(num_array)):
            if j != i:
                mult *= num_array[j]
        new_num_array.append(mult)
    return new_num_array


def get_pairs(lst: List) -> Optional[List[Tuple]]:
    '''Returns all pairs in list'''
    output_list = list()
    if len(lst) < 2:
        return None
    for i in range(len(lst) - 1):
        output_list.append((lst[i], lst[i+1]))
    return output_list


