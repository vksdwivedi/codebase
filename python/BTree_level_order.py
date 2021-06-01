import sys
# A class to store a binary tree node
class Node:
    def __init__(self, key=None, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

# Traverse the tree in a preorder fashion and store nodes in a dictionary
# corresponding to their level
def preorder(root, level, dict):
    # base case: empty tree
    if root is None:
        return
    # insert the current node and its level into the dictionary
    dict.setdefault(level, []).append(root.key)
    # recur for the left and right subtree by increasing the level by 1
    preorder(root.left, level + 1, dict)
    preorder(root.right, level + 1, dict)

# Recursive function to print level order traversal of a given binary tree
def levelOrderTraversal(root):
    # create an empty dictionary to store nodes between given levels
    dict = {}
    # traverse the tree and insert its nodes into the dictionary
    # corresponding to their level
    preorder(root, 1, dict)
    # iterate through the dictionary and print all nodes between given levels
    for i in range(1, len(dict) + 1):
        print(f"Level {i}:", dict[i])


if __name__ == '__main__':
    root = Node(15)
    root.left = Node(10)
    root.right = Node(20)
    root.left.left = Node(8)
    root.left.right = Node(12)
    root.right.left = Node(16)
    root.right.right = Node(25)
    root.right.right.right = Node(30)

    levelOrderTraversal(root)