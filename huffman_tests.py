# Tests Huffman coding functions.
# CSC 202, Project 3
# Given tests, Summer '19

import unittest

from array_list import List, add
from huffman_tree import *


class TestHuffman(unittest.TestCase):
    def test01_methods(self):
        msg = "Testing Huffman tree equality and representation"

        tree = HuffmanTree()
        tree.root = Node('a', 8, None, None)
        tree.size = 1

        self.assertEqual(tree, tree, msg)
        self.assertEqual(repr(tree),
                         "HuffmanTree(Node('a', 8, None, None), 1)", msg)

        self.assertFalse(tree.root < tree.root, msg)
        with self.assertRaises(TypeError):
            tree.root < ('t', 9)

    def test02_combine(self):
        msg = "Testing combining Huffman nodes"

        left = Node('a', 8, None, None)
        right = Node('t', 9, None, None)
        soln = \
            Node('a', 17,
                 Node('a', 8, None, None),
                 Node('t', 9, None, None))

        self.assertEqual(combine(left, right), soln, msg)

    def test03_build(self):
        msg = "Testing building Huffman trees"

        chars = List()
        add(chars, 0, ('e', 13))
        add(chars, 1, ('t', 9))
        add(chars, 2, ('a', 8))

        soln = HuffmanTree()
        soln.root = \
            Node('a', 30,
                 Node('e', 13, None, None),
                 Node('a', 17,
                      Node('a', 8, None, None),
                      Node('t', 9, None, None)))
        soln.size = 5

        self.assertEqual(build(chars), soln, msg)

    def test04_encode(self):
        msg = "Testing encoding using Huffman trees"

        tree = HuffmanTree()
        tree.root = \
            Node('a', 30,
                 Node('e', 13, None, None),
                 Node('a', 17,
                      Node('a', 8, None, None),
                      Node('t', 9, None, None)))
        tree.size = 5

        self.assertEqual(encode(tree, 'a'), "10", msg)

    def test05_decode(self):
        msg = "Testing decoding using Huffman trees"

        tree = HuffmanTree()
        tree.root = \
            Node('a', 30,
                 Node('e', 13, None, None),
                 Node('a', 17,
                      Node('a', 8, None, None),
                      Node('t', 9, None, None)))
        tree.size = 5

        self.assertEqual(decode(tree, "10"), 'a', msg)

    def test06_more_decode(self):
        msg = "Testing more cases of decoding using Huffman trees"

        tree = HuffmanTree()
        tree.root = \
            Node('a', 30,
                 Node('e', 13, Node('a', 10, Node('n', 6, None, None), Node('k', 4, None, None)),
                      Node('t', 3, None, None)),
                 Node('a', 17,
                      Node('a', 8, None, None),
                      Node('t', 9, None, None)))
        tree.size = 9

        self.assertEqual(decode(tree, "001"), 'k', msg)
        self.assertEqual(decode(tree, "000"), 'n', msg)

    def test07_build_none(self):
        msg = "Testing building a tree: empty tree"

        chars = List()

        soln = HuffmanTree()
        self.assertEqual(build(chars), soln, msg)

    def test08_empty(self):
        msg = "Testing encoding an empty tree: ERROR"

        soln = HuffmanTree()
        with self.assertRaises(ValueError):
            encode(soln, 'a')

    def test085_empty(self):
        msg = "Testing decoding an empty tree: ERROR"

        tree = HuffmanTree()
        tree.size = 0
        with self.assertRaises(ValueError):
            decode(tree, "1")

    def test09_root_only(self):
        msg = "Testing encoding a tree with a size of one"

        tree = HuffmanTree()
        tree.root = \
            Node('a', 30, None, None)
        tree.size = 1

        self.assertEqual(encode(tree, 'a'), "", msg)

    def test0925_root_only(self):
        msg = "Testing encoding a tree with a size of one: ERROR"

        tree = HuffmanTree()
        tree.root = \
            Node('a', 30, None, None)
        tree.size = 1

        with self.assertRaises(ValueError):
            encode(tree, 'b')

    def test95_one_bit(self):
        msg = "Testing decoding a single bit"
        tree = HuffmanTree()
        tree.root = \
            Node('a', 30,
                 Node('e', 1, None, None),
                 Node('a', 17,
                      Node('a', 8, None, None),
                      Node('t', 9, None, None)))
        tree.size = 9
        self.assertEqual(decode(tree, "0"), 'e', msg)

    def test975_build_one(self):
        msg = "Testing building: only one node"
        chars = List()
        add(chars, 0, ('a', 30))
        tree = HuffmanTree()
        tree.root = \
            Node('a', 30, None, None)
        tree.size = 1

        self.assertEqual(build(chars), tree, msg)

    def test10_no_char(self):
        msg = "Testing encoding a char that does not exist: ERROR"

        tree = HuffmanTree()
        tree.root = \
            Node('a', 30,
                 Node('e', 13, Node('a', 10, Node('n', 6, None, None), Node('k', 4, None, None)),
                      Node('t', 3, None, None)),
                 Node('a', 17,
                      Node('a', 8, None, None),
                      Node('t', 9, None, None)))
        tree.size = 9

        with self.assertRaises(ValueError):
            encode(tree, "z")

    def test105_no_code(self):
        msg = "Testing decoding with only root: empty code"
        tree = HuffmanTree()
        tree.root = \
            Node('a', 30, None, None)
        tree.size = 1

        self.assertEqual(decode(tree, ""), 'a', msg)

    def test1075_no_tree(self):
        msg = "Testing building an empty tree"

        tree = HuffmanTree()
        chars = List()
        self.assertEqual(build(chars), tree, msg)

    def test11_decode_errors(self):
        msg = "Testing for decoding: value error"

        tree = HuffmanTree()
        tree.root = \
            Node('a', 30,
                 Node('e', 13, None, None),
                 Node('a', 17,
                      Node('a', 8, None, None),
                      Node('t', 9, None, None)))
        tree.size = 5

        with self.assertRaises(ValueError):
            decode(tree, "111")

        with self.assertRaises(ValueError):
            decode(tree, "1")

        with self.assertRaises(ValueError):
            decode(tree, "")

    def test12_diff_freq(self):
        msg = "Testing very different freq."
        chars = List()
        add(chars, 0, ('a', 777))
        add(chars, 1, ('k', 1))
        add(chars, 2, ('t', 1813))
        tree = build(chars)

        self.assertEqual(encode(tree, 'k'), "00", msg)
        self.assertEqual(encode(tree, 'a'), "01", msg)
        self.assertEqual(encode(tree, 't'), "1", msg)

        with self.assertRaises(ValueError):
            encode(tree, 'y')


if __name__ == "__main__":
    unittest.main()
