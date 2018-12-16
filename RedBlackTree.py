'''
Jose Escobar
UTEP ID 80536060
CS3 Lab 3: Red-Black and AVL Tree implementation
'''

class RBTNode: #Red-Black Tree Node
    def __init__(self, key, embedding, parent, is_red = False, left = None, right = None):
        self.key = key
        self.embedding = embedding
        self.left = left
        self.right = right
        self.parent = parent

        if is_red:
            self.color = "red"
        else:
            self.color = "black"
            
    def are_both_children_black(self):
        if self.left != None and self.left.is_red():
            return False
        if self.right != None and self.right.is_red():
            return False
        return True

    def count(self):
        count = 1
        if self.left != None:
            count = count + self.left.count()
        if self.right != None:
            count = count + self.right.count()
        return count
    
    def get_grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    def get_predecessor(self):
        node = self.left
        while node.right is not None:
            node = node.right
        return node

    def get_sibling(self):
        if self.parent is not None:
            if self is self.parent.left:
                return self.parent.right
            return self.parent.left
        return None

    def get_uncle(self):
        grandparent = self.get_grandparent()
        if grandparent is None:
            return None
        if grandparent.left is self.parent:
            return grandparent.right
        return grandparent.left

    def is_black(self):
        return self.color == "black"

    def is_red(self):
        return self.color == "red"

    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)
        return False

    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False
            
        if which_child == "left":
            self.left = child
        else:
            self.right = child
        if child != None:
            child.parent = self
        return True
    
    def get_embedding(self):
        if self.embedding is not None:
            return self.embedding
    
    def set_embedding(self, array):
        self.embedding = array


class RedBlackTree: #Implementation of methods to modify/research Red-Black Tree
    def __init__(self):
        self.root = None
    
    def __len__(self):
        if self.root is None:
            return 0
        return self.root.count()
    
    def _bst_remove(self, key):
        node = self.search(key)
        self._bst_remove_node(node)

    def _bst_remove_node(self, node):
        if node is None:
            return
        if node.left is not None and node.right is not None:
            successor_node = node.right
            while successor_node.left is not None:
                successor_node = successor_node.left
            successor_key = successor_node.key
            self._bst_remove_node(successor_node)
            node.key = successor_key
        elif node is self.root:
            if node.left is not None:
                self.root = node.left
            else:
                self.root = node.right
            if self.root is not None:
                self.root.parent = None
        elif node.left is not None:
            node.parent.replace_child(node, node.left)
        else:
            node.parent.replace_child(node, node.right)
                
    def _depth(self, k):
        _dep = self._depth_total(self.root, k)
        f=open("RB_depth.txt", "a+")
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
        
    def _height(self):
        return self._height_total(self.root)

    def _height_total(self, node):
        if node is None:
            return -1
        left_height = self._height_total(node.left)
        right_height = self._height_total(node.right)
        return 1 + max(left_height, right_height)
        
    def _write(self):
        _ascend = self._write_afile(self.root)
        f=open("RedBlack_tree.txt", "a+", encoding="utf-8")
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
    
    def insert(self, key, embedding):
        new_node = RBTNode(key, embedding, None, True, None, None)
        self.insert_node(new_node)
        
    def insert_node(self, node):
        if self.root is None:
            self.root = node
        else:
            current_node = self.root
            while current_node is not None:
                if node.key < current_node.key:
                    if current_node.left is None:
                        current_node.set_child("left", node)
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.set_child("right", node)
                        break
                    else:
                        current_node = current_node.right
        node.color = "red"
        self.insertion_balance(node)

    def insertion_balance(self, node):
        if node.parent is None:
            node.color = "black"
            return
        if node.parent.is_black():
            return
        parent = node.parent
        grandparent = node.get_grandparent()
        uncle = node.get_uncle()
        if uncle is not None and uncle.is_red():
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.insertion_balance(grandparent)
            return
        if node is parent.right and parent is grandparent.left:
            self.rotate_left(parent)
            node = parent
            parent = node.parent
        elif node is parent.left and parent is grandparent.right:
            self.rotate_right(parent)
            node = parent
            parent = node.parent
        parent.color = "black"
        grandparent.color = "red"
        if node is parent.left:
            self.rotate_right(grandparent)
        else:
            self.rotate_left(grandparent)

    def in_order(self, visitor_function):
        self.in_order_recursive(visitor_function, self.root)

    def in_order_recursive(self, visitor_function, node):
        if node is None:
            return
        self.in_order_recursive(visitor_function, node.left)
        visitor_function(node)
        self.in_order_recursive(visitor_function, node.right)

    def is_none_or_black(self, node):
        if node is None:
            return True
        return node.is_black()

    def is_not_none_and_red(self, node):
        if node is None:
            return False
        return node.is_red()

    def prepare_for_removal(self, node):
        if self.try_case1(node):
            return
        sibling = node.get_sibling()
        if self.try_case2(node, sibling):
            sibling = node.get_sibling()
        if self.try_case3(node, sibling):
            return
        if self.try_case4(node, sibling):
            return
        if self.try_case5(node, sibling):
            sibling = node.get_sibling()
        if self.try_case6(node, sibling):
            sibling = node.get_sibling()
        sibling.color = node.parent.color
        node.parent.color = "black"
        if node is node.parent.left:
            sibling.right.color = "black"
            self.rotate_left(node.parent)
        else:
            sibling.left.color = "black"
            self.rotate_right(node.parent)

    def remove(self, key):
        node = self.search(key)
        if node is not None:
            self.remove_node(node)
            return True
        return False

    def remove_node(self, node):
        if node.left is not None and node.right is not None:
            predecessor_node = node.get_predecessor()
            predecessor_key = predecessor_node.key
            self.remove_node(predecessor_node)
            node.key = predecessor_key
            return

        if node.is_black():
            self.prepare_for_removal(node)
        self._bst_remove(node.key)

        if self.root is not None and self.root.is_red():
            self.root.color = "black"

    def rotate_left(self, node):
        right_left_child = node.right.left
        if node.parent != None:
            node.parent.replace_child(node, node.right)
        else: # node is root
            self.root = node.right
            self.root.parent = None
        node.right.set_child("left", node)
        node.set_child("right", right_left_child)

    def rotate_right(self, node):
        left_right_child = node.left.right
        if node.parent != None:
            node.parent.replace_child(node, node.left)
        else: # node is root
            self.root = node.left
            self.root.parent = None
        node.left.set_child("right", node)
        node.set_child("left", left_right_child)
            
    def search(self, key):
        current_node = self.root
        while current_node is not None:
            if current_node.key == key:
                return current_node
            elif key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        return None\

    def try_case1(self, node):
        if node.is_red() or node.parent is None:
            return True
        return False # node case 1

    def try_case2(self, node, sibling):
        if sibling.is_red():
            node.parent.color = "red"
            sibling.color = "black"
            if node is node.parent.left:
                self.rotate_left(node.parent)
            else:
                self.rotate_right(node.parent)
            return True
        return False # not case 2

    def try_case3(self, node, sibling):
        if node.parent.is_black() and sibling.are_both_children_black():
            sibling.color = "red"
            self.prepare_for_removal(node.parent)
            return True
        return False # not case 3

    def try_case4(self, node, sibling):
        if node.parent.is_red() and sibling.are_both_children_black():
            node.parent.color = "black"
            sibling.color = "red"
            return True
        return False # not case 4

    def try_case5(self, node, sibling):
        if self.is_not_none_and_red(sibling.left) and self.is_none_or_black(sibling.right) and node is node.parent.left:
            sibling.color = "red"
            sibling.left.color = "black"
            self.rotate_right(sibling)
            return True
        return False # not case 5

    def try_case6(self, node, sibling):
        if self.is_none_or_black(sibling.left) and self.is_not_none_and_red(sibling.right) and node is node.parent.right:
            sibling.color = "red"
            sibling.right.color = "black"
            self.rotate_left(sibling)
            return True
        return False # not case 6