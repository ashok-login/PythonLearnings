def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as error:
        raise ValueError("Cannot divide by zero") from error