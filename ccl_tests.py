import unittest
import numpy as np
from ccl import connected_component_labelling, CONNECTIVITY_4, CONNECTIVITY_8


class TestCCL(unittest.TestCase):

	def test_empty_image(self):
		input_image = np.zeros((3, 3), dtype=bool)
		desired_output = np.zeros((3, 3), dtype=np.int16)

		output = connected_component_labelling(input_image, CONNECTIVITY_8)
		self.assertTrue(np.array_equal(output, desired_output))


	def test_full_image(self):
		input_image = np.ones((3, 3), dtype=bool)
		desired_output = np.ones((3, 3), dtype=np.int16)

		output = connected_component_labelling(input_image, CONNECTIVITY_8)
		self.assertTrue(np.array_equal(output, desired_output))


	def test_one_pixel_image(self):
		input_image = np.ones((1,1), dtype=bool)
		desired_output = np.ones((1, 1), dtype=np.int16)

		output = connected_component_labelling(input_image, CONNECTIVITY_8)
		self.assertTrue(np.array_equal(output, desired_output))


	def test_simple_case(self):
		input_image = np.array([[False, False, False, False],
								[False, True, True, False],
								[False, False, False, False]])
		desired_output = np.array([[0,0,0,0],
								   [0,1,1,0],
								   [0,0,0,0]])

		output = connected_component_labelling(input_image, CONNECTIVITY_8)
		self.assertTrue(np.array_equal(output, desired_output))


	def test_nw_image_corner(self):
		input_image = np.array([[True, False,],
								[False, False]])
		desired_output = np.array([[1,0],
								   [0,0]])

		output = connected_component_labelling(input_image, CONNECTIVITY_8)
		self.assertTrue(np.array_equal(output, desired_output))


	def test_se_image_corner(self):
		input_image = np.array([[False, False,],
								[False, True]])
		desired_output = np.array([[0,0],
								   [0,1]])
		
		output = connected_component_labelling(input_image, CONNECTIVITY_8)
		self.assertTrue(np.array_equal(output, desired_output))


	def test_connectivities(self):
		input_image = np.array([[True, False],
								[False, True]])
		desired_output_c4 = np.array([[1,0],
								      [0,2]])

		desired_output_c8 = np.array([[1,0],
								      [0,1]])


		output_c4 = connected_component_labelling(input_image, CONNECTIVITY_4)
		output_c8 = connected_component_labelling(input_image, CONNECTIVITY_8)

		self.assertTrue(np.array_equal(output_c4, desired_output_c4), "\noutput: \n" + str(output_c4) + "\ndesired: \n" + str(desired_output_c4))
		self.assertTrue(np.array_equal(output_c8, desired_output_c8))


	def test_secondpass_c4(self):
		input_image = np.array([[False, True,],
								[True, True]])
		desired_output = np.array([[0,1],
								   [1,1]])	
		
		output = connected_component_labelling(input_image, CONNECTIVITY_4)
		self.assertTrue(np.array_equal(output, desired_output))			


	def test_secondpass_c8(self):
		input_image = np.array([[True, False, True],
								[False, True, False]])
		desired_output = np.array([[1,0,1],
								   [0,1,0]])
		
		output = connected_component_labelling(input_image, CONNECTIVITY_8)
		self.assertTrue(np.array_equal(output, desired_output))

	def test_thirdpass_c4(self):
		input_image = np.array([[False, True, False, False],
								[True, True, False, True]])
		desired_output = np.array( [[0,1,0,0],
									[1,1,0,2]])

		output = connected_component_labelling(input_image, CONNECTIVITY_4)
		self.assertTrue(np.array_equal(output, desired_output))
	
	def test_thirdpass_c8(self):
		input_image = np.array([[True, False, True, False, True],
								[False, True, False, False, False]])
		desired_output = np.array( [[1,0,1,0,2],
									[0,1,0,0,0]])

		output = connected_component_labelling(input_image, CONNECTIVITY_8)
		self.assertTrue(np.array_equal(output, desired_output))

unittest.main()
