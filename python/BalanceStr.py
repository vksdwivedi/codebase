def balancestring(str):
    open_list = ["[", "{", "("]
    close_list = ["]", "}", ")"]
    stack = []
    for i in str:
        print("Processed string value: ",i)
        if i in open_list:
            stack.append(i)
        else:
            if not stack:
                return False
            print("Stack is:",stack)
            currentChar = stack.pop()
            print("After pop Stack is:",stack)
            print("currentChar = ",currentChar)
            if currentChar == "(":
                if i != ")":
                    return False
            if currentChar == "{":
                if i != "}":
                    return False
            if currentChar == "[":
                if i != "]":
                    return False

    if stack:
        return False
    return True


if __name__ == "__main__":
    expr = "([()([{])}{}]{})"
    if balancestring(expr):
        print("Balanced")
    else:
        print("UnBalanced")











