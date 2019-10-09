def f(x: list):
    for i in x:
        print(i)


def a() -> str:


    return []



f(x=a())


from typing import List


def a() -> List[str]:
    return [23423, 234]
