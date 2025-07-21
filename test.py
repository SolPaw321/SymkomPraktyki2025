from beartype import beartype as check_input_types

@check_input_types
def f(x: int):
    print(x)


f(432.0)