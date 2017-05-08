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
def print_result(columns, results, label):
    BOLD = '\033[1m'
    END = '\033[0m'
    col_width = []
    for column_index in range(len(columns)):
        results_column = []
        for result_index in range(len(results)):
            results_column.append(str(results[result_index][column_index]))
        results_column_width = len(max(results_column, key=len))
        col_width.append(max(len(columns[column_index]), results_column_width) )
    print(label)
    print(BOLD, end='')
    for i, column in enumerate(columns):
        print(column.ljust(col_width[i]), ' ', end='')
    print(END)
    for result in results:
        for i, item in enumerate(result):
            print(str(item).ljust(col_width[i]), ' ', end='')
        print()
    print()
    return
