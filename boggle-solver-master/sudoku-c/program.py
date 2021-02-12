tree = [[['n', 't'], [['i', 'o'], [' ', '']]], ['e', ['h', 'r']]]

def is_leaf(node):
    return isinstance(node, str)

def find_leaf(encoded, tree):
    i = 0
    while not get_left(tree) == get_right(tree):
        if (encoded[i] == '0'):
            tree = get_left(tree)
        if (encoded[i] == '1'):
            tree = get_right(tree)
        i = i + 1
        
    return (tree, encoded[i:])

def get_left(node):
    return node[0] if isinstance(node, list) else None

def get_right(node):
    return node[1] if isinstance(node, list) else None

def decode(encoded, tree):
    (leaf, encoded) = find_leaf(encoded, tree)
    message = str(leaf)
    while len(encoded):
        (leaf, encoded) = find_leaf(encoded, tree)
        message += leaf
    return message

print(decode("0001001000111001110101110110110101111001100000101111011000111010111100111", tree))
print("test" + tree[0][1][1][1] + "test")

