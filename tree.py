#!/usr/bin/python

"""
AVL Tree - a self balancing BST
David Weinberger (davidtweinberger@gmail.com)
Brown University '16
01/07/2015

Description:

This is an implementation of a balanced binary search tree with 
the following external methods:
	1. insert(data) 				inserts data into the tree, if it is not already
	2. contains(data) 				returns True if the data is in the tree
	3. remove(data) 				removes data if it is in the tree
	4. __str__() <---> print 		pretty-prints the tree (for testing)

The rest are internal routines used to maintain the requirements
of an AVL tree.
"""
class AVL_tree:
	#Inner node class
	class AVL_node:
		"""
		Node class to be used in the tree.
		Each node has a balance factor attribute representing 
		the longest downward path rooted at the node.
		"""
		def __init__(self, data=None, left=None, right=None, balance=0, parent=None):
			self.data = data
			self.left = left
			self.right = right
			self.parent = parent

			#used to balance the tree: balance = height(left subtree) - height(right subtree)
			#tree at node is balanced if the value is in [-1, 0, 1], else it is unbalanced
			self.balance = balance 
			return

	def __init__(self):
		self._root = None
		self._depth = None
		self._max_chars = None
		return

	def __str__(self):
		"""
		Traverses and prints the binary tree in an organized and pretty way.
		Uses a BFS (level-order) traversal.
		"""
		self.synchronizeFields()
		if (self._depth == 0):
			return ""
		s = ""
		queue = []
		level = 0
		queue.append((1, self._root))
		while len(queue):
			nodelev, node = queue.pop(0)
			if (not node):
				if ((self._depth - nodelev + 1) <= 0):
					continue
				if (nodelev != level):
					s += "\n"
					s += " "*int((self._max_chars)*(2**(self._depth - nodelev) - 1))
					level = nodelev
				s += " "*(self._max_chars)*(2**(self._depth - nodelev + 1) - 1)
				s += " "*self._max_chars
				queue.append((nodelev + 1, None))
				queue.append((nodelev + 1, None))
				continue
			if (nodelev != level):
				s += "\n"
				s += " "*(self._max_chars)*(2**(self._depth - nodelev) - 1)
				level = nodelev
			for i in range(int(self._max_chars - len(str(node.data)))):
				s += "|"
			s += str(node.data) 
			s += " "*(self._max_chars)*(2**(self._depth - nodelev + 1) - 1)
			if node.left:
				queue.append((nodelev + 1, node.left))
			else:
				queue.append((nodelev + 1, None))
			if node.right:
				queue.append((nodelev + 1, node.right))
			else:
				queue.append((nodelev + 1, None))
		s += "\n"
		return s

	def synchronizeFields(self):
		"""
		Calculates depth and max_chars of the tree
		"""
		if (not self.getRoot()):
			self._depth = 0
			self._max_chars = 1
			return
		self._depth = 0
		self._max_chars = 1
		Q = []
		Q.append((self.getRoot(), 1, len(str(self.getRoot().data))))
		while len(Q):
			node, depth, chars = Q.pop(0)
			self._depth = max(self._depth, depth)
			self._max_chars = max(self._max_chars, chars)
			if node.left:
				Q.append((node.left, depth + 1, len(str(node.left.data))))
			if node.right:
				Q.append((node.right, depth + 1, len(str(node.right.data))))
		return

	def getRoot(self):
		return self._root

	def setRoot(self, node):
		self._root = node

	def contains(self, data):
		"""
		External method used to search the tree for a data element.
		"""
		return True if self.recursiveContains(data, self.getRoot()) else False

	def recursiveContains(self, data, node):
		"""
		Internal method used to recursively search for data elements
		"""
		if not node:
			return None
		elif node.data == data:
			return node
		elif data > node.data:
			return self.recursiveContains(data, node.right)
		elif data < node.data:
			return self.recursiveContains(data, node.right)

	def insert(self, data):
		"""
		This is the external insert method for the data structure.
		Args:
			data: a data object to be inserted into the tree
		"""
		if (data == None):
			return 
		if (not self.getRoot()):
			self.setRoot(AVL_tree.AVL_node(data=data))
			return
		else:
			self._done = 0
			self.recursiveInsert(self.getRoot(), data)
			delattr(self, "_done")
			return

	def recursiveInsert(self, node, data):
		"""
		This is an internal method used to insert data elements 
		recursively into the tree.
		"""

		#no duplicates in the tree
		if (data == node.data):
			return

		if data < node.data:
			if node.left:
				self.recursiveInsert(node.left, data)
			else:
				node.left = AVL_tree.AVL_node(data=data, parent=node)
				self.updateBalance(node.left)
		else:
			if node.right:
				self.recursiveInsert(node.right, data)
			else:
				node.right = AVL_tree.AVL_node(data=data, parent=node)
				self.updateBalance(node.right)
		return

	def updateBalance(self, node):
		"""
		Balances the tree starting with a newly inserted node (node)
		"""
		if (node.balance > 1 or node.balance < -1):
			self.rebalance(node)
			return
		if node.parent:
			if node.parent.left is node: #lchild
				node.parent.balance += 1
			elif node.parent.right is node: #rchild
				node.parent.balance -= 1

			#recurses to the parent
			if node.parent.balance != 0:
				self.updateBalance(node.parent)

	def rotateLeft(self, node):
		"""
		Performs a left rotation.
		"""
		print "rotating left around: " + str(node.data)
		newRootNode = node.right
		node.right = newRootNode.left
		if (newRootNode.left):
			newRootNode.left.parent = node
		newRootNode.parent = node.parent
		if node is self.getRoot():
			self.setRoot(newRootNode)
		else:
			if node.parent.left is node:
				node.parent.left = newRootNode
			else:
				node.parent.right = newRootNode
		newRootNode.left = node
		node.parent = newRootNode
		node.balance = node.balance + 1 - min(newRootNode.balance, 0)
		newRootNode.balance = newRootNode.balance + 1 + max(node.balance, 0)

	def rotateRight(self, node):
		"""
		Performs a right rotation.
		"""
		print "rotating right around: " + str(node.data)
		newRootNode = node.left
		node.left = newRootNode.right
		if (newRootNode.right):
			newRootNode.right.parent = node
		newRootNode.parent = node.parent
		if node is self.getRoot():
			self.setRoot(newRootNode)
		else:
			if node.parent.right is node:
				node.parent.right = newRootNode
			else:
				node.parent.left = newRootNode
		newRootNode.right = node
		node.parent = newRootNode
		node.balance = node.balance - 1 - max(newRootNode.balance, 0)
		newRootNode.balance = newRootNode.balance - 1 + min(node.balance, 0)

	def rebalance(self, node):
		"""
		Performs the tree rotations to rebalance the tree.
		"""
		if node.balance < 0:
			if node.right.balance > 0:
				self.rotateRight(node.right)
				self.rotateLeft(node)
			else:
				self.rotateLeft(node)
		elif node.balance > 0:
			if node.left.balance < 0:
				self.rotateLeft(node.left)
				self.rotateRight(node)
			else:
				self.rotateRight(node)

def main():
	pass

if __name__ == '__main__':
	main()
