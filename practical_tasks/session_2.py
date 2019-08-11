from typing import List, Set
import string


#Task 1.1
def in_all(*args: str) -> Set[str]:
    words = [set(word) for word in args]
    return words[0].intersection(*words) if args else None

def at_least_one(*args: str) -> Set[str]:
    return set().union(*args) if args else None

def min_in_two(*args: str) -> Set[str]:
    alphabet = dict()
    for letter in string.ascii_lowercase:
        alphabet[letter] = 0
    for word in args:
        for letter in word:
            alphabet[letter] +=1
    return {let for let in alphabet.keys() if alphabet[let] > 1} if args else None

def not_in_args(*args: str) -> Set[str]:
    return set(string.ascii_lowercase).difference(*args) if args else None


#Task 1.2
def make_dict(num: int) -> dict:
    return {i: i**2 for i in range(1, num)}


#Task 1.3
def count_letters(phrase: str) -> dict:
    answer = dict()
    for let in phrase:
        if answer.get(let):
            answer[let] += 1
        else:
            answer[let] = 1
    return answer

#Task 1.4
def combine_dicts(*args) -> dict:
    if not args:
        return None
    sum_dict = args[0]
    for new_dict in args[1:]:
        for key in new_dict.keys():
            sum_dict.setdefault(key, 0)
            sum_dict[key] += new_dict[key]
    return sum_dict

#Task 1.5
def call_once(function):
    flag = True
    result = None
    def wrapper(*args, **kwargs):
        nonlocal flag, result
        if flag:
            result = function(*args, **kwargs)
            flag = False
        return result
    return wrapper
