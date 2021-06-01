def insert(root, key):
    if root.data is None:
        return BinarySearchTreeNode(key)
    else:
        if key < root.data:
            root.left = insert(root.left, key)
        else:
            root.right = insert(root.right, key)
    return root


def search1(root, key):
    if root.data == key:
        return True
    else:
        if key < root.data:
            if root.left:
                return search1(root.left, key)
            else:
                return False
        if key > root.data:
            if root.right:
                return search1(root.right, key)
            else:
                return False


class BinarySearchTreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def add_child(self, data):
        if self.data is None:
            return BinarySearchTreeNode(data)
        if self.data == data:
            return
        if data < self.data:
            if self.left:
                self.left.add_child(data)
            else:
                self.left = BinarySearchTreeNode(data)
        if data > self.data:
            if self.right:
                self.right.add_child(data)
            else:
                self.right = BinarySearchTreeNode(data)

    def search(self, data):
        if self.data == data:
            return True
        else:
            if data < self.data:
                if self.left:
                    return self.left.search(data)
                else:
                    return False
            else:
                if self.right:
                    return self.right.search(data)
                else:
                    return False

    def inorder_traversal(self):
        element = []
        if self.left:
            element += self.left.inorder_traversal()
        element.append(self.data)
        if self.right:
            element += self.right.inorder_traversal()
        return element

    def postorder_traversal(self):
        element = []
        if self.left:
            element += self.left.postorder_traversal()
        if self.right:
            element += self.right.postorder_traversal()
        element.append(self.data)
        return element

    def preorder_traversal(self):
        element = []
        element.append(self.data)
        if self.left:
            element += self.left.preorder_traversal()
        if self.right:
            element += self.right.preorder_traversal()
        return element

    def treeMax(self):
        if self.right is None:
            return self.data
        else:
            return self.right.treeMax()

    def treeMin(self):
        if self.left is None:
            return self.data
        else:
            return self.left.treeMin()



def build_tree(elements):
    root = BinarySearchTreeNode(elements[0])
    for i in range(1, len(elements)):
        root.add_child(elements[i])
    return root


numbers_tree = build_tree([17, 4, 3, 1, 20, 7, 9, 23, 18, 34])
# numbers_tree = build_tree([1,2,3,4,5,6,7])
numbers_tree.add_child(19)
print("Pre order traversal gives this sorted list:", numbers_tree.preorder_traversal())
print("Post order traversal gives this sorted list:", numbers_tree.postorder_traversal())
print("In order traversal gives this sorted list:", numbers_tree.inorder_traversal())
print("Tree Max value:=", numbers_tree.treeMax())
print("Tree Min value:=", numbers_tree.treeMin())