from bencode import Bencode, BencodeParseException

bdecode = Bencode()
test_stings = ['2:qw', '0:', '12:qwertyqwerty']
test_ints = ['i2e', 'i-2e', 'i0e']
test_lists = ['l2:qw2:ace', 'le', 'll2:qw2:ace2:qwe']
test_dicts = ['d5:emptyldee3:kekll0:12:приветi2eed1:ai1eei1e8:покаe3:lold1:1i0e1:3li1ei2e1:cd1:ai1eeeee']
test_errors = ['ie', '2:qer', 'lte']

print('Testing strings:')
for test in test_stings:
    print(test, '-->', bdecode.decode(test))

print('\nTesting ints:')
for test in test_ints:
    print(test, '-->', bdecode.decode(test))

print('\nTesting lists:')
for test in test_lists:
    print(test, '-->', bdecode.decode(test))

print('\nTesting dicts:')
for test in test_dicts:
    print(test, '-->', bdecode.decode(test))

print('\nTesting error:')
for test in test_errors:
    try:
        bdecode.decode(test)
    except BencodeParseException as e:
        print('exception: ', str(e))
        continue
