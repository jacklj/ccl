Connected Component Labelling
=============================

Connected Component Labelling (CCL) is a technique used in Image Processing to identify blobs of pixels in an image. A blob, or connected component, is an area of connected foreground (?picture definition?) pixels: a single shape made up of a continuous mass of pixels, where from any pixel inside it you can travel to any other pixel inside it, without ever leaving the shape. 

CCL is often used as part of the image segmentation step in a Computer Vision pipeline. Once the connected components in an image have been labelled, each one can be isolated and further analysis performed, such as object classification (determining what kind of thing the object is). A common example is in Optical Character Recognition (recognition of handwritten or typed text in images): each connected component is likely to be an individual letter, so once they have been identified and labelled, they can be passed to a character recognition stage (e.g. a neural net). 

Some modern image processing pipelines have replaced techniques like CCL with end-to-end neural nets (deep neural nets), however algorithms like CCL are still key for applications such as live object detection and tracking, in embedded systems and when training data is limited.

There are two main ways to implement the CCL algorithm: 

1. Scan through the image sequentially from top to bottom and left to right, labelling each pixel based on the labels of its surrounding pixels. A second pass is then needed to correct labelling inconsistencies that certain shaped components cause (equivalent labels are stored in a "union-find" data structure - more on this later). 
2. Scan through the image, and as soon as a foreground pixel is encountered, label the whole of its parent component, using a stack to keep track of the component's pixels. 

In this article we'll look at the first method - designed by Rosenfeld and Pfaltz in 1966 using results from graph theory - as it is particularly efficient. (?talk about efficiency?)


Two pass Connected Component Labelling with Union-Find
------------------------------------------------------

Let's restrict our inputs to monochrome (black and white) images. Each pixel can either be a foreground (black) pixel, or a background (white) pixel. We will use the counting numbers (positive integers) to label our components. Background pixels will be labelled '0'. Therefore, we want our algorithm to do the following operation:
	
	             		  

		  * * *   *    			0 1 1 1 0 2
		      *   *     -> 		0 0 0 1 0 2
		  * * *    				0 1 1 1 0 0
		



First Pass
-----------

In the first pass we scan through the image, pixel by pixel, and look at each pixel's neighbours. A pixel's neighbours are the pixels that immediately surround it. If a pixel is neighbours with a labelled pixel, then it should be given the same label as its neighbour. Which specific neighbouring pixels we look at depends on the purpose of our image analysis - we can choose depending on the type of image, what it contains, etc. Two commonly used connectivities are 4-connectivity and 8-connectivity:

 4-connectivity (looking at the North, East, South and West neighbours):

	  n
	w x e
	  s

 8-connectivity (looking at the North, North-East, East, South-East, South, South-West, West and North-West neighbours):

	nw n ne
	w  x  e
	sw s se


For this article we will use 4-connectivity.

As we scan through the image, row by row from top to bottom, and within each row left to right, we only need to examine those neighbours above and to the left of the current pixel. This is because of the direction in which we are scanning through the image - pixels to the right of and below the current pixel won't have been processed yet, so obviously won't be labelled. Therefore, our labelling kernel (the shape we are using to scan through the image and get each pixel's neighbours) looks like this:

	  n    
	w x

Once the labels from the relevant neighbours have been retrieved, there are three potential scenarios:

1. The pixel has no labelled neighbours (no neighbouring foreground pixels). Therefore, this pixel is the first pixel of a new shape, and should be given a new label. A label counter is used to keep track of the labels that have already been used, so that we make sure a unique new label is given. 
2. The pixel has one or more neighbours with the same label. The current pixel is therefore part of the same shape, so is given the same label as its neighbour(s).
3. The pixel has multiple neighbours with different labels. This still means that the current pixel is part of the same shape as it's neighbours, however a labelling inconsistency has been found, which will need to be fixed in the second pass. Label the current pixel with the smallest of its neighbours' labels.


(? example of each scenario, and example of first pass working so far on an image?)



Handling inconsistencies...
---------------------------

Certain shaped components lead to the labelling inconsistencies encountered in scenario 3 above. They result in the component containing areas of pixels with different labels, which is not what we want. This is simply due to the direction in which we are scanning through the image - components with two 'sections' that only join on the right side will 'look' like 2 separate components until that right joining section is encountered, and by then the two sections will have already been labelled differently. 

During the first pass, we need to record when multiple labels are occurring in the same component (scenario 3). Once these label equivalences (they are equivalent because they should actually be the same label) have been recorded, we can fix these errors with a second pass of the image. To store the label equivalences efficiently, we use the disjoint-set data structure (a.k.a. union-find). This keeps track of which labels are equivalent, and lets us efficiently retrieve the lowest label (the 'representative') in each set of equivalent labels. 

Therefore, if we encounter the following situation during the first pass:

	  1
	3 x

We will record in our disjoint-set data structure that the labels 1 and 3 are equivalent.



Second Pass
-----------
Now we use the recorded label equivalences to fix any labelling inconsistencies from the first pass.

Again scanning through the image pixel by pixel, for each labelled pixel we check if we recorded any equivalent labels in our disjoint-set data structure. If we did, then we replace the pixel's label with the lowest label in its equivalence set. Eventually, every label is replaced with the representative label of its set. Then we're done!

For example:

	Original image:

		0 1 1 1 0 1
		0 0 0 1 0 1
		0 1 1 1 0 0


	After first pass:

		0 1 1 1 0 2
		0 0 0 1 0 2
		0 3 3 1 0 0

		Label equivalencies: (1,3)


	After second pass:

		0 1 1 1 0 2
		0 0 0 1 0 2
		0 1 1 1 0 0


Done!

Jack Lawrence-Jones, 28th July 2016.












