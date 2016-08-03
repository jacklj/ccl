Connected Component Labelling
=============================

A Connected Component Labelling algorithm implemented in Python.

[How it works](https://jacklj.github.io/ccl/).

Usage:
		
	Python:
		>>> image = Image.open("./binary_image.png")
		>>> bool_image = image_to_2d_bool_array(image)
		>>> result = connected_component_labelling(bool_image, 4)

	Terminal (second parameter is connectivity type):
		$  python ccl.py path/to/image.png 4
