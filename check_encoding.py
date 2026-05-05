with open('index.html', 'rb') as f:
    b = f.read(10)
    print(' '.join(f'{x:02x}' for x in b))
    print('Encoding guess:')
    if b[0:2] == b'\xff\xfe':
        print('UTF-16 LE')
    elif b[0:2] == b'\xfe\xff':
        print('UTF-16 BE')
    elif b[0:3] == b'\xef\xbb\xbf':
        print('UTF-8 with BOM')
    else:
        print('Unknown or plain ASCII/UTF-8')
