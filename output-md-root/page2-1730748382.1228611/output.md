![](figures/0-0-FIGURE.jpg)

Figure 2. UCF sample results. Left: input counting image. Middle: Ground truth density map. Right: AMDCN prediction of density map on test image. The network never saw these images during training. All density maps are one channel only (i.e. grayscale), but are colored here for clarity.

of regression for production of density maps [24]. In the same spirit, [4] combines deep and shallow convolutions within the same network, providing accurate counting of dense objects (e.g. the UCF50 crowd dataset).

In this paper, however, we aim to apply the dilated convolution method of [25], which has shown to be able to incorporate multiscale perspective information without using multiple inputs or a complicated network architecture, as well as the multicolumn approach of |8,28] to aggregate multiscale information for the counting problem.

## 3. Method

## 3.1. Dilated Convolutions for Multicolumn Networks

We propose the use of dilated convolutions as an attractive alternative to the architecture of the HydraCNN [18], which seems to saturate in performance at $3$ or more g城g区MeGinoae od no区oe dGn e gregated multicolumn dilated convolution network,
forth shortened as the AMDCN. The architecture of the AMDCN is inspired by the multicolumn counting network of [28]. Extracting features from multiple scales is a good idea when attempting to perform perspective-free counting and increasing the convolution kernel size across columns is an efficient method of doing so. However, the number of parameters increases exponentially as larger kernels are used in these columns to extract features at larger scales. Therefore, we propose using dilated convolutions rather than larger kernels.

Dilated convolutions, as discussed in [25], allow for the exponential increase of the receptive field with a linear increase in the number of parameters with respect to each hidden layer.

In a traditional 2D convolution, we define a real valued function $F \, \colon\, \mathbb{Z}^{2} \, \to\, \mathbb{R},$ an input $\Omega_{r} \,=\, [-r, r ]^{2} \, \in\, \mathbb{Z}^{2}$ , and a filter function $k \, : \, \Omega_{r} \, \to\, \mathbb{R}.$ In this case, a convolution opeationasdfined in |25) is given by

$$
( F * k ) ( \mathbf{p} )=\sum_{\mathbf{s}+\mathbf{t}=\mathbf{p}} F ( \mathbf{s} ) k ( \mathbf{t} ). \qquad\qquad( 1 ) 
$$

A dilated convolution is essentially a generalization of the traditional 2D convolution that allows the operation to skip some inputs. This enables an increase in the size of the filter (i.e. the size of the receptive field) without losing resolution. Formally, we define from [25| the dilated convolution as

$$
( F *_{l} k ) ( \mathbf{p} )=\sum_{\mathbf{s}+l \mathbf{t}=\mathbf{p}} F ( \mathbf{s} ) k ( \mathbf{t} ) \qquad\qquad( 2 ) 
$$

where $l$ is the index of the current layer of the convolution.

Using dilations to construct the aggregator in combination with the multicolumn idea will allow for the construction of a network with more than just $3 ~$ or $4 ~$ columns as in [28] and [8], because the aggregator should prevent the saturation of performance with increasing numbers of columns. Therefore the network will be able to extract useful features from more scales. We take advantage of dila-tions within the columns as well to provide large receptive fields with fewer parameters.

Looking at more scales should allow for more accurate regression of the density map. However, because not all scales will be relevant, we extend the network beyond a simple $1 \times1$ convolution after the merged columns. Instead, we construct a second part of the network, the aggre-gator, which sets our method apart from $[ 2 8 ], [ 8 ]$ , and other multicolumn networks. This aggregator is another series of dilated convolutions that should appropriately consolidate the multiscale information collected by the columns. This is a capability of dilated convolutions observed by [25] While papers such as $[ 2 8 ]$ and |8] have shown that multiple columns and dilated columns are useful in extracting multi-scale information, we argue in this paper that the simple ag-gregator module built using dilated convolutions is able to effectively make use multiscale information from multiple columns. We show compelling evidence for these claims in Section 4.5

The network as shown in Figure $1$ contains ${}_{5}$ columns. Note that dilations allow us to use more columns for counting than [28] or [8]. Each column looks at a larger scale than the previous (the exact dilations can also be seen in Figure [1). There are 32 feature maps for each convolution, and all inputs are zero padded prior to each convolution in order to maintain the same data shape from input to output. That is, an image input to this network will result in a density map of the same dimensions. All activations in the specified network are ReLUs. Our input pixel values are floating point $3 2$ bit values from 0 to $1$ . We center our inputs at $\omicron$ by subtracting the per channel mean from each channel. When