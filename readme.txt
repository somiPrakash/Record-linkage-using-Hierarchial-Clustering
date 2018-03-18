Dependencies used : 

* numpy 
* pandas     
* Levenshtein
...............................................................................................................

Parameters to be tweaked in the code : 
1) weights         # line 13
>>> It is a list that takes 4 values as input.They are positive integers , which are further normalised by the sum of all weight values entered. It brings each weight in range (0-1).These weight values determine, which attribute out of 
['first_name' ,'last_name' ,'dob' ,'gender']  plays a major role in determining the similarity any of two  entries in the dataset.

2) net_threshold   # line 15
>>> Value lies in range (0-1) , and determines ,how big the clusters are to be formed.Larger the threshold, larger the individual clusters and vice versa.

3) linkage         # line 17
>>> Type of linkage to be used in the hierarchial clustering: 'single' , 'complete' , 'average'

...............................................................................................................

How to run : 
> Run the file 'dedup.py' . make sure the input file 'dataset.csv' is in the same folder as the python script.
> Change the path of 'dataset.csv' in the python script  after  downloading .
...............................................................................................................

Approach used : 
>  Since it is unsupervised data, clustering seemed the viable solution so the script here implements hierarchial clustering .
> Hierarchial clustering makes use of a similarity/distance matrix calculated for all the 'N' entries of a  dataset,each treated as an individual cluster.
> Distance measure of the strings here used is 'Levenshtein Distance'.The distance is converted into similarity value in range (0-1)
> The matrix formed is N x N  , and from there, we take either the upper or the lower traingular part of the matrix in consideration, checking of the maximum similarity string enries.The one with max similarity are clustered together leaving us  with N-1 clusters.
> The similarity matrix is calculated again for N-1 points , and the process is repeated, and with each iteration, clusters become larger , and similarity value between clusters becomes smaller.Util the maximum value of similarity is above our defined threshold, the iteration continues.

> Distance between two clusters ,any one having more than one element, is where we introduce the 'linkage' terminology.
It was seen that 'complete linkage' formed good clusters than 'average' or 'single'.
