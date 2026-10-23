def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1

a = infinite_sequence()

while next(a) < 50:
    print(a)