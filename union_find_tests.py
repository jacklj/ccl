import unittest
from union_find import UnionFind

class TestUnionFind(unittest.TestCase):

	def test_makeset(self):
		uf = UnionFind()
		three = uf.MakeSet(3) # makes a set containing one element with the value 3

		self.assertEqual(three.value, 3)
		self.assertEqual(three.parent.value, 3)
		self.assertEqual(three.rank, 0)

	def test_union(self):
		uf = UnionFind()
		five = uf.MakeSet(5)
		seven = uf.MakeSet(7)
		uf.Union(five, seven) # same rank trees, so 1st argument is added to 2nd 
							  # argument, arbitrarily

		self.assertEqual(five.rank, 0)
		self.assertEqual(seven.rank, 1)

		self.assertEqual(five.parent, seven)

	def test_find(self):
		uf = UnionFind()
		five = uf.MakeSet(5)
		seven = uf.MakeSet(7)
		uf.Union(five, seven)

		self.assertEqual(uf.Find(five), seven)
		self.assertEqual(uf.Find(seven), seven)


	def test_union_by_rank(self):
		uf = UnionFind()
		one = uf.MakeSet(1)
		two = uf.MakeSet(2)
		three = uf.MakeSet(3)

		uf.Union(one, two) # 1st added to 2nd

		self.assertEqual(uf.Find(one), two)
		self.assertEqual(uf.Find(two), two)
		self.assertEqual(uf.Find(three), three)

		self.assertEqual(one.rank, 0)
		self.assertEqual(two.rank, 1)
		self.assertEqual(three.rank, 0)

		uf.Union(one,three) # arbitrarily, 1st would be added to 2nd
							# union by rank -> 3 should be added to (1,2)

		self.assertEqual(uf.Find(one), two)
		self.assertEqual(uf.Find(two), two)
		self.assertEqual(uf.Find(three), two)	
		
		self.assertEqual(one.rank, 0)
		self.assertEqual(two.rank, 1)
		self.assertEqual(three.rank, 0)

		self.assertEqual(one.parent, two)
		self.assertEqual(two.parent, two)
		self.assertEqual(three.parent, two)


	def test_path_compression(self):
		uf = UnionFind()
		one = uf.MakeSet(1)
		two = uf.MakeSet(2)
		three = uf.MakeSet(3)
		four = uf.MakeSet(4)

		uf.Union(one, two)
		uf.Union(three, four)
		uf.Union(two, three)

		#		4
		#	   / \
		#	  2   3
		#    /
		#   1

		self.assertEqual(one.parent, two)
		self.assertEqual(two.parent, four)
		self.assertEqual(four.parent, four)
		self.assertEqual(three.parent, four)

		uf.Find(one)

		#	    4
		#	  / | \
		#	 1  2  3

		self.assertEqual(one.parent, four)
		self.assertEqual(two.parent, four)
		self.assertEqual(four.parent, four)
		self.assertEqual(three.parent, four)		


unittest.main()
