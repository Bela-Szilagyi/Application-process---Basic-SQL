import pprint


# @title: string - title of the menu
# @list_options: list of strings - the options in the menu
# @exit_message: string - the last option with (0) (example: "Back to main menu")
def print_menu(title, list_options, exit_message):
    print(title)
    for index, menu_objects in enumerate(list_options, 1):
        print('({0}) {1}'.format(index, menu_objects))
    print('(0)', exit_message)


# This function gets a list of inputs from the user by the terminal
# @list_labels: list of strings - the labels of the inputs
# @title: string - title of the "input section"
# @inputs: list of string - list of the received values from the user
def get_inputs(list_labels, title):
    inputs = []
    print(title)
    for label in list_labels:
        inputs.append(input('{}'.format(label)))
    return inputs


# This function needs to print an error message. (example: Error: @message)
# @message: string - the error message
def print_error_message(message):
    print(message)
    print()
    return


# This function needs to print result of the query functions
# @result: string or list or dictionary - result of the special function
# @label: string - label of the result
def print_result(results, label):
    print(label)
    for result in results:
        for item in result:
            print(item, ' ', end='')
        print()
    print()
    return
