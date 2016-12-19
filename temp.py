def a(a, b='1', c=2, *args, **kargs):
    print(a, b, c)
    print(args)
    print(kargs)

a(a='1')
