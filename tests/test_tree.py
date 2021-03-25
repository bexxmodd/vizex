# add path to the main package and test bstree.py
from access import ADD_PATH
ADD_PATH()


import unittest

from bstree import Node, BinarySearchTree

class TestDirectoryFiles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tree = BinarySearchTree()
        cls.tree.add("dog")
        cls.tree.add("cat")
        cls.tree.add("pig")

        # right-sided tree
        cls.righty = BinarySearchTree()
        cls.righty.add(5)
        cls.righty.add(3)
        cls.righty.add(11)
        cls.righty.add(7)
        cls.righty.add(2)
        cls.righty.add(1)

        # right-sided tree
        cls.lefty = BinarySearchTree()
        cls.lefty.add(5);
        cls.lefty.add(3);
        cls.lefty.add(7);
        cls.lefty.add(11);
        cls.lefty.add(9);
        cls.lefty.add(1);
        cls.lefty.add(4);

    def test_depth_root(self):
        try:
            var1 = self.tree.depth("dog")
            self.assertEqual(0, var1, 
            "BinarySearchTree.depth returns incorrect value when input value is root")
        except Exception as e:
            self.fail(f'Exception was thrown: {e}')

    def test_depth_left_of_root(self):
        try:
            var1 = self.tree.depth("cat")
            self.assertEqual(1, var1, 
            "BinarySearchTree.depth returns incorrect value when input value is left child of root")
        except Exception as e:
            self.fail(f'Exception was thrown: {e}')

    def test_depth_right_of_root(self):
        try:
            var1 = self.tree.depth("pig")
            self.assertEqual(1, var1, 
            "BinarySearchTree.depth returns incorrect value when input value is right child of root")
        except Exception as e:
            self.fail(f'Exception was thrown: {e}')

    def test_depth_value_na(self):
        try:
            var1 = self.tree.depth("sparrow")
            self.assertEqual(-1, var1, 
            "BinarySearchTree.depth returns incorrect value when input value is right child of root")
        except Exception as e:
            self.fail(f'Exception was thrown: {e}')

    def test_right_sided_tree(self):
        try:
            
            var1 = self.righty.depth(2)
            self.assertEqual(2, var1)
        except Exception as e:
            self.fail(f'Exception was thrown: {e}')

    def test_left_sided_tree(self):
        try:
            var1 = self.lefty.depth(9)
            self.assertEqual(3, var1)
        except Exception as e:
            self.fail(f'Exception was thrown: {e}')

    def test_find_root(self):
        try:
            var = self.tree.find_node('dog')
            if not var:
                self.fail("BinarySearchTree.findNode returned null when looking for value that is root");
            self.assertEqual(var.value, 'dog')
        except Exception as e:
            self.fail(f"BinarySearchTree.findNode throws exception when target is root: {e}")

    def test_find_left_child(self):
        try:
            var = self.tree.find_node('cat')
            if not var:
                self.fail("BinarySearchTree.findNode returned null when looking for value that is left child of root");
            self.assertEqual(var.value, 'cat')
        except Exception as e:
            self.fail(f"BinarySearchTree.findNode throws exception when target is left child of root: {e}")

    def test_find_right_child(self):
        try:
            var = self.tree.find_node('pig')
            if not var:
                self.fail("BinarySearchTree.findNode returned null when looking for value that is right child of root");
            self.assertEqual(var.value, 'pig')
        except Exception as e:
            self.fail(f"BinarySearchTree.findNode throws exception when target is right child of root: {e}")

    def test_find_value_na(self):
        try:
            var = self.tree.find_node('bird')
            self.assertIsNone(var)
        except Exception as e:
            self.fail(f"BinarySearchTree.findNode throws exception when target is not found: {e}")


    def test_leaf(self):
        try:
            var = self.tree.height('cat')
            self.assertEqual(0, var)
        except Exception as e:
            self.fail(f'Exception was thrown: {e}')

    def test_parent_of_leaves(self):
        try:
            var = self.tree.height('dog')
            self.assertEqual(1, var)
        except Exception as e:
            self.fail(f'Exception was thrown: {e}')

    def test_height_value_na(self):
        try:
            var = self.tree.height('sparrow')
            self.assertEqual(-1, var)
        except Exception as e:
            self.fail(f'Exception was thrown: {e}')

    def test_height_right_sided(self):
        try:
            var = self.righty.height(11)
            self.assertEqual(1, var)
        except Exception as e:
            self.fail(f'Exception was thrown: {e}')


if __name__ == '__main__':
    unittest.main()