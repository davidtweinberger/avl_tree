# avl_tree
A python implementation of the AVL Tree (a self-balancing binary tree)

Description:

This is an implementation of a balanced binary search tree with 
the following external methods:
 1. __insert__(data) inserts data into the tree, if it is not already contained in the tree
 2. __insertList__(list) inserts data elements from list into the tree by iterating and calling __insert__
 3. __contains__(data) returns True if the data is in the tree, False otherwise
 4. __str__() pretty-prints the tree (for testing purposes) using a BFS traversal

The rest are internal routines used to maintain the requirements
of an AVL tree.

To test the tree, navigate to the avl_tree directory in a shell and type:
```
$ python
```
to enter the python interpreter. (Make sure the path to the interpreter - usually /usr/local/bin/python is in the shell's path).
Then type:
```
>>> from tree import *
```
to import the classes from tree.py.
Test the tree using something along these lines:
```
>>> tree = AVL_tree()
>>> tree.insert(1)
>>> tree.insert(2)
>>> tree.insert(199)
>>> print tree
...
>>> print tree.contains(1)
True
>>> print tree.contains(3)
False
```
etc.  You can also add elements from a list to the tree using insertList().

