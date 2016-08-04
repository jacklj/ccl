"""
	Node class for Disjoint-set data structure with Union-Find algorithms
	----------------------------------------------------------------------
	Jack Lawrence-Jones, July 2016
"""

class Node(object):
	"""
		Private tree node class.

		Node:
			value: the node's value
			parent: reference to the node's parent
			rank: the rank of the tree (only valid if node is a root)
	"""
	# Constructor
	def __init__(self, value):
		self.value = value
		self.parent = self # Node is its own parent, therefore it's a root node
		self.rank = 0 # Tree of single node has rank 0

	# Print format for debugging
	def __str__(self):
		st = "[value: " + str(self.value) + ", parent: " + str(self.parent.value) 
		st += ", rank: " + str(self.rank) +  "]"
		return st