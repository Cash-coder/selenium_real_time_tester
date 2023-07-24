# selenium_real_time_tester for bot development
Tool that takes functions as command line user input and execute those functions in selenium. 
This avoids having to code, execute, adjust, debug, execute the whole program again and again. 
Now you can test functions, xpaths and approaches without having to re run the entire program each time you change something
Ideal for developing bots with selenium, try xpaths, clicks, functions, etc .. without leaving or crushing the program


Future improvements stack:

-1  historic function list
    type hh or enter to get the history of the last x commands
    in a list, type list index to get that func into your clipboard
    automatic paste clipboard while in command line, edit and run again

-2  common function layout
    type: -fa variableName xpah 
    -f stands for function and -a for assign
    variableName xpah -> that xpath's element gets assigned to variableName
    ie: -fa e //h2 -> e = d.find_element(By.XPATH, "//h2")

    -fc -> function click
    -fr -> function refresh
    ...
