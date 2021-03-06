# -*- coding: utf-8 -*-
"""Assignment 2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GecvXTJ9Nd3mOa_2FVOQIZcoQgtE9fg_

# Exercise 2: Decision Trees

In this assignment you will implement a Decision Tree algorithm as learned in class.

## Read the following instructions carefully:

1. This jupyter notebook contains all the step by step instructions needed for this exercise.
1. Submission includes this notebook only with the exercise number and your ID as the filename. For example: `hw2_123456789_987654321.ipynb` if you submitted in pairs and `hw2_123456789.ipynb` if you submitted the exercise alone.
1. Write **efficient vectorized** code whenever possible. Some calculations in this exercise take several minutes when implemented efficiently, and might take much longer otherwise. Unnecessary loops will result in point deduction.
1. You are responsible for the correctness of your code and should add as many tests as you see fit. Tests will not be graded nor checked.
1. Write your functions in this notebook only. **Do not create Python modules and import them**.
1. You are allowed to use functions and methods from the [Python Standard Library](https://docs.python.org/3/library/) and [numpy](https://www.numpy.org/devdocs/reference/) only. **Do not import anything else.**
1. Your code must run without errors. Make sure your `numpy` version is at least 1.15.4 and that you are using at least python 3.6. Changes of the configuration we provided are at your own risk. Any code that cannot run will not be graded.
1. Write your own code. Cheating will not be tolerated.
1. Answers to qualitative questions should be written in **markdown** cells (with $\LaTeX$ support). Answers that will be written in commented code blocks will not be checked.

## In this exercise you will perform the following:
1. Practice OOP in python.
2. Implement two impurity measures: Gini and Entropy.
3. Construct a decision tree algorithm.
4. Prune the tree to achieve better results.
5. Visualize your results.

# I have read and understood the instructions: *** 204287635 & 209045749 ***
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# make matplotlib figures appear inline in the notebook
# %matplotlib inline
plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

"""## Warmup - OOP in python

Our desicion tree will be implemented using a dedicated python class. Python classes are very similar to classes in Java.


You can use the following [site](https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/) to learn about classes in python.
"""

class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, node):
        self.children.append(node)

n = Node(5)
p = Node(6)
q = Node(7)
n.add_child(p)
n.add_child(q)
n.children

"""## Data preprocessing

For the following exercise, we will use a dataset containing mushroom data `agaricus-lepiota.csv`. 

This data set includes descriptions of hypothetical samples corresponding to 23 species of gilled mushrooms in the Agaricus and Lepiota Family. Each species is identified as definitely edible, definitely poisonous, or of unknown edibility and not recommended. This latter class was combined with the poisonous
one (=there are only two classes **edible** and **poisonous**). 
    
The dataset contains 8124 observations with 22 features:
1. cap-shape: bell=b,conical=c,convex=x,flat=f,knobbed=k,sunken=s
2. cap-surface: fibrous=f,grooves=g,scaly=y,smooth=s
3. cap-color: brown=n,buff=b,cinnamon=c,gray=g,green=r,pink=p,purple=u,red=e,white=w,yellow=y
4. bruises: bruises=t,no=f
5. odor: almond=a,anise=l,creosote=c,fishy=y,foul=f, musty=m,none=n,pungent=p,spicy=s
6. gill-attachment: attached=a,descending=d,free=f,notched=n
7. gill-spacing: close=c,crowded=w,distant=d
8. gill-size: broad=b,narrow=n
9. gill-color: black=k,brown=n,buff=b,chocolate=h,gray=g,green=r,orange=o,pink=p,purple=u,red=e,white=w,yellow=y
10. stalk-shape: enlarging=e,tapering=t
11. stalk-root: bulbous=b,club=c,cup=u,equal=e,rhizomorphs=z,rooted=r
12. stalk-surface-above-ring: fibrous=f,scaly=y,silky=k,smooth=s
13. stalk-surface-below-ring: fibrous=f,scaly=y,silky=k,smooth=s
14. stalk-color-above-ring: brown=n,buff=b,cinnamon=c,gray=g,orange=o,pink=p,red=e,white=w,yellow=y
15. stalk-color-below-ring: brown=n,buff=b,cinnamon=c,gray=g,orange=o,pink=p,red=e,white=w,yellow=y
16. veil-type: partial=p,universal=u
17. veil-color: brown=n,orange=o,white=w,yellow=y
18. ring-number: none=n,one=o,two=t
19. ring-type: cobwebby=c,evanescent=e,flaring=f,large=l,none=n,pendant=p,sheathing=s,zone=z
20. spore-print-color: black=k,brown=n,buff=b,chocolate=h,green=r,orange=o,purple=u,white=w,yellow=y
21. population: abundant=a,clustered=c,numerous=n,scattered=s,several=v,solitary=y
22. habitat: grasses=g,leaves=l,meadows=m,paths=p,urban=u,waste=w,woods=d

First, we will read and explore the data using pandas and the `.read_csv` method. Pandas is an open source library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.
"""

# load dataset
data = pd.read_csv('agaricus-lepiota.csv')

"""One of the advantages of the Decision Tree algorithm is that almost no preprocessing is required. However, finding missing values is always required."""

#############################################################################
# TODO: Find the columns with missing values and remove them from the data.#
#############################################################################
data_columns = data.columns.values.tolist()
columns_to_remove = []
for col in data_columns:
    if (data[col].dropna().empty):
        columns_to_remove.append(col)
data = data.drop(columns = columns_to_remove)
pass
#############################################################################
#                             END OF YOUR CODE                              #
#############################################################################

"""We will split the dataset to `Training` and `Testing` datasets."""

from sklearn.model_selection import train_test_split
# Making sure the last column will hold the labels
X, y = data.drop('class', axis=1), data['class']
X = np.column_stack([X,y])
# split dataset using random_state to get the same split each time
X_train, X_test = train_test_split(X, random_state=99)

print("Training dataset shape: ", X_train.shape)
print("Testing dataset shape: ", X_test.shape)

y.shape

"""## Impurity Measures

Impurity is a measure of how often a randomly chosen element from the set would be incorrectly labeled if it was randomly labeled according to the distribution of labels in the subset. Implement the functions `calc_gini` and `calc_entropy`. You are encouraged to test your implementation (10 points).
"""

def calc_gini(data):
    """
    Calculate gini impurity measure of a dataset.
 
    Input:
    - data: any dataset where the last column holds the labels.
 
    Returns the gini impurity.    
    """
    gini = 0.0
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    labels = np.unique(data[:, -1])
    gini = 1.0
    for label in labels:
        gini -= (np.count_nonzero(data[:, -1] == label) / data.shape[0]) ** 2
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return gini

def calc_entropy(data):
    """
    Calculate the entropy of a dataset.

    Input:
    - data: any dataset where the last column holds the labels.

    Returns the entropy of the dataset.    
    """
    entropy = 0.0
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    labels = np.unique(data[:, -1])
    for label in labels:
        entropy -= (np.count_nonzero(data[:, -1] == label) / data.shape[0]) * np.log2(np.count_nonzero(data[:, -1] == label) / data.shape[0])
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return entropy

##### Your Tests Here #####
calc_gini(X), calc_entropy(X)

"""## Goodness of Split

Given a feature the Goodnees of Split measures the reduction in the impurity if we split the data according to the feature.
$$
\Delta\varphi(S, A) = \varphi(S) - \sum_{v\in Values(A)} \frac{|S_v|}{|S|}\varphi(S_v)
$$

In our implementation the goodness_of_split function will return either the Goodness of Split or the Gain Ratio as learned in class. You'll control the return value with the `gain_ratio` parameter. If this parameter will set to False (the default value) it will return the regular Goodness of Split. If it will set to True it will return the Gain Ratio.
$$
GainRatio(S,A)=\frac{InformationGain(S,A)}{SplitInformation(S,A)}
$$
Where:
$$
InformationGain(S,A)=Goodness\ of\ Split\ calculated\ with\ Entropy\ as\ the\ Impurity\ function \\
SplitInformation(S,A)=- \sum_{a\in A} \frac{|S_a|}{|S|}\log\frac{|S_a|}{|S|}
$$
NOTE: you can add more parameters to the function and you can also add more returning variables (The given parameters and the given returning variable should not be touch). (10 Points)
"""

def goodness_of_split(data, feature, impurity_func, gain_ratio=False):
    """
    Calculate the goodness of split of a dataset given a feature and impurity function.

    Input:
    - data: any dataset where the last column holds the labels.
    - feature: the feature index.
    - impurity func: a function that calculates the impurity.
    - gain_ratio: goodness of split or gain ratio flag.

    Returns the goodness of split (or the Gain Ration).  
    """
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    values = np.unique(data[:, feature])
    if (gain_ratio == True):
        impurity_func = calc_entropy
    goodness = impurity_func(data)
    for value in values:
        sub_data = []
        for row in data:
            if (row[feature] == value):
                sub_data.append(row)
        goodness -= ((np.count_nonzero(data[:, feature] == value) / data.shape[0]) * impurity_func(np.array(sub_data)))
    if (gain_ratio == True):
        split_info = 0.0
        for value in values:
            split_info -= ((np.count_nonzero(data[:, feature] == value) / data.shape[0]) * np.log2(np.count_nonzero(data[:, feature] == value) / data.shape[0]))
        return (goodness / split_info)
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return goodness

"""## Building a Decision Tree

Use a Python class to construct the decision tree. Your class should support the following functionality:

1. Initiating a node for a decision tree. You will need to use several class methods and class attributes and you are free to use them as you see fit. We recommend that every node will hold the feature and value used for the split and its children.
2. Your code should support both Gini and Entropy as impurity measures. 
3. The provided data includes categorical data. In this exercise, when splitting a node create the number of children needed according to the attribute unique values.

Complete the class `DecisionNode`. The structure of this class is entirely up to you. 

Complete the function `build_tree`. This function should get the training dataset and the impurity as inputs, initiate a root for the decision tree and construct the tree according to the procedure you learned in class. (30 points)
"""

class DecisionNode:
    """
    This class will hold everything you require to construct a decision tree.
    The structure of this class is up to you. However, you need to support basic 
    functionality as described above. It is highly recommended that you 
    first read and understand the entire exercise before diving into this class.
    """
    def __init__(self, feature, pred = None):
        self.feature = feature # column index of criteria being tested
        self.children = [] # list of children
        self.pred = pred # prediction of label
        self.features_values = {} # dictionary of all parents feature indexes and values
        self.labels_counts = [] # Relevant only for leaves
        
    def add_child(self, node, feature_value):
        feature_values_so_far = self.features_values.copy()
        feature_values_so_far[self.feature] = feature_value
        node.features_values = feature_values_so_far
        self.children.append((node, feature_value))
        
    def add_label_count(self, label, count):
        self.labels_counts.append((label, count))
        
    def is_leaf(self):
        if(len(self.children) == 0):
            return True
        else:
            return False
    
    def tree_depth(self):
        depth = 0
        if self == None:
            return 0
        else:
            for child in self.children:
                child_depth = child[0].tree_depth()
                if(child_depth > depth):
                    depth = child_depth
        return depth + 1
    
    def children_count(self):
        return len(self.children)
    
    def set_pred(self, data):
        sub_data = []
        for row in data:
            flag = True
            for feature in self.features_values.keys():
                if (row[feature] != self.features_values[feature]):
                    flag = False
                    break
            if (flag == True):
                sub_data.append(row)
        classes, counts = np.unique((np.array(sub_data))[:, -1], return_counts = True)
        maxcount = np.argmax(counts)
        maxclass = classes[maxcount]
        self.pred = maxclass

def build_tree(data, impurity, gain_ratio=False, chi=1, max_depth=1000):
    """
    Build a tree using the given impurity measure and training dataset. 
    You are required to fully grow the tree until all leaves are pure. 

    Input:
    - data: the training dataset.
    - impurity: the chosen impurity measure. Notice that you can send a function
                as an argument in python.
    - gain_ratio: goodness of split or gain ratio flag
    - chi: chi square p-value cut off (1 means no pruning)
    - max_depth: the allowable depth of the tree

    Output: the root node of the tree.
    """
    root = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    unused_features = []
    for i in range(0, data.shape[1] - 1):
        unused_features.append(i)
    root = build_tree_recursion(data, impurity, root, 0, unused_features, gain_ratio, chi, chi_table, max_depth)
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return root

def build_tree_recursion(data, impurity, root, depth, unused_features, gain_ratio, chi, chi_table, max_depth):
    my_unused_features = list(unused_features)
    if(depth == max_depth):
        return None
    
    classes, counts = np.unique(data[:, -1], return_counts = True)
    
    if(classes.shape[0] == 1): # Node is monochromatic, no need to proceed build
        root = DecisionNode(None, classes[0])
        root.add_label_count(classes[0], counts[0])
        return root

    if(len(my_unused_features) == 0): # All attributes have been used, Node isn't monochromatic
        maxcount = np.argmax(counts)
        maxclass = classes[maxcount]
        root = DecisionNode(None, maxclass)
        for i in range(0, classes.shape[0]):
            root.add_label_count(classes[i], counts[i])
        return root
    
    goodness_dict = {}
    for feature in my_unused_features: # Find "best" question
        goodness_dict[feature] = goodness_of_split(data, feature, impurity, gain_ratio)
    max_goodness_feature = max(goodness_dict, key = goodness_dict.get)
    if(goodness_dict[max_goodness_feature] == 0):  # If all the gains are 0 we need to stop, as mentioned in Piazza
        maxcount = np.argmax(counts)
        maxclass = classes[maxcount]
        root = DecisionNode(None, maxclass)
        for i in range(0, classes.shape[0]):
            root.add_label_count(classes[i], counts[i])
        return root
    else:
        root = DecisionNode(max_goodness_feature) 
        values, counts_values = np.unique(data[:, max_goodness_feature], return_counts = True) # Find number of children
        
        if(chi != 1): # Chi pruning
            probs = []
            for i in range(0, classes.shape[0]):
                probs.append((counts[i] / np.sum(counts))) # Distribution of each class in our node
            p, n, E = [], [], []
            for value in range(0, values.shape[0]):
                p_count = 0
                n_count = 0
                for instance in range(0, data.shape[0]):
                    if(data[instance, max_goodness_feature] == values[value]):
                        if(data[instance, -1] == classes[0]):
                            p_count = p_count + 1
                        if(data[instance, -1] == classes[1]):
                            n_count = n_count + 1
                p.append(p_count)
                n.append(n_count)
                current_E = []
                for i in range(0, classes.shape[0]):
                    current_E.append(counts_values[value] * probs[i])
                E.append(current_E)
            chi_square = 0.0
            for value in range(0, values.shape[0]):
                chi_square = chi_square + (((p[value] - E[value][0]) ** 2) / E[value][0]) + (((n[value] - E[value][1]) ** 2) / E[value][1])
            if(chi_square < chi_table[values.shape[0] - 1][chi]): # We need to make the node a leaf
                maxcount = np.argmax(counts)
                maxclass = classes[maxcount]
                root.pred = maxclass
                for i in range(0, classes.shape[0]):
                    root.add_label_count(classes[i], counts[i])
                return root
        
        my_unused_features.remove(max_goodness_feature)
        for value in values:
            selector = [row for row in range(0, data.shape[0]) if data[row, max_goodness_feature] == value]
            child = build_tree_recursion(data[selector, :], impurity, None, depth + 1, my_unused_features, gain_ratio, chi, chi_table, max_depth) # Keep building the tree
            if(child != None): # When pruning the tree we interrupt the building, so we need to make the node a leaf
                root.add_child(child, value)
            else:
                maxcount = np.argmax(counts)
                maxclass = classes[maxcount]
                root.pred = maxclass
                root.feature = None
                for i in range(0, classes.shape[0]):
                    root.add_label_count(classes[i], counts[i])
    return root

# python supports passing a function as an argument to another function.
tree_gini = build_tree(data = X_train, impurity = calc_gini) # gini and goodness of split
tree_entropy = build_tree(data = X_train, impurity = calc_entropy) # entropy and goodness of split
tree_entropy_gain_ratio = build_tree(data = X_train, impurity = calc_entropy, gain_ratio = True) # entropy and gain ratio

"""## Tree evaluation

Complete the functions `predict` and `calc_accuracy`. (10 points)
"""

def predict(node, instance):
    """
    Predict a given instance using the decision tree
 
    Input:
    - root: the root of the decision tree.
    - instance: an row vector from the dataset. Note that the last element 
                of this vector is the label of the instance.
 
    Output: the prediction of the instance.
    """
    pred = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    for child in node.children:
        if child[1] == instance[node.feature]:
            return predict(child[0], instance)
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return node.pred

def calc_accuracy(node, dataset):
    """
    Predict a given dataset using the decision tree
 
    Input:
    - node: a node in the decision tree.
    - dataset: the dataset on which the accuracy is evaluated
 
    Output: the accuracy of the decision tree on the given dataset (%).
    """
    accuracy = 0
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    for instance in dataset:
        if (predict(node, instance) == instance[-1]):
            accuracy += 1
    accuracy /= dataset.shape[0]
    accuracy *= 100
    pass
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return accuracy

"""After building the three trees using the training set, you should calculate the accuracy on the test set. For each tree print the training and test accuracy. Select the tree that gave you the best test accuracy. For the rest of the exercise, use that tree (when you asked to build another tree use the same impurity function and same gain_ratio flag). """

#### Your code here ####
acc_gini_goodness_train = calc_accuracy(tree_gini, X_train) #gini and goodness of split TrainSet accuracy
acc_gini_goodness_test = calc_accuracy(tree_gini, X_test) #gini and goodness of split TestSet accuracy
acc_entropy_goodness_train = calc_accuracy(tree_entropy, X_train) #entropy and goodness of split TrainSet accuracy
acc_entropy_goodness_test = calc_accuracy(tree_entropy, X_test) #entropy and goodness of split TestSet accuracy
acc_entropy_gain_train = calc_accuracy(tree_entropy_gain_ratio, X_train) #entropy and gain ratio TrainSet accuracy
acc_entropy_gain_test = calc_accuracy(tree_entropy_gain_ratio, X_test) #entropy and gain ratio TestSet accuracy

print("gini and goodness of split TrainSet accuracy: ", acc_gini_goodness_train)
print("gini and goodness of split TestSet accuracy: ", acc_gini_goodness_test)
print("entropy and goodness of split TrainSet accuracy: ", acc_entropy_goodness_train)
print("entropy and goodness of split TestSet accuracy: ", acc_entropy_goodness_test)
print("entropy and gain ratio TrainSet accuracy: ", acc_entropy_gain_train)
print("entropy and gain ratio TestSet accuracy: ", acc_entropy_gain_test)

best_accuracy = acc_gini_goodness_test
best_impurity = calc_gini
best_gain_ratio = False
best_tree = "gini and goodness of split"
if (acc_entropy_goodness_test > best_accuracy):
    best_accuracy = acc_entropy_goodness_test
    best_impurity = calc_entropy
    best_gain_ratio = False
    best_tree = "entropy and goodness of split"
if (acc_entropy_gain_test > best_accuracy):
    best_accuracy = acc_entropy_gain_test
    best_impurity = calc_entropy
    best_gain_ratio = True
    best_tree_description = "entropy and gain ratio"

print("best tree is:", best_tree)

"""## Post pruning

Iterate over all nodes in the tree that have at least a single child which is a leaf. For each such node, replace it with its most popular class. Calculate the accuracy on the testing dataset, pick the node that results in the highest testing accuracy and permanently change it in the tree. Repeat this process until you are left with a single node in the tree (the root). Finally, create a plot of the training and testing accuracies as a function of the number of nodes in the tree. (15 points)
"""

#### Your code here ####
from copy import copy, deepcopy

def post_pruning(root, train, test):
    train_acc_array = [calc_accuracy(root, train)]
    test_acc_array = [calc_accuracy(root, test)]
    nodes = [count_nodes(root)]
    best_acc_tree = 0
    best_tree = None
    curr_acc_tree = 0    
    
    while(root.children):
        
        best_acc = -1
        best_parent = None
        
        # an array with all the nodes that have at least one children that is a leaf.
        parents = parent_check(root)
        
        for parent in parents:
            # saving the parents children
            tmp_childrens = []
            for child in parent.children:
                tmp_childrens.append(child)
    
            # making the node to be the the most popular class
            parent.set_pred(train)
            
            # deleting the parents children from the tree
            parent.children = []

            # calculating the tree accuracy with out the parent            
            curr_test_acc = calc_accuracy(root, test)
            
            # checking if the current split that I deleted was the best one to delete up until now.
            if (curr_test_acc > best_acc):
                best_acc = curr_test_acc
                best_parent = parent 
                
            # returning the childrens value and the parent class.
            for child in tmp_childrens:
                parent.children.append(child)
            parent.pred = None
                
            nodes_sum = count_nodes(root)

        # deletes the nodes that provide the best accuracy and turns their parent to a leaf.
        curr_acc_tree = calc_accuracy(root, test)
        if curr_acc_tree > best_acc_tree:
            best_acc_tree = curr_acc_tree 
            best_tree = deepcopy(root)
            
        best_parent.children = []
        best_parent.set_pred(train)
        
        # updating the arrays that need to be returned
        nodes.append(nodes_sum)
        test_acc_array.append(best_acc)
        train_acc = calc_accuracy(root, train)
        train_acc_array.append(train_acc)
        
    return (best_tree ,nodes, train_acc_array, test_acc_array)

def count_nodes(node):
    if(node.children_count() == 0):
        return 1
    nodes = 1
    for child in node.children:
        nodes = nodes + count_nodes(child[0])
    return nodes

def parent_check(node):
    array = []
    queue = [node]
    
    while(len(queue)>0):
        curr_node = queue.pop(0)
        flag_child = 0
        
        for child in curr_node.children:
            if child[0].children_count() == 0:
                if flag_child == 0:
                    array.append(curr_node)
                    flag_child = 1
            else:
                queue.append(child[0])        
    return array

train_tree = build_tree(data = X_train, impurity = best_impurity, gain_ratio = best_gain_ratio)
best_post_purning_tree, num_of_nodes, training, testing = post_pruning(train_tree, X_train, X_test)

plt.plot(num_of_nodes, training, 'r--')
plt.plot(num_of_nodes, testing,'b--')

plt.xlabel('number of nodes')
plt.ylabel('accuracy')
plt.title('accuracy as a function of the number of nodes')
plt.legend(['training data', 'testing data'])
plt.show()

"""## Chi square pre-pruning

Consider the following p-value cut-off values: [1 (no pruning), 0.5, 0.25, 0.1, 0.05, 0.0001 (max pruning)]. For each value, construct a tree and prune it according to the cut-off value. Next, calculate the training and testing accuracy. On a single plot, draw the training and testing accuracy as a function of the tuple (p-value, tree depth). Mark the best result on the graph with red circle. (15 points)
"""

### Chi square table values ###
# The first key is the degree of freedom 
# The second key is the p-value cut-off
# The values are the chi-statistic that you need to use in the pruning
chi_table = {1: {0.5 : 0.45,
                 0.25 : 1.32,
                 0.1 : 2.71,
                 0.05 : 3.84,
                 0.0001 : 100000},
             2: {0.5 : 1.39,
                 0.25 : 2.77,
                 0.1 : 4.60,
                 0.05 : 5.99,
                 0.0001 : 100000},
             3: {0.5 : 2.37,
                 0.25 : 4.11,
                 0.1 : 6.25,
                 0.05 : 7.82,
                 0.0001 : 100000},
             4: {0.5 : 3.36,
                 0.25 : 5.38,
                 0.1 : 7.78,
                 0.05 : 9.49,
                 0.0001 : 100000},
             5: {0.5 : 4.35,
                 0.25 : 6.63,
                 0.1 : 9.24,
                 0.05 : 11.07,
                 0.0001 : 100000},
             6: {0.5 : 5.35,
                 0.25 : 7.84,
                 0.1 : 10.64,
                 0.05 : 12.59,
                 0.0001 : 100000},
             7: {0.5 : 6.35,
                 0.25 : 9.04,
                 0.1 : 12.01,
                 0.05 : 14.07,
                 0.0001 : 100000},
             8: {0.5 : 7.34,
                 0.25 : 10.22,
                 0.1 : 13.36,
                 0.05 : 15.51,
                 0.0001 : 100000},
             9: {0.5 : 8.34,
                 0.25 : 11.39,
                 0.1 : 14.68,
                 0.05 : 16.92,
                 0.0001 : 100000},
             10: {0.5 : 9.34,
                  0.25 : 12.55,
                  0.1 : 15.99,
                  0.05 : 18.31,
                  0.0001 : 100000},
             11: {0.5 : 10.34,
                  0.25 : 13.7,
                  0.1 : 17.27,
                  0.05 : 19.68,
                  0.0001 : 100000}}

#### Your code here ####
from matplotlib.patches import Ellipse

training_accuracy = []
testing_accuracy = []
tuples = []
p_values = [1, 0.5, 0.25, 0.1, 0.05, 0.0001]
for p_value in p_values:
    tree = build_tree(X_train, impurity = best_impurity, gain_ratio = best_gain_ratio, chi = p_value)
    training_accuracy.append(calc_accuracy(tree, X_train))
    testing_accuracy.append(calc_accuracy(tree, X_test))
    tree_depth = str(tree.tree_depth())
    p = str(p_value)
    str_tuple = p + ", " + tree_depth 
    tuples.append(str_tuple)
tuples.reverse()
training_accuracy.reverse()
testing_accuracy.reverse()
best_value_chi = max(testing_accuracy)
best_index_chi = np.argmax(testing_accuracy) + 1
plt.figure(figsize=(7, 7))
plt.plot(tuples, training_accuracy, marker='o')
plt.ylabel('accuracy')
plt.xlabel('(p_value, depth)')
plt.plot(tuples, testing_accuracy, marker='o')
circle = Ellipse((best_index_chi, best_value_chi), width = 0.2, height = 2, color = 'red', fill = False)
plt.gcf().gca().add_artist(circle)
plt.legend(['training', 'testing'])

"""Build the best 2 trees:
1. tree_max_depth - the best tree according to max_depth pruning
1. tree_chi - the best tree according to chi square pruning
"""

#### Your code here ####
tree_post_pruning = best_post_purning_tree
tree_chi = build_tree(X_train, impurity = best_impurity, gain_ratio = best_gain_ratio, chi = p_values[len(p_values) - best_index_chi])

"""## Number of Nodes

Of the two trees above we will choose the one with fewer nodes. Complete the function counts_nodes and print the number of nodes in each tree. (5 points) 
"""

def count_nodes(node):
    """
    Count the number of node in a given tree
 
    Input:
    - node: a node in the decision tree.
 
    Output: the number of node in the tree.
    """
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    if(node.children_count() == 0):
        return 1
    nodes = 1
    for child in node.children:
        nodes = nodes + count_nodes(child[0])
    return nodes

node_num_dict = {}
node_num_dict[tree_post_pruning] = count_nodes(tree_post_pruning)
node_num_dict[tree_chi] = count_nodes(tree_chi)
print("Post pruning number of nodes: ", node_num_dict[tree_post_pruning])
print("Chi square pruning number of nodes: ", node_num_dict[tree_chi])
chosen_tree = min(node_num_dict.keys(), key = (lambda k: node_num_dict[k]))
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

"""## Print the tree

Complete the function `print_tree` and execute it on your chosen tree. Your tree should be visualized clearly. You can use the following example as a reference:
```
[ROOT, feature=X0],
  [X0=a, feature=X2]
    [X2=c, leaf]: [{1.0: 10}]
    [X2=d, leaf]: [{0.0: 10}]
  [X0=y, feature=X5], 
    [X5=a, leaf]: [{1.0: 5}]
    [X5=s, leaf]: [{0.0: 10}]
  [X0=e, leaf]: [{0.0: 25, 1.0: 50}]
```
In each brackets:
* The first argument is the parent feature with the value that led to current node
* The second argument is the selected feature of the current node
* If the current node is a leaf, you need to print also the labels and their counts

(5 points)
"""

# you can change the function signeture
def print_tree(node, depth=0, parent_feature='ROOT', feature_val='ROOT'):
    '''
    prints the tree according to the example above

    Input:
    - node: a node in the decision tree

    This function has no return value
    '''
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    if (parent_feature == 'ROOT'):
        print("[ROOT, feature=X{}],".format(node.feature))
    elif (node.is_leaf() == False):
        print("{}[X{}={}, feature=X{}],".format(print_indentation(depth), parent_feature, feature_val, node.feature))
    elif (len(node.labels_counts) == 1):
        print("{}[X{}={}, leaf]: [{{{}: {}}}]".format(print_indentation(depth), parent_feature, feature_val, node.labels_counts[0][0], node.labels_counts[0][1]))
        return
    else:
        print("{}[X{}={}, leaf]: [{{{}: {}, {}: {}}}]".format(print_indentation(depth), parent_feature, feature_val, node.labels_counts[0][0], node.labels_counts[0][1], node.labels_counts[1][0], node.labels_counts[1][1]))
        return
    for child in node.children:
        print_tree(child[0], depth + 1, node.feature, child[1])

def print_indentation(depth): # Help function to print indentation according to the example
    if (depth == 0):
        return ""
    else:
        indent = " "
        for i in range(0, depth - 1):
            indent = indent + " "
    return indent + indent

print_tree(chosen_tree)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
