# Assignment 1
"""
Problem: Create a List of Palindromes
You are given a list of strings. Use list comprehension to create a new list that contains only the words that are palindromes (i.e., words that read the same backwards as forward).

words = ["madam", "hello", "racecar", "world", "level", "python"]

Expected Output:
['madam', 'racecar', 'level']

"""

def palindrome_list(words):
    return [word for word in words if word == word[::-1]]

#Assignment 2
"""
Problem: Grouping by First Letter
You are given a list of strings. Use dictionary comprehension to group the strings by their first letter.
words = ["apple", "banana", "avocado", "blueberry", "cherry", "date"]

Expected Output:
{'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry'], 'c': ['cherry'], 'd': ['date']}
"""

def group_by_first_letter(words):
    return {word[0]: [w for w in words if w[0] == word[0]] for word in words}

