'''
Jose Escobar
UTEP ID 80536060
CS3 Lab 3: Red-Black and AVL Tree implementation
'''

import AVLTree
import RedBlackTree
import math 
from AVLTree import AVLTree
from RedBlackTree import RedBlackTree
from AVLTree import Node


def read_file(): #Creates a Tree from the given file
    f = open('glove.6B.50d.txt', encoding="utf-8")
    line = f.readline()
    while line:
        _line = line.split(" ")
        word = _line[0]
        if word[0].isalpha():
            embedding_array = []
            for j in range(1,len(_line)):
                embedding_array.append(float(_line[j]))
            node = Node(word, embedding_array)
            try:
                tree.insert(node)
            except:
                tree.insert(word,embedding_array)
        line = f.readline()
    f.close()

#Main method stars here. User is asked the type of Tree to use and methods are called for implementation
while True:
    _input = input("For Red-Black Tree type 0" + "\n" + "For AVL Tree type 1" + "\n" + "Your selection: ")
    if _input is not '0' and _input is not '1':
        print("Invalid, type 0 or 1" )
        continue
    else:
        break

if _input is "0": #Red-Black Tree
    tree = RedBlackTree()
    read_file()
    print("RedBlack Tree has "+ str(len(tree)) + ' nodes')
    print('and')
    print("It's height is " + str(tree._height()))

    output_file = open("RedBlack_tree.txt", "w+", encoding = 'utf-8')
    tree._write()
    output_file.close()
    
    while True:
        _inputuser = input("Please enter the depth of nodes you would like printed to file: ")
        # Checks if the input is valid for the tree.
        if int(_inputuser) >= int(tree._height()) or int(_inputuser) < 0:
             print("Depth is not valid, please choose another depth size" )
             continue
        else:
             break
#Depth of tree is read
    k=int(_inputuser)
    depth_file = open("RB_depth.txt", "w+", encoding="utf-8")
    tree._depth(k)
    depth_file.close()

if _input is "1": #AVL Tree
    tree = AVLTree()
    read_file() 
    
    print("Nodes in tree: "+ str(tree._size()))
    print("\n")
    print("Height: " + str(tree._height()))
    
    output_file = open("AVL_tree.txt", "w+", encoding = 'utf-8')
    tree._write()
    output_file.close()
    
    while True:
        _inputuser = input("Please enter the depth of nodes you would like printed to file: ")
        print()
        if int(_inputuser) >= int(tree._height()) or int(_inputuser) < 0:
            print("Depth is not valid, please choose another depth size: ")
            continue
        else:
             break
#Depth of tree is read
    k=int(_inputuser)
    depth_file = open("AVL_depth.txt", "w+", encoding = 'utf-8')
    tree._depth(k)
    depth_file.close()

f = open('twoWord.txt')
line = f.readline()

while line:
    _line = line.split(" ")
    w0 = tree.search(_line[0])
    w1 = tree.search(_line[1])
    if w0 is None or w1 is None:
        print('no comparison is found')
    else:
        dot_prod = 0
        magnitude_0 = 0
        magnitude_1 = 0
        e0 = w0.get_embedding()
        e1 = w1.get_embedding()
        for i in range (len(e0)):
            dot_prod+= e0[i]*e1[i]
            magnitude_0 += e0[i]*e0[i]
            magnitude_1 += e1[i]*e1[i]
        magnitude_0 = math.sqrt(magnitude_0)
        magnitude_1 = math.sqrt(magnitude_1)
        magnitude_0 = magnitude_0 * magnitude_1
        cosine_similarity = dot_prod/magnitude_0
        print(_line[0],"",_line[1],"", cosine_similarity)
    line = f.readline()