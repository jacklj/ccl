"""
	Disjoint-set data structure
	Jack Lawrence-Jones, July 2016

	A structure that maintains a collection of disjoint sets (no sets share items - each 
	possible pair of sets' has intersection {}).

	Implemented as a forest (n disjointed trees), using union-by-rank and path compression.
	
	Naive implementation:
		MakeSet: O(1)
		Find: O(n) worst case
		Union: O(n) (because it performs 2 Find operations)

	With union-by-rank (create balanced trees):
		Find: O(log(n)) worst case
		Union: O(log(n)) worst case

	Also with path compression:
		Find: O(log*(n))
		Union: O(log*(n))
		(Amortized complexity (averaged over all operations performed) is effectively O(1))

	N.B. Rank (of a tree):
		A measure/score of the size/depth of a tree (can't use depth due to path compression), 
		calculated as follows:
			1. A tree containing only one node has rank 0
			2. Performing the union of 2 trees with the same rank (r) produces a tree with rank 
			   r+1
		The tree's rank is stored in the root node's rank.
"""

# Private classes/methods/state ################################################################
all_nodes_addressed_by_value = {} # to keep track of nodes


def getNode(value): # get node with value 'value' (O(1))
	if value in all_nodes_addressed_by_value:
		return all_nodes_addressed_by_value[value]
	else:
		return False


class Node(object):
	"""
		Private tree node class.

		Node:
			value: the node's value
			parent: reference to the node's parent
			rank: the rank of the tree (only used if node is a root)

	"""
	# constructor
	def __init__(self, value):
		self.value = value
		self.parent = self # node is its own parent, therefore it's a root node
		self.rank = 0 # tree of single node has rank 0

		# keep track of node
		all_nodes_addressed_by_value[value] = self

	# print format for debugging
	def __str__(self):
		st = "[value: " + str(self.value) + ", parent: " + str(self.parent.value) 
		st += ", rank: " + str(self.rank) +  "]"
		return st



# Required disjoint-set operations #############################################################
def MakeSet(value):
	"""
		MakeSet(value):
			Makes a new set containing one node (with value 'value').
	"""
	
	# Modification to classic disjoint-set behaviour: if node already exists, return it
	if getNode(value):
		# print("Node with value '" + str(value) + "' already exists.")
		return getNode(value)

	# otherwise create node
	node = Node(value)
	return node


def Find(x):
	"""
		Find(Node x):
			Returns the representative node of the set containing node x.
			By recursively getting the node's parent.

		Optimisation using path compression: 
			Once you've found the root of the tree, set each visited node's parent to the root, 
			therefore flattening the tree along that path, speeding up future operations.
			This is only a constant time complexity increase, but means future Find operations 
			along the same path are O(1).

	"""

	# Node is not its own parent, therefore it's not the root node.
	if x.parent  != x:  
		x.parent = Find(x.parent) # Flatten tree as you go (Path Compression)
	
	# If node is its own parent, then it is the root node -> return it.
	return x.parent


def Union(x,y):
	"""
		Union(Node x, Node y):
			Performs a union on the two sets containing nodes x and y.
			Gets the representative nodes of x's and y's respective containing sets, and makes 
			one of them the other's parent (depending on their rank).

		Optimisation using union-by-rank:
			Always add the lower ranked tree ('smaller') to the larger one, ensuring no increase 
			in tree depth. If the two trees have the same rank, the depth will increase by one 
			(worst case). Without union-by-rank, each union operation is much more likely to 
			cause an increase in tree depth.

	"""

	# if x and y are the same node, do nothing.
	if x == y:
		return

	# Get the roots of both nodes' containing trees (= the representative elements of each of 
	# their containing sets)
	x_root = Find(x)
	y_root = Find(y)

	# If x and y are already members of the same set, do nothing.
	if x_root == y_root:
		return

	# Perform set union.
	# Union-by-rank optimisation: always add 'smaller' tree to 'larger' tree.
	if x_root.rank > y_root.rank: 
		# x_root has larger rank ('bigger' tree), so add y to x.
		y_root.parent = x_root

	elif x_root.rank < y_root.rank: 
		# y_root hes larger rank, so add x to y.
		x_root.parent = y_root

	else: 
		# x_root and y_root have same rank (same 'sized' trees).
		# Therefore add one tree to other arbitrarily and increase the resulting tree's rank 
		# score by one.
		x_root.parent = y_root
		y_root.rank = y_root.rank + 1

	# Could update all children nodes to flatten list? Will still be O(3n) = O(n) -> why not?



# Debugging functions ##########################################################################
def display_all_nodes():
	print("All nodes:")
	for item in all_nodes_addressed_by_value.values():
		print(item)


def display_all_sets():
	sets = {} # initialise so nodes can't be added twice

	# Add all nodes to set dictionary 
	# 	keys: representative items
	#	values: all items with that representative)
	for item in all_nodes_addressed_by_value.values():
		if Find(item).value not in sets.keys():
			sets[Find(item).value] = [] # initialise list for this key
		sets[Find(item).value].append(item)

	# 2. Display each representative key's set of items 
	st = ""
	for representative in sets.keys():
		st = st +  "("
		for item in sets[representative]:
			st = st + str(item.value) + ","
		st = st[:-1] # remove final ','
		st = st + ") "

	print(st)


# Testing ######################################################################################
# to do: proper test cases.

# [1 2 3] [4]
# one = MakeSet(1)
# MakeSet(1) # try and make a node with same value
# two = MakeSet(2)
# three = MakeSet(3)
# four = MakeSet(4)

# Union(two, one)
# Union(two, three)

# display_all_nodes()
# print("-----")
# display_all_sets()
