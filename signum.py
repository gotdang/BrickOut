# Python doesn't have a built-in sign function, so we'll make one.
# https://thingspython.wordpress.com/2011/03/12/snippet-sgn-function/
# https://stackoverflow.com/questions/1986152/why-doesnt-python-have-a-sign-function/1986776
def signum(x: int) -> int:
    return (x>0) - (x<0)
