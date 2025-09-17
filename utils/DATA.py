n = 10
x = 1
y = 1
while n > 0:
    print(x^2 + y^2 + x*y)
    if x == y:
        x += 1
    else:
        y += 1
    n -= 1