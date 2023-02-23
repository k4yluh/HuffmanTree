# Implements a Huffman tree.
# CSC 202, Project 3
# Given code, Summer '19

import array_list as ulist
import sorted_list as slist


class HuffmanTree:
    """
    A Huffman tree
    NOTE: Do not alter this class.
    """

    def __init__(self):
        # The root of this tree:
        self.root = None
        # The number of nodes in this tree:
        self.size = 0

    def __eq__(self, other):
        return (type(other) == HuffmanTree
                and self.root == other.root
                and self.size == other.size)

    def __repr__(self):
        return "HuffmanTree(%r, %d)" % (self.root, self.size)


class Node:
    """
    A single node in a Huffman tree
    NOTE: Do not alter this class.
    """

    def __init__(self, char, freq, left, right):
        # The character contained in this node:
        self.char = char
        # The frequency of the character:
        self.freq = freq
        # The left child of this node:
        self.left = left
        # The right child of this node:
        self.right = right

    def __eq__(self, other):
        return (type(other) == Node
                and self.char == other.char
                and self.freq == other.freq
                and self.left == other.left
                and self.right == other.right)

    def __lt__(self, other):
        if type(other) != Node:
            raise TypeError
        else:
            return self.freq < other.freq \
                   or (self.freq == other.freq and self.char < other.char)

    def __repr__(self):
        return "Node(%r, %r, %r, %r)" \
               % (self.char, self.freq, self.left, self.right)


def combine(left, right):
    """
    Combine two nodes with a common parent.
    TODO: Implement this function. It must have O(1) complexity.

    :param left: A smaller Node to use as a left subtree
    :param right: A larger Node to use as a right subtree
    :return: A new Node combining the left and right
    """
    if left.char < right.char:
        new = Node(left.char, left.freq + right.freq, left, right)
    else:
        new = Node(right.char, left.freq + right.freq, left, right)
    return new


def build(chars):
    """
    Build a Huffman tree from characters and their frequencies.
    TODO: Implement this function. It must have O(n^2) complexity.

    :param chars: A List of (character, frequency) pairs
    :return: A new HuffmanTree containing the characters and their frequencies
    """
    tree = HuffmanTree()
    s_lst = slist.SortedList()
    count = 0
    for i in range(chars.size):
        n = Node(chars.array[i][0], chars.array[i][1], None, None)
        slist.insert(s_lst, n)
        count += 1
    while s_lst.size > 1:
        left = slist.remove(s_lst, 0)
        right = slist.remove(s_lst, 0)
        new = combine(left, right)
        slist.insert(s_lst, new)
        count += 1
    if s_lst.size == 1:
        tree.root = s_lst.array[0]
        tree.size = count
        return tree
    elif s_lst.size == 0:
        return tree


def encode_helper(tree, char, bit):
    if tree.root is None:
        raise ValueError
    elif tree.size == 1 and tree.root.char != char:
        raise ValueError
    elif tree.size == 1 and tree.root.char == char:
        return bit
    # if tree.root.char == char:
    #     return bit
    if tree.root.left is None and tree.root.right is None and tree.root.char == char:
        bit = bit + "!"
        return bit
    elif tree.root.left is None and tree.root.right is None and tree.root.char != char:
        bit = bit + "X"
        return bit
    else:
        left = HuffmanTree()
        left.root = Node(tree.root.left.char, tree.root.left.freq, tree.root.left.left, tree.root.left.right)
        lbit = bit + "0"
        l = encode_helper(left, char, lbit)
        for i in l:
            if i == "!":
                return l
            elif i == "X":
                right = HuffmanTree()
                right.root = Node(tree.root.right.char, tree.root.right.freq, tree.root.right.left, tree.root.right.right)
                rbit = bit + "1"
                r = encode_helper(right, char, rbit)
                for e in r:
                    if e == "!":
                        return r
                    elif e == "X" and bit != "":
                        return r
                    elif e == "X" and bit == "":
                        raise ValueError


def encode(tree, char):
    """
    Encode a character using a Huffman tree.
    TODO: Implement this function. It may have up to O(n^2) complexity.

    :param tree: A HuffmanTree
    :param char: A character
    :return: The bistring encoding the character in the tree
    :raise ValueError: If the character is not encoded by any bitstring
    """
    bit = ""
    code = encode_helper(tree, char, bit)
    code = code.replace('!', '', 1)
    return code


def decode(tree, code):
    """
    Decode a code using a Huffman tree.
    TODO: Implement this function. It may have up to O(n^2) complexity.

    :param tree: A HuffmanTree
    :param code: A bitstring
    :return: The character encoded by the bitstring in the tree
    :raise ValueError: If the bistring does not encode any character
    """
    if tree.root is None:
        raise ValueError
    elif tree.root.left is None and tree.root.right is None and code == "":
        return tree.root.char
    elif tree.root.left is None and tree.root.right is None and code != "":
        raise ValueError
    elif (tree.root.left is not None or tree.root.right is not None) and code == "":
        raise ValueError
    if code[0] == '0':
        new_code = code.replace('0', '', 1)
        new_tree = HuffmanTree()
        new_tree.root = Node(tree.root.left.char, tree.root.left.freq, tree.root.left.left, tree.root.left.right)
        return decode(new_tree, new_code)
    elif code[0] == '1':
        new_code = code.replace('1', '', 1)
        new_tree = HuffmanTree()
        new_tree.root = Node(tree.root.right.char, tree.root.right.freq, tree.root.right.left, tree.root.right.right)
        return decode(new_tree, new_code)
