

def strict(func):
    def wrap(*args, **kwargs):
        annots = func.__annotations__
        for arg_name, arg_value in zip(annots, args):
            expected_type = annots[arg_name]
            if not isinstance(arg_value, expected_type):
                raise TypeError(
                    f"Аргумент '{arg_name}' имеет тип {type(arg_value).__name__}."
                )
        return func(*args, **kwargs)
    return wrap


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


def main() -> None:
    print(sum_two(1, 2))
    print(sum_two(1, 2.4))
    
    
if __name__ == "__main__":
    main()
