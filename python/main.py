# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    weekdays = ['sun','mon','tue','wed','thu','fri','sun','mon','mon']
    my_dict = {};
    for x in set(weekdays):
        my_dict[x] = weekdays.count(x)
    print(my_dict)


    inverse = [(key, value) for key, value in my_dict.items()]
    print(max(inverse))
