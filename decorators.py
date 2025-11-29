# def print_kwargs(**kwargs):
#     return kwargs

# print(print_kwargs(kwarg1=1, kwarg2=2, kwarg3=3))
# print(print_kwargs(kwarg5=5, kwarg6=6))

# def print_args(*args):
#     return args

# print(print_args(1,2,3,4))
# print(print_args(5,6))

# def print_args_kwargs(*args, **kwargs):
#     print(args)
#     print(kwargs)

# print_args_kwargs(1, 2, 3, 4, kwarg1=1, kwarg2=2)

import functools

logged_in = False

def print_args(func):
    @functools.wraps(func)
    def decorator_wrapper(*args):
        print(func.__name__)

        for idx, e in enumerate(args):
            print(f'{idx}: {e}')

        return func(*args)
    
    return decorator_wrapper


def auth_logged_in(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        if logged_in == False:
            return print('Please login to preform this action')
        else:
            return func(*args, **kwargs)
        
    return decorator_wrapper


@auth_logged_in
@print_args
def sum_num(*args):
    return sum(list(args))


@print_args
def concatenate_str(*args):
    return ' '.join(args)


@print_args
def sort_list(*args):
    return sorted(list(args))


# print(sum_num(1,2,3))
# print(concatenate_str("hello", "world"))
# print(sort_list(32, 14, 27, 60))


def only_strings(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                kwargs[key] = str(value)

        if args:
            new_list = args[0]

            for idx, e in enumerate(new_list):
                new_list[idx] = str(e)

            args = (new_list,)


        return func(*args, **kwargs)
    
    return decorator_wrapper


@only_strings
def string_joined(list_of_strings):
    new_list = list_of_strings

    return ", ".join(new_list)


@only_strings
def convert_to_str(**kwargs):
    new_list = []
    for key, val in kwargs.items():
        new_list.append(val)
    
    return ", ".join(new_list)

lst = ['one', 'two', 'three', 'four', 'five', 6]
joined_string = convert_to_str(kw1=1,kw2=2,kw3=3,kw4='four')

# print(lst)
# print(string_joined(lst))
print(joined_string)

