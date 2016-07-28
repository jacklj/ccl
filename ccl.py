"""
	Connected Component Labelling algorithm.
	Jack Lawrence-Jones, July 2016

	For blob/connected component detection. Labels each pixel within a given blob with the same 
	label.
	Monochrome images.

	2 pass implementation using disjoint-set data structure to record label equivalences.
	O(n) for image containing n pixels. 
"""

import copy
from union_find import MakeSet, Union, Find, getNode, display_all_sets


CONNECTIVITY_4 = 1
CONNECTIVITY_8 = 2


def connected_component_labelling(image, connectivity_type):
	"""
		2 pass algorithm using disjoint-set data structure to maintain record of label 
		equivalences.

		1st pass: label image and record label equivalence classes.
		2nd pass: replace labels with their root labels.

		(optional 3rd pass: Flatten labels so they are consecutive integers starting from 1.)

		Takes monochrome image represented as 2D integer array:
			foreground pixels -> 1
			background pixels -> 0

	"""
	image = copy.deepcopy(image) # Copy input image so we don't change the input image itself.
	current_label = 1 # Label counter

	# 1st Pass: label image and record label equivalences.
	for y, row in enumerate(image): # Pythonic loop index variables
		for x, pixel in enumerate(row):
			
			if pixel <= 0:
				# Background pixel - do nothing
				pass
			else: 
				# Foreground pixel - work out what its label should be.

				# Get set of neighbour's labels
				labels = neighbouring_labels(image, connectivity_type, x, y)

				if not labels:
					# If no neighbouring foreground pixels, new label - use current_label 
					image[y][x] = current_label
					MakeSet(current_label) # record label in disjoint set
					current_label = current_label + 1 # increment for next time				
				
				else:
					# Pixel is definitely part of a connected component: get smallest label of 
					# neighbours
					smallest_label = smallest(labels)
					image[y][x] = smallest_label

					if len(labels) > 1: # More than one type of label in component -> add 
										# equivalence class.
						for label in labels:
							Union(getNode(smallest_label), getNode(label))

	print("1st pass:")
	print_image(image)
	display_all_sets()

	# 2nd Pass: replace labels with their root labels.
	final_labels = {}
	new_label_number = 1

	for y, row in enumerate(image):
		for x, pixel_value in enumerate(row):
			
			if pixel_value > 0: # Foreground pixel
				# Get element's set's representative value and use as the pixel's new label.
				new_label = Find(getNode(pixel_value)).value 
				image[y][x] = new_label

				# Add label to list of labels used, for 3rd pass (flattening label list).
				if new_label not in final_labels.keys():
					final_labels[new_label] = new_label_number
					new_label_number = new_label_number + 1

	print("2nd pass:")
	print_image(image)
	display_all_sets()


	# 3rd Pass: flatten label list so labels are consecutive integers starting from 1 (in order 
	# of top to bottom, left to right).
	# Different implementation of disjoint-set may remove the need for 3rd pass?
	for y, row in enumerate(image):
		for x, pixel_value in enumerate(row):
			
			if pixel_value > 0: # Foreground pixel
				image[y][x] = final_labels[pixel_value]

	return image



# Private functions ############################################################################
def neighbouring_labels(image, connectivity_type, x, y):
	"""
		Gets the set of neighbouring labels of pixel(x,y), depending on the connectivity type.

		Labelling kernel (only includes neighbouring pixels that have already been labelled - 
		row above and column to the left):

			Connectivity 4:
				    n
				 w  x  
			 
			Connectivity 8:
				nw  n  ne
				 w  x   
	"""

	labels = set()

	if connectivity_type == CONNECTIVITY_4 or connectivity_type == CONNECTIVITY_8:
		# West neighbour
		if x > 0: # pixel is not on left edge of image
			west_neighbour = image[y][x-1]
			if west_neighbour > 0: # it's a labelled pixel
				labels.add(west_neighbour)

		# North neighbour
		if y > 0: # pixel is not on top edge of image
			north_neighbour = image[y-1][x]
			if north_neighbour > 0: # it's a labelled pixel
				labels.add(north_neighbour)


	if connectivity_type == CONNECTIVITY_8:
		# North-west neighbour
		if x > 0 and y > 0: # pixel is not on left or top edges of image
			northwest_neighbour = image[y-1][x-1]
			if northwest_neighbour > 0: # it's a labelled pixel
				labels.add(northwest_neighbour)

		# North-east neighbour
		if y > 0 and x < len(image[y]) - 1: # pixel is not on top or right edges of image
			northeast_neighbour = image[y-1][x+1]
			if northeast_neighbour > 0: # it's a labelled pixel
				labels.add(northeast_neighbour)

	return labels


def smallest(set_x):
	"""
		Returns the smallest item in the set (returns False if set is empty).
	"""
	if set_x:
		set_x = copy.deepcopy(set_x) # so we don't pop an item off the actual set of labels
		smallest = set_x.pop()
		for item in set_x:
			if item < smallest:
				smallest = item
		return smallest

	else:
		return False


def print_image(image):
	""" 
		Prints a 2D array nicely. For debugging.
	"""
	for y, row in enumerate(image): # python loop index variables
		print(row)



# to do ########################################################################################
# from Pillow import Image
# from numpy import *
def convert_image_to_2d_int_array(image_path):
	"""
		Converts monochrome images to 2D arrays.
	"""
	# temp=asarray(Image.open(image_path))
	
	# for j in temp:
	# 	# new_temp gets the two first pixel values
	#     new_temp = asarray([[i[0],i[1]] for i in j]) 
	    

def display_coloured_image(labelled_image):
	"""
		Displays image with connected components coloured in.
	"""
	pass


def connected_components(labelled_image):
	"""
		Gets list of connected components, each with bounding box (x-min, y-min, x-max, y-max), 
		mass (total number of pixels it contains) and an image of the component.
	"""
	pass


# make this module useable as a script from the command line
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1: # at least one command line parameter
	    image_path = str(sys.argv[1])
	    image_array = convert_image_to_2d_int_array(image_path)
	    result = connected_component_labelling(image_array)
	    print_image(result)



# Testing ######################################################################################
# to do: proper test cases
i1 = [
	[0,0,0,0],
	[0,1,1,1],
	[0,0,0,1],
	[0,1,1,1],
	]

i2 = [
	[1,1,0,0,0,1,1,1,0,0],
	[0,1,0,0,0,0,0,1,0,0],
	[0,0,0,1,0,1,1,1,0,0],
	[0,0,1,1,0,0,0,0,1,0],
	[0,0,1,1,0,0,0,0,0,0],
	[0,1,1,1,0,0,0,1,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,1,1,1,1,1],
	[0,0,0,0,0,1,1,1,1,1],
	[0,0,0,0,0,0,0,0,0,0],
	]

print("Original image:")
print_image(i2)
print("----")

result = connected_component_labelling(i2, CONNECTIVITY_4)
print("Labelled:")
print_image(result)
print("----")
print_image(i2)


# test_set = set()
# test_set.add(3)
# print(smallest(test_set))
