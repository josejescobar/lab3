'''
Jose Escobar
UTEP ID 80536060
CS3 Lab 3: Red-Black and AVL Tree implementation
'''

class Node: #AVL Tree Node
    def __init__(self, key, embedding):
        self.key = key
        self.embedding = embedding
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0
        
    def get_balance(self):
        left_height = -1
        if self.left is not None:
            left_height = self.left.height
        right_height = -1
        if self.right is not None:
            right_height = self.right.height
        return left_height - right_height

    def update_height(self):
        left_height = -1
        if self.left is not None:
            left_height = self.left.height
        right_height = -1
        if self.right is not None:
            right_height = self.right.height
        self.height = max(left_height, right_height) + 1

    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False
        if which_child == "left":
            self.left = child
        else:
            self.right = child
        if child is not None:
            child.parent = self
        self.update_height()
        return True

    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)
        return False

    def get_embedding(self):
        if self.embedding is not None:
            return self.embedding
    
    def set_embedding(self, array):
        self.embedding = array

        
class AVLTree: ##Implementation of methods to modify/research AVL Tree
    def __init__(self):
        self.root = None

    def rotate_left(self, node):
        right_left_child = node.right.left
        if node.parent is not None:
            node.parent.replace_child(node, node.right)
        else:  
            self.root = node.right
            self.root.parent = None
        node.right.set_child('left', node)
        node.set_child('right', right_left_child)
        return node.parent

    def rotate_right(self, node):
        left_right_child = node.left.right
        if node.parent is not None:
            node.parent.replace_child(node, node.left)
        else:  
            self.root = node.left
            self.root.parent = None
        node.left.set_child('right', node)
        node.set_child('left', left_right_child)        
        return node.parent

    def rebalance(self, node):
        node.update_height()        
        if node.get_balance() == -2:
            if node.right.get_balance() == 1:
                self.rotate_right(node.right)
            return self.rotate_left(node)
        elif node.get_balance() == 2:
            if node.left.get_balance() == -1:
                self.rotate_left(node.left)
            return self.rotate_right(node)
        return node

    def insert(self, node):
        if self.root is None:
            self.root = node
            node.parent = None
        else:
            current_node = self.root
            while current_node is not None:
                if node.key < current_node.key:
                    if current_node.left is None:
                        current_node.left = node
                        node.parent = current_node
                        current_node = None
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.right = node
                        node.parent = current_node
                        current_node = None
                    else:
                        current_node = current_node.right
            node = node.parent
            while node is not None:
                self.rebalance(node)
                node = node.parent
                
    def _depth(self, k):
        _dep = self._depth_total(self.root, k)
        f=open("AVL_depth.txt", "a+")
        for i in range (len(_dep)):
            f.write(str(_dep[i]+" \n"))
        f.close()
        return None
       
    def _depth_total(self, node, k):
        arr = []
        if node is None:
            return
        if k==0:
            arr.append(node.key)
        else:
            arr = arr + self._depth_total(node.left, k-1)
            arr = arr + self._depth_total(node.right, k-1)
        return arr
            
    def _write(self):
        _ascend = self._write_afile(self.root)
        f=open("AVL_tree.txt", "a+", encoding="utf-8")
        for i in range (len(_ascend)):
            f.write(str(_ascend[i])+" \n")
        f.close()
        return None
    
    def _write_afile(self, node):
        arr = []
        if node:
            arr = self._write_afile(node.left)
            arr.append(node.key)
            arr = arr + self._write_afile(node.right)
        return arr
    
    def _height(self):
        return self._height_total(self.root)

    def _height_total(self, node):
        if node is None:
            return -1
        left_height = self._height_total(node.left)
        right_height = self._height_total(node.right)
        return 1 + max(left_height, right_height)

    def _size(self):
        return self._size_total(self.root)
    
    def _size_total(self, node):
        if node is None:
            return 0
        else:
            return self._size_total(node.left) + 1 + self._size_total(node.right)

    def search(self, key):
        current_node = self.root
        while current_node is not None:
            if current_node.key == key: return current_node
            elif current_node.key < key: current_node = current_node.right
            else: current_node = current_node.left
        return None

    def remove_key(self, key):
        node = self.search(key)
        if node is None:
            return False
        else:
            return self.remove_node(node)
            
    def remove_node(self, node):
        if node is None:
            return False
        parent = node.parent
            
        # Case 1: Internal node with 2 children
        if node.left is not None and node.right is not None:
            successor_node = node.right
            while successor_node.left != None:
                successor_node = successor_node.left
]            node.key = successor_node.key
            self.remove_node(successor_node)
            return True
        
        # Case 2: Root node (with 1 or 0 children)
        elif node is self.root:
            if node.left is not None:
                 self.root = node.left
            else:
                 self.root = node.right

            if self.root is not None:
                 self.root.parent = None

            return True
        
        # Case 3: Internal with left child only
        elif node.left is not None:
            parent.replace_child(node, node.left)
            
        # Case 4: Internal with right child only OR leaf
        else:
            parent.replace_child(node, node.right)
        node = parent
        while node is not None:
            self.rebalance(node)            
            node = node.parent
        
        return True