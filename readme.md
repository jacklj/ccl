Connected Component Labelling
=============================

Connected Component Labelling is a technique used in Computer Vision and Image Processing to identify blobs of connected foreground pixels in an image. 

It is often used as one of the first steps in an image processing pipeline - image segmentation. Once the connected components in an image have been labelled, it is easy to extract each component for further processing, such as for object classification (determining what kind of thing the object is). A common example is in Optical Character Recognition (recognition of handwritten or typed text in images): once each component has been labelled, it can be extracted and passed to a character recognition stage (e.g. a neural net). 

Some modern image processing pipelines have replaced techniques like Connected Component Labelling with end to end neural nets (deep neural nets), however algorithms like Connected Component Labelling are still key for applications such as live object detection and tracking, in embedded systems and when training data is limited.

There are two main ways to implement the Connected Component Labelling algorithm: one scans through the image sequentially top to bottom and left to right, labelling each pixel based on its neighbours that have previously been labelled. A second pass is then required to complete the labelling, as certain shapes will result in components containing multiple labels after the first pass. The second implementation labels the whole of each component as soon as it encounters one of it's pixels, using a stack to keep track of the component's pixels. In this article we'll look at the first implementation - designed by Rosenfeld and Pfaltz in 1966 using results from graph theory - as it is particularly efficient.


Two pass Connected Component Labelling with Union-Find
-------------------------------------------------------

For simplicity, we will consider a monochrome image as a two dimensional boolean list, with background pixels having value 0 and foreground pixels having value 1. We will label the components with positive integers.

	 
	   * * *   			 [[0,1,1,1],
	     *      		  [0,0,1,0],
	 *   *      	-> 	  [1,0,1,0],
	 * * *       		  [1,1,1,0]]
	             		  
	


First Pass
-----------

In the first pass we scan through the image, pixel by pixel, and look at each pixel's neighbours. Which specific neighbours we look at is arbitrary and depends on the purpose of our image processing system. Two commonly used connectivities are 4-connectivity and 8-connectivity:

 4-connectivity (north, east, south, west):

	  n
	w x e
	  s

 8-connectivity (north, north-east, east, south-east, south, south-west, west, north-west):

	nw n ne
	w  x  e
	sw s se

For this article we will use 4-connectivity for simplicity.

As we scan through the image row by row from top to bottom, and within each row left to right, we only need to examine those neighbours above and to the left of the current pixel. Therefore our 4-connectivity labelling kernel (the shape we are using to scan through the image and get each pixels neighbours) looks like this:

	  n
	w x

Once the labels from the relevant neighbours have been retrieved, the current pixel is labelled with the smallest of these labels. 

If there are no neighbouring foreground pixels, then the pixel is given a new label. A label counter is used to keep track of the labels that have already been used, so that we make sure a unique new label is given.

Certain shapes can, however, result in components containing multiple different labels, which is not what we want. Therefore, a second pass is required to fix these components. During the first pass, we need to record when multiple labels are occurring in the same component. This occurs when the north neighbour has a different label to the west neighbour. Once these label equivalences have been recorded, we can fix these 'errors' with a second pass of the image. To store these label equivalences efficiently, we use the disjoint-set data structure (a.k.a. union-find). This keeps track of which labels are connected to which other labels, and lets us efficiently retrieve the lowest label in each set of equivalent labels. Therefore, if we encounter the following situation during the first pass:

	  4
	3 x

We will record in our disjoint-set data structure that the labels 3 and 4 are equivalent.



Second Pass
-----------
Now we use the recorded label equivalences to fix any component labelling inconsistencies in our image.

Again scanning through the image pixel by pixel, for each labelled pixel we check if for that label we recorded any equivalent labels in our disjoint-set data structure. If we did, then we replace the pixel's label with the lowest label (the 'representative') in it's equivalence set. Eventually, every label is replaced with the representative label of it's set. Then we're done!

For example:

	Original image:

		0 1 1 1 0 1
		0 0 0 1 0 1
		0 1 1 1 0 0


	After first pass:

		0 1 1 1 0 2
		0 0 0 1 0 2
		0 3 3 1 0 0

		(labels 1 and 3 are recorded as equivalent)


	After second pass:

		0 1 1 1 0 2
		0 0 0 1 0 2
		0 1 1 1 0 0


Done!













