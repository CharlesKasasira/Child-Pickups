# About the Dataset

Labeled Faces in the Wild (LFW) is a database of face photographs designed for studying the problem of unconstrained face recognition. Here are some details about the LFW dataset:

Size and Content:
LFW consists of 13,233 labelled images of faces.
These images belong to 5,749 people.
The dataset includes variations in pose, lighting, and expression.

Format:
Images in the LFW dataset are typically in JPEG format.
Each image is associated with a label that identifies the person in the image.
Each image is available as "lfw/name/name_xxxx.jpg" where "xxxx" is the image number padded to four characters with leading zeroes. For example, the 10th George_W_Bush image can be found as "lfw/George_W_Bush/George_W_Bush_0010.jpg"

Dimensions:
Each image is a 250x250 jpg, detected and centered using the openCV implementation of Viola-Jones face detector. The cropping region returned by the detector was then automatically enlarged by a factor of 2.2 in each dimension to capture more of the head and then scaled to a uniform size.

Metadata:
The dataset is accompanied by metadata that includes information about the individuals in the images, such as their names.

