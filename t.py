import re

def rating_map(value):
    review_num = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
    }

    return review_num.get(value)


a = rating_map('One')
print(type(a))