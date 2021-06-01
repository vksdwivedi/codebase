class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None

    def print(self):
        if self.head is None:
            print("Linked list is empty")
            return
        itr = self.head
        llstr = ''
        while itr:
            llstr += str(itr.data) + ' --> ' if itr.next else str(itr.data)
            itr = itr.next
        print(llstr)

    def get_length(self):
        count = 0
        itr = self.head
        while itr:
            count += 1
            itr = itr.next

        return count

    def insert_at_begining(self, data):
        node = Node(data, self.head)
        self.head = node

    def insert_at_end(self, data):
        if self.head is None:
            self.head = Node(data, None)
            return

        itr = self.head

        while itr.next:
            itr = itr.next

        itr.next = Node(data, None)

    def insert_at(self, index, data):
        if index < 0 or index > self.get_length():
            raise Exception("Invalid Index")

        if index == 0:
            self.insert_at_begining(data)
            return

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                node = Node(data, itr.next)
                itr.next = node
                break

            itr = itr.next
            count += 1

    def remove_at(self, index):
        if index < 0 or index >= self.get_length():
            raise Exception("Invalid Index")

        if index == 0:
            self.head = self.head.next
            return

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                itr.next = itr.next.next
                break

            itr = itr.next
            count += 1

    def insert_values(self, data_list):
        self.head = None
        for data in data_list:
            self.insert_at_end(data)

    def remove_by_value(self, data):
        if self.head.data == data:
            self.head = self.head.next
            return
        itr = self.head
        while itr:
            if itr.next.data == data:
                itr.next = itr.next.next
                break
            itr = itr.next

    def insert_after_value(self, data_after, data_to_insert):
        itr = self.head
        while itr:
            if itr.data == data_after:
                itr.next = Node(data_to_insert, itr.next)
                break

            itr = itr.next

    def reverselinklst(self):
        prev = None
        current = self.head
        while current:
            next = current.next
            current.next = prev
            prev = current
            current = next

        self.head = prev


def MergeLists(headA, headB):
    if headA is None and headB is None:
        return None

    if headA is None:
        return headB
    elif headB is None:
        return headA

    if headA.data < headB.data:
        ret = headA
        ret.next = MergeLists(headA.next, headB)
    else:
        ret = headB
        ret.next = MergeLists(headA, headB.next)

    return ret


def MergeListsNonRec(nodeA, nodeB):
    mergedHead = Node()  # dummy node so can be handled the same
    merged = mergedHead

    while nodeA is not None or nodeB is not None:
        if nodeA is None:
            merged.next = nodeB
            break
        elif nodeB is None:
            merged.next = nodeA
            break
        else:
            if nodeA.data < nodeB.data:
                merged.next = nodeA
                nodeA = nodeA.next
            else:
                merged.next = nodeB
                nodeB = nodeB.next
        merged = merged.next

    return mergedHead.next


if __name__ == '__main__':
    ll = LinkedList()
    ll.insert_values(["banana", "mango", "grapes", "orange"])
    # ll.insert_at(1,"blueberry")
    # ll.remove_at(2)
    ll.print()
    # ll.remove_by_value("grapes")
    # ll.insert_after_value("banana", "apple")
    ll.reverselinklst()
    ll.print()
