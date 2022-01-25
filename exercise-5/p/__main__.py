if __name__ == '__main__':
    import sys
    import p

    if len(sys.argv) != 2:
        print('USAGE: python -m p <module>')
    elif sys.argv[1] == 'a':
        print('created', p.A())
    elif sys.argv[1] == 'b':
        print('created', p.B())
    elif sys.argv[1] == 'c':
        print('created', p.C())
    elif sys.argv[1] == 'd':
        print('created', p.D())
    else:
        print('USAGE: python -m p <module>')