from os import write
import numpy as np
from tkinter import*
import time

#Creat Tkinter UI Interface
test = False
root = Tk()
test2 = False
var = IntVar()
fname = IntVar()
withname = IntVar()
balname = IntVar()
amountname = IntVar()
 
#Catogorise Bug Detection Count
over_under = 0
syntax = 0
dao = 0

#Output File Report
report = open('bugreport.txt', 'w')

#Check Commpiler Issue - Syntax Bug
''' 
This check catches if a smart contract is defined using the
^ operator for compiler version.

Best practice to use static rather than dynamic compiler version
as future versions could have unintended effects

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def compiler_issue(file):
    code = enumerate(open(file))
    bug = "^"
    score = 0
    for i, line in code:
        if bug in line:
            print("\nCompiler Bug Detected at Line: " + str(i + 1))
            print("Solution: Remove ^ operator as future compilers may have unintended effects")
            print("Risk: Medium")
            print("Confidence: High\n")
            
            report.write("\nCompiler Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Remove ^ operator as future compilers may have unintended effects")
            report.write("\nRisk: Medium")
            report.write("\nConfidence: High\n")
            
            score += 12
            global syntax
            syntax += 1

    return score

#Check Safe Math Issue - Overflow/Underflow Bug
''' 
This check catches if a smart contract is defined without
the Safe Math Library present when using uint variable type

Best practice to use Safe Math Library which can minimise attack
exploiting overflow/underflow vulnerabilities with arthimetic operations

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_safe_math(file):
    code = enumerate(open(file))
    library = "using SafeMath for uint"
    integer = "uint"
    func = "function"
    safe = False
    function_current = True
    start = True
    end_val = "}"
    score = 0
    for i, line in code:
        if end_val in line:
            #Next Code Segment
            function_current = True
            start = False
        else:
            start = True
        
        if (integer in line) and (safe == False) and (start == True):
            if library in line:
                function_current = False
                safe = True
                #Already using SafeMath Lib

        if (integer in line) and (safe == False) and (start == True):
            if (library not in line) and (function_current == True) and (func not in line):
                #Not using SafeMath Lib
                print("\nInteger Overflow/Underflow Bug Detected at Line: " + str(i + 1))
                print("Solution: Use SafeMath for uint library to minimise vulnerbaility")
                print("Risk: High")
                print("Confidence: High\n")
                
                report.write("\nInteger Overflow/Underflow Bug Detected at Line: " + str(i + 1))
                report.write("\nSolution: Use SafeMath for uint library to minimise vulnerbaility")
                report.write("\nRisk: High")
                report.write("\nConfidence: High\n")
                
                score+= 18
                global over_under
                over_under += 1
    return score

#Check Integer Operations - Overflow/Underflow Bug
''' 
This check catches if a smart contract uses arithemtic operations such as 
'+, -, *, /, %' when Safe Math functions could be used. 

Best practice to use Safe Math Library functions of add, sub, div, mod or mul 
which can minimise attack exploiting overflow/underflow vulnerabilities

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_integer_operations(file):
    code = enumerate(open(file))
    pos_inc = "++"
    neg_inc = "--"
    com = "//"
    ma_lib = ["+", "-", "*", "/", "%"]
    ma_lib_name = {"+":".add", "-":".sub", "*":".mul", "/":".div", "%":".mod"}   
    score = 0
    for i, line in code:
        for op in ma_lib:
            #Line uses arithmetic operations without safe math function
            if ( ((pos_inc not in line) or (neg_inc not in line)) and (op in line) and (com not in line)):    
                print("\nInteger Overflow/Underflow Bug Detected at Line: " + str(i + 1))
                print("Solution: Use SafeMath library operation " + ma_lib_name[op] + " to minimise vulnerbaility")
                print("Risk: Medium")
                print("Confidence: High\n")
                
                report.write("\nInteger Overflow/Underflow Bug Detected at Line: " + str(i + 1))
                report.write("\nSolution: Use SafeMath library operation " + ma_lib_name[op] + " to minimise vulnerbaility")
                report.write("\nRisk: Medium")
                report.write("\nConfidence: High\n")
                score+=18
                global over_under
                over_under += 1
    return score


#Check Loop Condition - Overflow/Underflow Bug
''' 
This check catches if a smart contract using operators such as >=, <= or uint
in a for or while loop condition statement

Best practice to use >, <, == or != loop for operations. Uint can cause
possible infinite loop

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_loop_condition(file):
    code = enumerate(open(file))
    type_1 = "for"
    type_2 = "while"
    var_type = "uint"
    use = "using"
    bug_1 = ">="
    bug_2 = "<="
    score = 0
    global over_under
    #Check for/while loop contains uint conditional statement
    for i, line in code:
        if((type_1 in line) or (type_2 in line)):
            if((bug_1 in line) or (bug_2 in line)):    
                print("\nLoop Integer Overflow/Underflow Bug Detected at Line: " + str(i + 1))
                print("Solution: When using uint for/while loop avoid >= or <= that could cause infinite loop")
                print("Instead use >, <, == or != loop operators")
                print("Risk: Low")  
                print("Confidence: Medium\n")
                    
                report.write("\nLoop Integer Overflow/Underflow Bug Detected at Line: " + str(i + 1))
                report.write("\nSolution: When using uint for/while loop avoid >= or <= that")
                report.write("\ncould cause infinite loop. Instead use >, <, == or != loop operators")
                report.write("\nRisk: Low")  
                report.write("\nConfidence: Medium\n")
                score+= 4
                over_under += 1
                
            if ((var_type in line) and (use not in line)):
                print("\nLoop Integer Overflow/Underflow Bug Detected at Line: " + str(i + 1))
                print("Solution: Careful when using uint within loop as could cause infinite loop check no")
                print("constant true condition can evaluate")
                print("Risk: High")  
                print("Confidence: Medium\n")
                    
                report.write("\nLoop Integer Overflow/Underflow Bug Detected at Line: " + str(i + 1))
                report.write("\nSolution: Careful when using uint within loop as could cause infinite loop check no")
                report.write("\nconstant true condition can evaluate")
                report.write("\nRisk: High")  
                report.write("\nConfidence: Medium\n")
                
                score+= 12
                over_under += 1
    return score

#Check Division Before Multiply - Overflow/Underflow Bug
''' 
This check catches if a smart contract has mathematical operations with
multiplication or division, that division occurs first 

Best practice to use have multiplication first, as division first can
cause loss of pecision in operations 

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_div_multiply(file):
    code = enumerate(open(file))
    div_op = "/"
    div_op_safe = "div"
    mul_op = "*"
    mul_op_safe = "mul"
    outer = ")"
    inner = "("
    score = 0
    for i, line in code:
        if (((div_op in line) or (div_op_safe in line)) and ((mul_op in line) or (mul_op_safe in line))):
            if ((outer in line) and (inner in line)):
                #Extract content from within bracket operations
                content = line[line.find(inner)+len(inner):line.rfind(outer)]
                if ((div_op in content) or (div_op_safe in content)):
                    #Check division is first expression in brackets
                    print("\nDivsion before multiply Bug Detected at Line: " + str(i + 1))
                    print("Solution: Re-Order expression with multiplication first as integer truncation \
                        \nwith loss of precision to minimise vulnerbaility")
                    print("Risk: Medium")  
                    print("Confidence: Medium\n")
                    
                    report.write("\nDivsion before multiply Bug Detected at Line: " + str(i + 1))
                    report.write("\nSolution: Re-Order expression with multiplication first as integer truncation")
                    report.write("\nwith loss of precision to minimise vulnerbaility")
                    report.write("\nRisk: Medium")  
                    report.write("\nConfidence: Medium\n")
                    score+= 8
                    global over_under
                    over_under += 1
    return score            
                    
#Check Unary Operations Warning - Overflow/Underflow Bug
''' 
This check catches if a smart contract contains =+, =- or =* 
which could be intended as =+, -= or *=

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_unary(file):
    code = enumerate(open(file))
    bug_plus = "=+"
    bug_minus = "=-"
    bug_times = "=*"
    score = 0
    for i, line in code:
        #Check if plus/minus/product unary error exists
        if ((bug_plus in line) or (bug_minus in line) or (bug_times in line)):
            print("\nDangerous Unary Expression Bug Detected at Line: " + str(i + 1))
            print("Solution: Check correct use could have meant += or -= or *=")
            print("Risk: Low")  
            print("Confidence: High\n")
            
            report.write("\nDangerous Unary Expression Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Check correct use could have meant += or -= or *=")
            report.write("\nRisk: Low")  
            report.write("\nConfidence: High\n")
            score += 6
            global over_under
            over_under += 1
    return score


#Check Type Reference - Overflow/Underflow Bug
''' 
This check catches if a smart contract defined variable using var
instead of using numerical data type of uint

Should explicitly declare uint data types to 
avoid unexpected behaviors

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_type_infer(file):
    code = enumerate(open(file))
    score = 0
    key = "var"
    start = "= "
    end = ";"
    for i, line in code:
        if (key in line):
            #Extract value of var definition
            value = line[line.find(start)+len(start):line.rfind(end)]
            if (value.isnumeric()):
                #Check if value from var data type is numeric violation
                print("\nUnsafe Type Innference Overflow/Underflow Bug Detected at Line: " + str(i + 1))
                print("Solution: Explicitly declare uint data types to avoid unexpected behaviors")
                print("Risk: Medium")  
                print("Confidence: High\n")
            
                report.write("\nUnsafe Type Innference Overflow/Underflow Bug Detected at Line: " + str(i + 1))
                report.write("\nSolution: Explicitly declare uint data types to avoid unexpected behaviors")
                report.write("\nRisk: Medium")  
                report.write("\nConfidence: High\n")
                score += 12
                global over_under
                over_under += 1
    return score

#Check Boolan Constance - Syntax Bug
''' 
This check catches if a smart contract incorporates Boolean
Constance or Tautology conditions

Should verify that Tautology is not intended as well as Constance
is not indended

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_bool_const(file):
    code = enumerate(open(file))
    bug_one = "(false)"
    bug_two = "(true)"
    bug_three = "|| true"
    bug_four = "|| false"
    bug_five = "true ||"
    bug_six = "false ||"
    bug_seven = "&& true"
    bug_eight = "&& false"
    bug_nine = "true &&"
    bug_ten = "false &&"
    key = "if"
    var_one = " = true"
    var_two = " = false"
    score = 0
    
    global syntax

    for i, line in code:
        #Check all conditions of true or false bugs exist
        if ((bug_one in line) or (bug_two in line) or (bug_three in line) or (bug_four in line) or (bug_five in line)):
            print("\nBoolean Constant Bug Detected at Line: " + str(i + 1))
            print("Solution: Simplify condition or verify code is not a mistake in boolen const")
            print("Risk: Low")   
            print("Confidence: High\n")
            
            report.write("\nBoolean Constant Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Simplify condition or verify code is not a mistake in boolen const")
            report.write("\nRisk: Low")   
            report.write("\nConfidence: High\n")
            score+= 6
            syntax += 1
                   
        if ((bug_six in line) or (bug_seven in line) or (bug_eight in line) or (bug_nine in line) or (bug_ten in line)):
            print("\nBoolean Constant Bug Detected at Line: " + str(i + 1))
            print("Solution: Simplify condition or verify code is not a mistake in boolen const")
            print("Risk: Low")   
            print("Confidence: High\n")
            
            report.write("\nBoolean Constant Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Simplify condition or verify code is not a mistake in boolen const")
            report.write("\nRisk: Low")   
            report.write("\nConfidence: High\n")
            score+= 6
            syntax += 1

        if((key in line) and ((var_one in line) or (var_two in line))):
            #If statement tautology check
            print("\nBoolean Constant Bug Detected at Line: " + str(i + 1))
            print("Solution: Verify whether mistake of tautology")
            print("Risk: Low")   
            print("Confidence: High\n")
            
            report.write("\nBoolean Constant Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Verify whether mistake of tautology")
            report.write("\nRisk: Low")   
            report.write("\nConfidence: High\n")
            score+= 6
            syntax += 1
    return score

#Check Array Length Assignement - Syntax Bug
''' 
This check catches if a smart contract defined an array 
with a static length

Should increase array length as array grows and storage needed

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_arr_length(file):
    code_first = enumerate(open(file))
    code_second = enumerate(open(file))
    inner = "[] "
    outer = ";"
    key = ".length"
    operator = "="
    names = np.array([])
    concat_names = np.array([])
    score = 0
    
    #Extract all array names from contract
    for i, line in code_first:
        if ((inner in line)):
            arrayname = line[line.find(inner)+len(inner):line.rfind(outer)]
            exists = False
            for value in names:
                if (value == arrayname):
                    exists = True      
            if (exists == False):
                names = np.append(names, arrayname)
                concat_names = np.append(concat_names, (arrayname + key))

    #Now we have the arrays check if length is set
    for i, line in code_second:
        for arr in concat_names:
            if ((arr in line) and (operator in line)): 
                print("\nArray Length Assignement Bug Detected at Line: " + str(i + 1))
                print("Solution: Don't set array length directly, add values as needed storage could be vulnerble")
                print("Risk: Medium") 
                print("Confidence: Medium\n")
                
                report.write("\nArray Length Assignement Bug Detected at Line: " + str(i + 1))
                report.write("\nSolution: Don't set array length directly, add values as needed storage could be vulnerble")
                report.write("\nRisk: Medium") 
                report.write("\nConfidence: Medium\n")
                score += 8
                global syntax
                syntax += 1
    return score  

#Check Missing Zero Address - Syntax Bug
''' 
This check catches if a smart contract function does not
check that the address is zero using: 
        - address(0)
        - 0x0
        - address(0x0)

Check address is not zero using require and address variable
reduce liklihood of interaction with a null address

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_address_zero(file):
    code = enumerate(open(file))
    score = 0;
   
    func = "function"
    add = "address"
    not_eq = "!="
    req = "require"
    big = ">"
    zero = "0"
    
    #Checks required
    type_1 = "address(0)"
    type_2 = "0x0"
    type_3 = "address(0x0)"
    
    #Find Address name in function
    address_name = ""
    add_function_start = False
    end_func = "}"
    end_len = 6
    overall_safe = False
    req_safe = False
    add_zero_safe = False
    function_line = 0
    
    #Start in function when find address stop when function ends
    for i, line in code:
        if ((add_function_start == True) and (end_func in line) and (len(line) == end_len)):
            #Here we can do print and write output
            if (overall_safe == False):
                
                print("\nZero Address Check Bug Detected at Function Line: " + str(function_line))
                print("Solution: Check address is not zero using require, address variable and checking")
                print("it is not equal to either 'address(0)', '0x0' or 'address(0x0)'")
                print("Risk: Medium") 
                print("Confidence: High\n")
                
                report.write("\nZero Address Check Bug Detected at Function Line: " + str(function_line))
                report.write("\nSolution: Check address is not zero using require, address variable and checking")
                report.write("\nit is not equal to either 'address(0)', '0x0' or 'address(0x0)'")
                report.write("\nRisk: Medium") 
                report.write("\nConfidence: High\n")
                
                score += 12
                global syntax
                syntax += 1
                
            #Reset Variables for next function
            address_name = ""
            add_function_start = False
            overall_safe = False
            req_safe = False
            add_zero_safe = False        
            function_line = 0

        if ((func in line) and (add in line)):
            add_function_start = True
            function_line = i + 1
            #Here we parse the address name
            start = "(address"
            end = ")"
            address_name =  line[line.find(start)+len(start):line.rfind(end)].replace(" ", "")
             
        if(add_function_start == True):
            #Here we are in the function and we check require and not null address exists
            if (req in line):
                req_safe = True
                if((address_name in line) and (not_eq in line)):
                    if((type_1 in line) or (type_2 in line) or (type_3 in line)):
                        add_zero_safe = True
                     
            
                if(((type_1 in line) or (type_2 in line) or (type_3 in line))):
                    add_zero_safe = True   
                    
                if(((big in line) and (zero in line))):
                    add_zero_safe = True  
                    
            if ((add_zero_safe == True) and (req_safe == True)):
                overall_safe = True
                
    return score

#Check Map Struct Deletion - Syntax Bug
''' 
This check catches if a smart contract either defines a map
struct as a different data type or uses delete keyword for 
mapping delete which doesnt not delete the entire mapping
only deletes entry

Should Use same data type key as defined in struct for mapping. 
Use lock technqiue mechanism to disable mapping structure 
if needed to remove

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_map_struct_delete(file):
    code = enumerate(open(file))
    code_1 = enumerate(open(file))
    code_2 = enumerate(open(file))

    score = 0;
   
    pub = "public"
    priv = "private"
    struct = "struct"
    mapp = "mapping"
    supress = ";"
    func = "function"
    before_type = "("
    after_type = " =>"
    after_dest = ") "
    empty = " "
    
    start_search = False
    end_struct = "}"
    start_struct = "{"
    end_len = 6
    struct_name = ""
    dtype = ""
    
    struct_dtype = {}
    
    global syntax

    
    #Find Struct Names if this struct contains a map then store it in np array
    for i, line in code:
        
        if((start_search == True) and (end_struct in line) and (len(line) == end_len)):
            start_search = False
            struct_name = ""
            dtype = ""
            
        if (struct in line):
            start_search = True
            #Get struct name
            struct_name = line[line.find(struct)+len(struct):line.rfind(start_struct)].replace(" ", "")
        
        if((mapp in line) and (start_search == True)):
            #Here store the data type with the struct name in dictionary
            dtype = line[line.find(before_type)+len(before_type):line.rfind(after_type)].replace(" ", "")
            entry = {struct_name:dtype}
            struct_dtype.update(entry)
       
    defined_mappings = np.array([])
    #Look for mapping outside of struct and store its name in array
    for i, line in code_1:
        
        if (mapp in line):
            for struct_name, dtype in struct_dtype.items():
                if ((struct_name in line) and (dtype in line)):
                    if (pub in line):
                        map_name = line[line.find(pub)+len(pub):line.rfind(supress)]
                        map_name.replace(" ", "")  
                        defined_mappings = np.append(defined_mappings, map_name)
                    if (priv in line):
                        map_name = line[line.find(priv)+len(priv):line.rfind(supress)]
                        map_name.replace(" ", "")  
                        defined_mappings = np.append(defined_mappings, map_name)
                if ((struct_name in line) and (dtype not in line)):
                    print("\nMapping Data Type Mismatch Bug detected Line: " + str(i+1))
                    print("Solution: Use same data type key as defined in struct for mapping")
                    print("Risk: Low") 
                    print("Confidence: Medium\n")
                
                    report.write("\nMapping Data Type Mismatch Bug detected Line: " + str(i+1))
                    report.write("\nSolution: Use same data type key as defined in struct for mapping")
                    report.write("\nRisk: Low") 
                    report.write("\nConfidence: Medium\n")
                    
                    score += 4
                    syntax += 1
                    
                    if (pub in line):
                        map_name = line[line.find(pub)+len(pub):line.rfind(supress)]
                        map_name.replace(" ", "")  
                        defined_mappings = np.append(defined_mappings, map_name)
                    if (priv in line):
                        map_name = line[line.find(priv)+len(priv):line.rfind(supress)]
                        map_name.replace(" ", "")  
                        defined_mappings = np.append(defined_mappings, map_name)
                if ((struct_name in line) and (priv not in line) and (pub not in line)):
                    map_name = line[line.find(after_dest)+len(after_dest):line.rfind(supress)]
                    map_name.replace(" ", "")  
                    defined_mappings = np.append(defined_mappings, map_name)
        
    #Look for functions that fail to delete mapping
    start_func = False
    delete = "delete"
    func_line = 0
    
    for i, line in code_2:
        if ((start_func == True) and (end_struct in line) and (len(line) == end_len)):
            start_func = False
            func_line = 0

        if (func in line):
            start_func = True
            func_line = i + 1

            
        if ((start_func == True) and (delete in line)):
            for name in defined_mappings:
                if (name in line):
                    
                    print("\nMapping Deletion Bug detected Line: " + str(i+1))
                    print("Only single item removed not entire mapping from mapping struct: " + name)
                    print("From deletion Function in line: " + str(func_line))
                    print("Solution: Use lock technqiue mechanism to disable mapping structure if needed to remove")
                    print("Risk: Medium") 
                    print("Confidence: High\n")
                
                    report.write("\nMapping Deletion Bug detected Line: " + str(i+1))
                    report.write("\nOnly single item removed not entire mapping from mapping struct: " + name)
                    report.write("\nFrom deletion Function in line: " + str(func_line))
                    report.write("\nSolution: Use lock technqiue mechanism to disable mapping structure if needed to remove")
                    report.write("\nRisk: Medium") 
                    report.write("\nConfidence: High\n")
                    
                    score += 12        
                    syntax += 1
    return score


#Check Uninitialised Storage Variable - Syntax Bug
''' 
This check catches if a smart contract includes struct variables
which are not set when using struct

Should Immediatly initalise storage variables could be ovveridded

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_init_storage_var(file):
    code_first = enumerate(open(file))
    code_second = enumerate(open(file))
    inner = "struct"
    con = "con"
    outer = " {" 
    req = "="
    req_end = ";"
    names = np.array([])
    var_one = "uint"
    var_two = "address"
    score = 0
    struct_exists = False
    
    global syntax

    #Get all struct names
    for i, line in code_first:
        if ((inner in line) and (con not in line)):
            struct_exists = True
        if (inner in line):
            struct_name = line[line.find(inner)+len(inner):line.rfind(outer)]
            exists = False
            for value in names:
                if (value == struct_name):
                    exists = True      
            if (exists == False):
                names = np.append(names, struct_name)
    #Look for uninitialised variables 
    for i, line in code_second:
        #Look for struct varibales 
        if (struct_exists == True):
            for var in names:
                if((var in line) and (req_end in line) and (req not in line)):
                    print("\nUninitialised Storage Variable Bug Detected at Line: " + str(i + 1))
                    print("Solution: Immediatly initalise storage variables could be ovveridded")
                    print("Risk: High") 
                    print("Confidence: Low\n")
                
                    report.write("\nUninitialised Storage Variable Bug Detected at Line: " + str(i + 1))
                    report.write("\nSolution: Immediatly initalise storage variables could be ovveridded")
                    report.write("\nRisk: High") 
                    report.write("\nConfidence: Low\n")
                
                    score += 6
                    syntax += 1
            if((var_one in line) and (req_end in line) and (req not in line)):
                print("\nUninitialised Storage Variable Bug Detected at Line: " + str(i + 1))
                print("Solution: Immediatly initalise storage variables could be ovveridded")
                print("Risk: High") 
                print("Confidence: Low\n")
                
                report.write("\nUninitialised Storage Variable Bug Detected at Line: " + str(i + 1))
                report.write("\nSolution: Immediatly initalise storage variables could be ovveridded")
                report.write("\nRisk: High") 
                report.write("\nConfidence: Low\n")
                
                score += 6
                syntax += 1
                
            if((var_two in line) and (req_end in line) and (req not in line)):
                print("\nUninitialised Storage Variable Bug Detected at Line: " + str(i + 1))
                print("Solution: Immediatly initalise storage variables could be ovveridded")
                print("Risk: High") 
                print("Confidence: Low\n")
                
                report.write("\nUninitialised Storage Variable Bug Detected at Line: " + str(i + 1))
                report.write("\nSolution: Immediatly initalise storage variables could be ovveridded")
                report.write("\nRisk: High") 
                report.write("\nConfidence: Low\n")
                
                score += 6
                syntax += 1
                
    return score

#Check Incorrect Shift Assembely - Syntax Bug
''' 
This check catches if a smart contract includes an assembly
shift that has parameters mismatched in their order

When using shr assembly shift if first position is a variable 
and second is constant, this bit shift is usually unintended

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_assemble_shift(file):
    code = enumerate(open(file))
    key = "assembly"
    end = "}"
    start = False
    shift = "shr"
    inner_one = "shr("
    outer_one = ","
    inner_two = ", "
    outer_two = ")"
    score = 0
    for i, line in code:
        if((start == True) and (end in line)):
            start = False
        if (key in line):
            start = True
        #If inside assemble call extract 2 variables or bit shit value 
        if ((shift in line) and (start == True)): 
            char_one = line[line.find(inner_one)+len(inner_one):line.rfind(outer_one)]
            char_two = line[line.find(inner_two)+len(inner_two):line.rfind(outer_two)]
            if ((char_two.isnumeric() == True) and (char_one.isnumeric() is False )):
                print("\nIncorrect Shit In Assembly Bug Detected at Line: " + str(i + 1))
                print("Solution: Swap order of parametres in shift")
                print("Risk: Medium") 
                print("Confidence: Medium\n")
                
                report.write("\nIncorrect Shit In Assembly Bug Detected at Line: " + str(i + 1))
                report.write("\nSolution: Swap order of parametres in shift")
                report.write("\nRisk: Medium") 
                report.write("\nConfidence: Medium\n")
                
                score += 8
                global syntax
                syntax += 1
                    
    return score

#Check Self Destruct - Syntax Bug
''' 
This check catches if a smart contract contains a self destruct with address
or a function that is public and uses self destruct

When address in self destruct address is not used as could 
send ether to an attacker contract. If using self detruct 
restrict access to function as not public

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_self_destruct(file):
    code = enumerate(open(file))
    code_second = enumerate(open(file))

    key_func = "function"
    key_visibility = "public"
    bug = "selfdestruct"
    end = "}"
    length = 2
    current = False
    score = 0
    
    global syntax
    
    #Case 1 Address to another contract
    for i, line in code:
        if ((bug in line)):
            print("\nSelf Destruct Vulnerability Detected at Line: " + str(i + 1))
            print("Solution: Check that address is not used as could send ether to an attacker contract")
            print("Risk: Medium")          
            print("Confidence: Low\n")
            
            report.write("\nSelf Destruct Vulnerability Detected at Line: " + str(i + 1))
            report.write("\nSolution: Check that address is not used as could send ether to an attacker contract")
            report.write("\nRisk: Medium")          
            report.write("\nConfidence: Low\n")
            
            score += 4
            syntax += 1
    #Case 2 public function with selfdestruct
    for i, line in code_second:
        if ((current == True) and (len(line) <= length) and (end in line)):
            current = False
        if ((key_func in line) and (key_visibility in line)):
            current = True
        if ((current == True) and (bug in line)):
            print("\nSelf Destruct Vulnerability Detected at Line: " + str(i + 1))
            print("Solution: If using self detruct restrict access to function as not public")
            print("Risk: High") 
            print("Confidence: High\n")
            
            report.write("\nSelf Destruct Vulnerability Detected at Line: " + str(i + 1))
            report.write("\nSolution: If using self detruct restrict access to function as not public")
            report.write("\nRisk: High") 
            report.write("\nConfidence: High\n")
            
            score += 18
            syntax += 1
                
    return score


#Check Transfer Gas/Funds - Syntax Bug
''' 
This check catches if a smart contract contains call.value
or send value methods

Use transfer function instead of send/call operation as they don't capture 
transaction fails to minimise vulnerbaility

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_transfer(file):
    code = enumerate(open(file))
    bug_1 = ".send("
    bug_2 = "call.value"
    score = 0
    
    global syntax
    
    for i, line in code:
        #check if send or call.value used in contract
        if bug_1 in line:
            print("\nUnhadled Exceptions Bug Detected at Line: " + str(i + 1))
            print("Solution: Use transfer function instead of send operation as send doesn't capture \
                \ntransaction fails to minimise vulnerbaility")
            print("Risk: Medium") 
            print("Confidence: High\n")
            
            report.write("\nUnhadled Exceptions Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Use transfer function instead of send operation as send doesn't capture")
            report.write("\ntransaction fails to minimise vulnerbaility")
            report.write("\nRisk: Medium") 
            report.write("\nConfidence: High\n")
            
            score +=12  
            syntax += 1
                       
        elif bug_2 in line:
            print("\nUnhadled Exceptions Bug Detected at Line: " + str(i + 1))
            print("Solution: Use transfer function operation since call has no gas limit to minimise vulnerbaility")
            print("Risk: Medium")  
            print("Confidence: High\n")
            
            report.write("\nUnhadled Exceptions Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Use transfer function operation since call has no gas limit to minimise vulnerbaility")
            report.write("\nRisk: Medium")  
            report.write("\nConfidence: High\n")
            
            score += 12
            syntax += 1
    return score          
            
#Check Bytes - Syntax Bug
''' 
This check catches if a smart contract contains bytes array
instead of using bytes

Use bytes instead of byte array as this could grow and access
un intended storage

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_bytes(file):
    code = enumerate(open(file))
    pattern = "bytes"
    pattern_variant = "byte"
    key_array = "[]"
    score = 0
    
    #Search for bytes[] or byte[] exist
    for i, line in code:
        if (((pattern in line) and (key_array in line)) or ((pattern_variant in line) and (key_array in line))):
            print("\nStorage Bug Detected at Line: " + str(i + 1))
            print("Solution: Use bytes instead of bytes[] array to minimise vulnerbaility")
            print("Risk: Low")  
            print("Confidence: High\n")
            
            report.write("\nStorage Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Use bytes instead of bytes[] array to minimise vulnerbaility")
            report.write("\nRisk: Low")  
            report.write("\nConfidence: High\n")
            
            score += 6
            global syntax
            syntax += 1
    return score  

#Check txOrigin - Syntax Bug
''' 
This check catches if a smart contract contains txorigin function 

Use msg.sender instead of tx.origin to minimise vulnerbaility. tx.Orgin is
vulnerable for authentication as it can be manipulated to be equal to an
owner address hence pass the require tests

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_tx_origin(file):
    code = enumerate(open(file))
    bug = "tx.origin"
    score = 0
    
    #Search for all invocations of tx.origin
    for i, line in code:
        if bug in line:
            print("\nAuthentication Bug Detected at Line: " + str(i + 1))
            print("Solution: Use msg.sender instead of tx.origin to minimise vulnerbaility")
            print("Risk: High") 
            print("Confidence: High\n") 
            
            report.write("\nAuthentication Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Use msg.sender instead of tx.origin to minimise vulnerbaility")
            report.write("\nRisk: High") 
            report.write("\nConfidence: High\n") 
            
            score += 18
            global syntax
            syntax += 1
    return score
            
#Check Function Visibility - Syntax Bug
''' 
This check catches if a smart contract contains functions
with unknown visibility


Use at least minimum public/private specifier when 
defining function to minimise vulnerbaility

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_function_visibility(file):
    code = enumerate(open(file))
    type_1 = "public"
    type_2 = "private"
    keyword = "function"
    type_3 = "internal"
    type_4 = "onlyOwner"
    type_5 = "external"
    score = 0
    
    #Find all functions check if visibility is set
    for i, line in code:
        if (keyword in line) and not((type_1 in line) or (type_2 in line) or (type_3 in line) or (type_4 in line) or (type_5 in line)):
            print("\nVisibility Bug Detected at Line: " + str(i + 1))
            print("Solution: Use public/private specifier when defining function to minimise vulnerbaility")
            print("Risk: High") 
            print("Confidence: High\n")
            
            report.write("\nVisibility Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Use public/private specifier when defining function to minimise vulnerbaility")
            report.write("\nRisk: High") 
            report.write("\nConfidence: High\n")
            
            score += 18
            global syntax
            syntax += 1
    return score
 
#Check Balance Equality - Syntax Bug
''' 
This check catches if a smart contract double equals for
evaluation of a balance variable

Use compartive statements instead of double equals to 
minimise vulnerbaility

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_balance_equality(file):
    code = enumerate(open(file))
    bug = ".balance =="
    score = 0
    
    #Search for balance equality statements
    for i, line in code:
        if bug in line:
            print("\nEquality Bug Detected at Line: " + str(i + 1))
            print("Solution: Use compartive statements instead of double equals to minimise vulnerbaility")
            print("Risk: Medium") 
            print("Confidence: Low\n")
            
            report.write("\nEquality Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Use compartive statements instead of double equals to minimise vulnerbaility")
            report.write("\nRisk: Medium") 
            report.write("\nConfidence: Low\n")
            
            score += 4
            global syntax
            syntax += 1
                    
    return score

#Check Block Timestamp - Syntax Bug
''' 
This check catches if a smart contract contains
block.timestamp for randomness

Avoid block.randomness for randomness to minimise DoS vulnerbaility

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_block_timestamp(file):
    code = enumerate(open(file))
    bug = "block.timestamp"
    score = 0
    
    #Search for call of block violation bug
    for i, line in code:
        if bug in line:
            print("\nRandomness Bug Detected at Line: " + str(i + 1))
            print("Solution: Avoid block.randomness for randomness to minimise DoS vulnerbaility")
            print("Risk: Low")                
            print("Confidence: High\n")
            
            report.write("\nRandomness Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Avoid block.randomness for randomness to minimise DoS vulnerbaility")
            report.write("\nRisk: Low")                
            report.write("\nConfidence: High\n")
            score += 6
            global syntax
            syntax += 1
    return score

#Check Block Variable - Syntax Bug
''' 
This check catches if a smart contract contains
block.timestamp/gaslimit or difficulty

Potenital leaky PRNGS rely heavily on past block hashes 
future vulnerbility

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_block_variable(file):
    code = enumerate(open(file))
    bug_coin = "block.coinbase"
    bug_gas = "block.gaslimit"
    bug_diff = "block.difficulty"
    score = 0
    
    #Search for call of block violation bug
    for i, line in code:
        if ((bug_coin in line) or (bug_gas in line) or (bug_diff in line)):
            print("\nBlock Variable Dependency Bug Detected at Line: " + str(i + 1))
            print("Solution: Potenital leaky PRNGS rely heavily on past block hashes future vulnerbility")
            print("Risk: Low") 
            print("Confidence: High\n")
            
            report.write("\nBlock Variable Dependency Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Potenital leaky PRNGS rely heavily on past block hashes future vulnerbility")
            report.write("\nRisk: Low") 
            report.write("\nConfidence: High\n")
            
            score+= 6
            global syntax
            syntax += 1
    return score

#Check Block Number - Syntax Bug
''' 
This check catches if a smart contract contains
block.number

Check function when getting current block number
could be invoked by an attacker for malicious intent

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_block_number(file):
    code = enumerate(open(file))
    bug = "block.number"
    score = 0
    
    #Search for call of block violation bug
    for i, line in code:
        if (bug in line):
            print("\nBlock Number Dependency Bug Detected at Line: " + str(i + 1))
            print("Solution: Could be invoked by an attacker for malicious intent")
            print("Risk: Low") 
            print("Confidence: High\n")
            
            report.write("\nBlock Number Dependency Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Could be invoked by an attacker for malicious intent")
            report.write("\nRisk: Low") 
            report.write("\nConfidence: High\n")
            
            score += 6
            global syntax
            syntax += 1
    return score
            
#Check Delegate Call - Syntax Bug
''' 
This check catches if a delegate call is made, 
potential for parity sig wallet attack

Avoid Delegate Call this can lead to unexpected code 
execution vulnerbaility

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_delegate_call(file):
    code = enumerate(open(file))
    bug = "delegatecall"
    bug_var = "DelegateCall"
    score = 0
    
    #Search for call of Delegate Call violation bug
    for i, line in code:
        if ((bug in line) or (bug_var in line)):
            print("\nDelegate Call Bug Detected at Line: " + str(i + 1))
            print("Solution: Avoid Delegate Call this can lead to unexpected code execution vulnerbaility")
            print("Risk: Medium") 
            print("Confidence: High\n")
            
            report.write("\nDelegate Call Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Avoid Delegate Call this can lead to unexpected code execution vulnerbaility")
            report.write("\nRisk: Medium") 
            report.write("\nConfidence: High\n")
            
            score += 12
            global syntax
            syntax += 1
    return score

#Check Loop Function Call - Syntax Bug
''' 
This check catches if a function call is made 
within a for or while loop

Avoid Function Call In For/While Loop possible DoS vulnerbaility

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_loop_function(file):
    code = enumerate(open(file))
    loop_for = "for"
    loop_while = "while"
    start_loop = "{"
    use = "using"
    bug = "."
    function_current = False
    loop_start = False
    end_val = "}"
    score = 0
    
    #Search for any function calls when for/while loop starts
    for i, line in code:
        if (bug in line) and (function_current == True):
            print("\nFor/While Loop Function Call Bug Detected at Line: " + str(i + 1))
            print("Solution: Avoid Function Call In For/While Loop possible DoS vulnerbaility")
            print("Risk: Medium")   
            print("Confidence: High\n")
            
            report.write("\nFor/While Loop Function Call Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Avoid Function Call In For/While Loop possible DoS vulnerbaility")
            report.write("\nRisk: Medium")   
            report.write("\nConfidence: High\n")
            
            score += 12
            global syntax
            syntax += 1
       
        if (((loop_for in line) or (loop_while in line)) and (use not in line) and (start_loop in line)):
            function_current = True
            loop_start = True            

        if (end_val in line) and (loop_start == True):
            #Next Function 
            function_current = False
            loop_start = False
    return score

#Check Over Powered Owner - Syntax Bug
''' 
This check catches if a contract bases function control and 
execution on the owner. Or a modifier function is used to
define an owner.

Owner private key at risk of being comprimised don't base 
function control on owner or use an owner modifier function

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_owner_power(file):
    code = enumerate(open(file))
    code_1 = enumerate(open(file))
    code_2 = enumerate(open(file))
    code_3 = enumerate(open(file))
    
    score = 0
    global syntax
    
    #General Req
    add = "address"
    own = "owner"
    constructor = "constructor"
    creator = "msg.sender"
    cont = False
    
    for i, line in code:
        if ((add in line) and (own in line)):
            cont = True
    
    #Case 1 using constructor
    start_con = False
    con_defined = False
    con_end_char = "}"
    end_len = 6
    func = "function"
    req = "require"
    start_func = False
    func_end_char = "}"
    if (cont == True):
        for i, line in code_1:
            if ((con_end_char in line) and (len(line) == end_len)):
                start_con = False
            if ((func_end_char in line) and (len(line) == end_len)):
                start_func = False       
            if (constructor in line):
                start_con = True
            if (start_con == True):
                #look for case
                if ((own in line) and (creator in line)):
                    con_defined = True
            if ((func in line) and (start_con == False) and (con_defined == True)):
                start_func = True
            if(start_func == True):
                if ((req in line) and (own in line) and (creator in line)):
                    print("\nOver Powered Owner Bug Detected at Line: " + str(i + 1))
                    print("Solution: Owner private key at risk of being comprimised don't base function control on owner")
                    print("Risk: High")   
                    print("Confidence: Medium\n")
            
                    report.write("\nOver Powered Owner Bug Detected at Line: " + str(i + 1))
                    report.write("\nSolution: Owner private key at risk of being comprimised") 
                    report.write("\ndon't base function control on owner")
                    report.write("\nRisk: High")   
                    report.write("\nConfidence: Medium\n") 
                    
                    score += 12
                    syntax += 1
           
    #Case 2 using modifer
    mod = "modifier "
    mod_last_part = "{"
    start_mod = False
    mod_end_char = "}"
    mod_exists = False
    modifier_name = ""
    mod_names = np.array([])
    inner = "("
    outer = ")"
    req_found = False
    owner_found = False
    msg_sender_found = False
    
    #List unkown size of owner modifiers
    for i, line in code_2:
        if ((start_mod == True) and (mod_end_char in line) and (len(line) == end_len)):
            start_mod = False
            if ((req_found == True) and (owner_found == True) and (msg_sender_found == True)):
                mod_exists = True
                mod_names = np.append(mod_names, modifier_name)
            req_found = False
            owner_found = False
            msg_sender_found = False
            modifier_name = ""
        if ((mod in line) and (inner not in line) and (outer not in line)):
            start_mod = True
            modifier_name = line[line.find(mod)+len(mod):line.rfind(mod_last_part)].replace(" ", "")
            #assign potential mod name here
        if ((start_mod == True) and (req in line)):
            req_found = True

        if ((start_mod == True) and (own in line)):
            owner_found = True

        if ((start_mod == True) and (creator in line)):
            msg_sender_found = True

    for i, line in code_3:
        if ((mod_exists == True) and (func in line)):
            for mod_variable in mod_names:
                if (mod_variable in line):
                    print("\nOver Powered Owner Bug Detected at Line: " + str(i + 1))
                    print("Solution: Owner private key at risk of being comprimised don't use modifier function") 
                    print("control of owner for functions")
                    print("Risk: High")   
                    print("Confidence: Medium\n")
            
                    report.write("\nOver Powered Owner Bug Detected at Line: " + str(i + 1))
                    report.write("\nSolution: Owner private key at risk of being comprimised don't use modifier function") 
                    report.write("\ncontrol of owner for functions")
                    report.write("\nRisk: High")   
                    report.write("\nConfidence: Medium\n") 
                    
                    score += 12
                    syntax += 1   
    return score

#Check Multiple Constructors - Syntax Bug
''' 
This check catches if a contract defines multiple constructors
either through constructor or a function constructor. Checks wether
same variables are defined over multiple constructors could be
overwritten. 

Use single constructor to initialise contract second constructor 
will be ignoreded. Use single constructor and intialise variables 
once in constructor

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_constructor_init(file):
    code = enumerate(open(file))
    code_1 = enumerate(open(file))
    code_2 = enumerate(open(file))
    score = 0
    global syntax

    start = " "
    end = ";"
    equal = "="
    con = "constructor"
    func = "function"
    mod = "modifier"
    struct = "struct"
    
    #List of variables defined prior to other parts in contract
    var_names = np.array([])
    
    #Store contrcat name
    contract_name = "";
    cont = "contract"
    con_end = "{"
    con_count = 0
    
    #Get init variable names
    for i, line in code:
        if (cont in line):
            contract_name = line[line.find(cont)+len(cont):line.rfind(con_end)].replace(" ", "")
            con_count +=1
        if((con in line) or (func in line) or (mod in line) or (struct in line)):
            break;
        if ((end in line) and (equal not in line)):
            #Find and store variable name in list 
            sub = line[line.find(start)+len(start):line.rfind(end)]
            dtype = sub[sub.find(start)+len(start):sub.rfind(start)]            
            var = line[line.find(dtype)+len(dtype):line.rfind(end)].replace(" ", "")
            var_names = np.append(var_names, var)

    #Case Overloading with old scheme using consturtor and function contract methods of consturctr 
    count = 0
    con_line = 0;
    func_line = 0;
    
    #Case 1 Multiple Constructors
    for i, line in code_1:
        #Case 1 we have 2 Constructors Defined causes unintended effect
        if (con in line):
            count += 1
            con_line = i + 1
        if ((func in line) and (contract_name in line)):
            count += 1
            func_line = i + 1
        
    if ((count >= 2) and (con_count <= 1)):
        print("\nMultiple Constructors Defined with constructor at Line: " + str(con_line))
        print("And function constructor at Line " + str(func_line))
        print("Solution: Use single constructor to initialise contract second constructor will be ignored") 
        print("Risk: Low")   
        print("Confidence: Medium\n")
        
        report.write("\nMultiple Constructors Defined with constructor at Line: " + str(con_line))
        report.write("\nAnd function constructor at Line " + str(func_line))
        report.write("\nSolution: Use single constructor to initialise contract second constructor will be ignored")
        report.write("\nRisk: Low")  
        report.write("\nConfidence: Medium\n")
        
        score += 4
        syntax += 1

    found_vars = np.array([])
    
    #Constructor
    start_con = False
    length = 6
    
    #Function
    start_func = False
    func_con_end =  "}"
    
    #Case 2 Defined Variables Across Multiple Constructors 
    for i, line in code_2:
        if ((func_con_end in line) and (start_con == True) and (len(line) == length)):
            start_con = False
            
        if ((con in line) and (start_con == False)):
            start_con = True
            
        if((func in line) and (contract_name in line) and (start_func == False)):
            start_func = True
    
        if ((func_con_end in line) and (start_func == True) and (len(line) == length)):
            start_func = False
    
        if((start_con == True) and (equal in line) and (end in line)):
            for current_var in var_names:
                if ((current_var in line)):
                    found_vars = np.append(found_vars, current_var)
                    
        if (start_func == True):
            for con_var in found_vars:
                if (con_var in line):
                    print("\nVariable " + con_var + " defined across multiple constructors")
                    print("See constructor Line: " + str(con_line) + " And function constructor Line: " + str(func_line))
                    print("Solution: Use single constructor and intialise variables once in constructor") 
                    print("Risk: Low")   
                    print("Confidence: Medium\n")
        
                    report.write("\nVariable " + con_var + " defined across multiple constructors")
                    report.write("\nSee constructor Line: " + str(con_line) + " And function constructor Line: " + str(func_line))
                    report.write("\nSolution: Use single constructor and intialise variables once in constructor")
                    report.write("\nRisk: Low")  
                    report.write("\nConfidence: Medium\n")
        
                    score += 4
                    syntax += 1                   
    return score

#Check Local Variable Shadowing - Syntax Bug
''' 
This check catches if a contract contains the phenomanum of
local variable shadowing. This includes the local variable shadows
an instance variable in the outerscope based in the modifier, struct, 
function, constructor and mapping. 

Consider renaming local function variable to mitigate unintended local
variable shadowing or Consider not redefining contract local variables 
variable unless inteded to.

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_loc_var_shadow(file):
    code = enumerate(open(file))
    code_1 = enumerate(open(file))
    code_2 = enumerate(open(file))
    
    score = 0;
    global syntax
    
    varname_type = {}
    mod = "modifier"
    func = "function"
    con = "constructor"
    contract = "contract"
    struct = "struct"
    map = "mapping"
    booly = "bool"
    pub = "public"
    start_pub = "public "
    under = "_"
    search_var = False
    start = " "
    end = ";"
    equals = "="
    con_count = 0;
    
    for i, line in code:
        if(con_count > 1):
            break
        if (contract in line):
            con_count += 1
        if (contract in line):
            search_var = True
        if ((mod in line) or (func in line) or (con in line) or (struct in line)):
            search_var = False

        #Case 1 No Equals
        if ((search_var == True) and (equals not in line) and (end in line) and (map not in line) and (pub not in line) and (booly not in line)):
            sub = line[line.find(start)+len(start):line.rfind(end)]
            dtype = sub[sub.find(start)+len(start):sub.rfind(start)]            
            var = line[line.find(dtype)+len(dtype):line.rfind(end)].replace(" ", "")
            dtype = dtype.replace(" ", "")
            
            entry = {var:dtype}
            varname_type.update(entry)
        #Case 2 Equals Set    
        if ((search_var == True) and (equals in line) and (end in line) and (map not in line) and (pub not in line) and (booly not in line)):
            sub = line[line.find(start)+len(start):line.rfind(equals)]
            dtype = sub.split()[0]
            var = sub.split()[1]   
            entry = {var:dtype}
            varname_type.update(entry)
        #Case 3 Public no Equals
        if ((search_var == True) and (equals not in line) and (end in line) and (map not in line) and (pub in line) and (booly not in line)):
            sub = line[line.find(start_pub)+len(start_pub):line.rfind(end)]
            var = sub
            dtype = line[line.find(start)+len(start):line.rfind(start_pub)].replace(" ", "")
            entry = {var:dtype}
            varname_type.update(entry)
                                            
        #Case 4 Public Equals
        if ((search_var == True) and (equals in line) and (end in line) and (map not in line) and (pub in line) and (booly not in line)):
            sub = line[line.find(start_pub)+len(start_pub):line.rfind(equals)]
            var = sub  
            dtype = line[line.find(start)+len(start):line.rfind(start_pub)].replace(" ", "")
            entry = {var:dtype}
            varname_type.update(entry)

    #Now use value and data type to search for two cases
    #Case 1 Function passes same variable name from dictionary could be same or different datatype
    for i, line in code_1:
        if (func in line):
            for var, data_type in varname_type.items():
                if ((var in line) and (under not in line)):                    
                    print("\nFunction Local Shadow Bug at Line: " + str(i+1) + " has variable " + var)
                    print("this is local variable shadowing")
                    print("Solution: Consider renaming local variable to mitigate unintended variable shadowing") 
                    print("Risk: Low")   
                    print("Confidence: Medium\n")
        
                    report.write("\nFunction Local Shadow Bug at Line: " + str(i+1) + " has variable " + var)
                    report.write("\nthis is local variable shadowing")
                    report.write("\nSolution: Consider renaming local variable to mitigate unintended local variable shadowing")
                    report.write("\nRisk: Low")  
                    report.write("\nConfidence: Medium\n")
                    
                    score += 4
                    syntax += 1
                    
    start_func = False
    end_func = "}"
    end_len = 6
    doub_eq = "=="
    o_brac = "("
    c_brac = ")"
    #Case 2 Define variable in function with different or same data type but same varible name
    for i, line in code_2:
        if ((start_func == True) and (end_func in line) and (len(line) == end_len)):
            start_func = False
        if ((start_func == False) and (func in line)):
            start_func = True
        
        
        if (start_func == True):
            for var, data_type in varname_type.items():
                var = " " + var + " "
                #2A Redefine WORST
                if ((var in line) and (data_type in line) and (doub_eq not in line) and (o_brac not in line) and (c_brac not in line) and (end in line)):
                                        
                    print("\nLocal Shadow Bug at Bug detected at Line: " + str(i+1) + " has data type: " + data_type + " and variable: " + var)
                    print("this is local variable shadowing, and can redefine contract prior variables")
                    print("Solution:  Consider not redefining contract local variable unless inteded to") 
                    print("Risk: Low")   
                    print("Confidence: Medium\n")
        
                    report.write("\nLocal Shadow Bug at Bug detected at Line: " + str(i+1) + " has data type: " + data_type)
                    report.write("\nand variable: " + var + "this is local variable shadowing, and can redefine contract prior variables")
                    report.write("\nSolution: Consider not redefining contract local variable unless inteded to")
                    report.write("\nRisk: Low")  
                    report.write("\nConfidence: Medium\n")
                    
                    score += 4
                    syntax += 1
                #2B Duplicate Variable Medium bad
                if ((var in line) and (data_type not in line) and (doub_eq not in line) and (o_brac not in line) and (c_brac not in line) and (end in line)):
                                        
                    print("\nLocal Shadow Bug at Bug detected at Line: " + str(i+1) + " has variable: " + var)
                    print("this is local variable shadowing, 2 variables defined with same name but different data types")
                    print("Solution: Consider renaming local variable to mitigate unintended local variable shadowing") 
                    print("Risk: Low")   
                    print("Confidence: Medium\n")
        
                    report.write("\nLocal Shadow Bug at Bug detected at Line: " + str(i+1) + " has variable: " + var)
                    report.write("\nthis is local variable shadowing, 2 variables defined with same name but different data types")
                    report.write("\nSolution: Consider renaming local variable to mitigate unintended variable shadowing")
                    report.write("\nRisk: Low")  
                    report.write("\nConfidence: Medium\n")
                    
                    score += 4
                    syntax += 1
    return score

#Check State Variable Shadowing - Syntax Bug
''' 
This check catches if a contract contains the phenomanum of
state variable shadowing. This includes using and refdefing inherited
variables from the parent contract in the child contract

Solutions include assign Parent Contract prior to child contract. 
Define inherited parent contract variable in Constructor. Same variable 
name from parent redefined use different variable name. Parent contract 
variable never assigned, assign in parent contract to prevent

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_state_var_shadow(file):
    code = enumerate(open(file))
    code_1 = enumerate(open(file))

    score = 0;
    global syntax
    
    #Before the constructor code is executed, state variables are initialised to their 
    #specified value if you initialise them inline, or zero if you do not.
    
    contract = "contract"
    construct = "constructor"
    func = "function"
    modify = "modifier"
    pub = "public"
    eq = "="
    close = ";"
    contract_name = ""
    end_len = 2
    end_con = "}"
    start_con = "{"
    start_search = False
    in_con = False
    
    #Array House Variable Names
    var_names = np.array([])

    #Dictionary House Variables Names and weather assigned
    var_assigned = {}
    
    #Store all state variabled from first contract and get parent contract name
    for i, line in code:
        if ((modify in line) or (func in line) or ((end_con in line) and (len(line) == end_len))):
            start = False
            break
        
        if (contract in line):
            start_search = True
            contract_name = line[line.find(contract)+len(contract):line.rfind(start_con)].replace(" ", "")

        if ((eq in line) and (start_search == True) and (in_con == False)):
            #Here store var name in array and var and and assigned in dictoonary
            if (pub not in line):             
                start = " "
                end_var = ""
                first = line[line.find(start)+len(start):line.rfind(eq)]
                Dtype = first[first.find(start)+len(start):first.rfind(start)]
                Dtype = Dtype[Dtype.find(start)+len(start):Dtype.rfind(start)]

                var_name = first[first.find(Dtype)+len(Dtype):first.rfind(end_var)].replace(" ", "")
                var_names = np.append(var_names, var_name)
                
                entry = {var_name:True}
                var_assigned.update(entry)
                
            if (pub in line):
                var_name = line[line.find(pub)+len(pub):line.rfind(eq)].replace(" ", "")
                var_names = np.append(var_names, var_name) 
                
                entry = {var_name:True}
                var_assigned.update(entry)   
                
        if ((eq not in line) and (close in line) and (start_search == True) and (in_con == False)):
            #Here store var name in list
            if (pub not in line):
                start = " "
                end_var = ""
                first = line[line.find(start)+len(start):line.rfind(close)]
                Dtype = first[first.find(start)+len(start):first.rfind(start)]
                var_name = first[first.find(Dtype)+len(Dtype):first.rfind(end_var)].replace(" ", "")
                var_names = np.append(var_names, var_name)
            
            if (pub in line):
                var_name = line[line.find(pub)+len(pub):line.rfind(close)].replace(" ", "")
                var_names = np.append(var_names, var_name)
                
        if (in_con == True):
        #Loop over stored variables if that name and eq in line and not in dic then put in dic with assigned value
            for name in var_names:
                if ((name in line) and (eq in line) and (name not in var_assigned)):
                    entry = {name:True}
                    var_assigned.update(entry)
                
        if ((construct in line) and (start_search == True)):
            in_con = True

    #Loop over variable list and if not in dictionary then put in dictionary with unassgined value
    for name in var_names:
        if (name not in var_assigned):
            entry = {name:False}
            var_assigned.update(entry)
    
    #Now look over remiaining contrcats
    inherit = "is"
    current_con = False
    current_construct = False
    end_contract = False
    end = "}"
    con_len = 6;
    before_anything = False
    
    for i, line in code_1:
        
        if (((current_con == True) and (end in line) and (len(line) == con_len)) or (end_contract == True)):
            current_con = False
            before_anything = False
            end_contract = False

        if ((inherit in line) and (contract_name in line)):
            current_con = True
            
        if ((construct in line) and (before_anything == True)):
            before_anything = False
            current_construct = True
            
        if (current_construct == True):
            for name,assign in var_assigned.items():
                if ((name in line) and (assign == False)):
                    print("\nState Variable Bug Detected at Line: " + str(i+1))
                    print("Solution: Assign Parent Contract prior to child contract")
                    print("Risk: Medium")      
                    print("Confidence: Medium\n")
                
                    report.write("\nState Variable Bug Detected at Line: " + str(i+1))
                    report.write("\nSolution: Assign Parent Contract prior to child contract")
                    report.write("\nRisk: Medium")      
                    report.write("\nConfidence: Medium\n")
                    
                    score += 8
                    syntax += 1
                
        if ((func in line) or (modify in line)):
            before_anything = False
            end_contract = True
            
        if ((before_anything == True)):
            for name in var_names:
                if ((name in line) and (eq in line)):
                    print("\nState Variable Bug Detected at Line: " + str(i+1))
                    print("Solution: Define inherited parent contract variable: " + name + " in Constructor")
                    print("Risk: High")      
                    print("Confidence: Medium\n")
                
                    report.write("\nState Variable Bug Detected at Line: " + str(i+1))
                    report.write("\nSolution: Define inherited parent contract variable: " + name + " in Constructor")
                    report.write("\nRisk: High")      
                    report.write("\nConfidence: Medium\n")
                    
                    score += 12
                    syntax += 1
                    
                if ((name in line) and (eq not in line)):
                    print("\nState Variable Bug Detected at Line: " + str(i+1))
                    print("Solution: Same variable name from parent redefined use different variable name")
                    print("Risk: Medium")      
                    print("Confidence: Medium\n")
                
                    report.write("\nState Variable Bug Detected at Line: " + str(i+1))
                    report.write("\nSolution: Same variable name from parent redefined use different variable name")
                    report.write("\nRisk: Medium")      
                    report.write("\nConfidence: Medium\n")
                    
                    score += 8
                    syntax += 1
                                    
            for name,assign in var_assigned.items():
                if ((name in line) and (assign == False)):
                    print("\nState Variable Bug Detected at Line: " + str(i+1))
                    print("Solution: Parent contract variable never assigned, assign in parent contract to prevent")
                    print("unintended effect")
                    print("Risk: High")      
                    print("Confidence: Medium\n")
                
                    report.write("\nState Variable Bug Detected at Line: " + str(i+1))
                    report.write("\nSolution: Parent contract variable never assigned, assign in parent contract to prevent")
                    report.write("\nunintended effect")
                    report.write("\nRisk: High")      
                    report.write("\nConfidence: Medium\n")
                    
                    score += 12
                    syntax += 1
                                                   
        #Look through Vars before constructor, function or modifier check not from parent contract
        if ((current_con == True) and (before_anything == False) and (current_construct == False)):
            before_anything = True            
            
    return score

#Check Block Gas Limit - Syntax Bug
''' 
This check catches if a contract contains for/while loops 
which conditionuses the length of an array or object to iterate over

Avoid loop of unknown size that could grow and cause 
DoS vulnerability

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_block_gas(file):
    code = enumerate(open(file))
    bug = "length"
    loop_for = "for"
    loop_while = "while"
    score = 0
    
    #Check if for or while loop uses length for iteration process
    for i, line in code:
        if (((loop_for in line) and (bug in line)) or ((loop_while in line) and (bug in line))):
            print("\nBlock Gas Limit Bug Detected at Line: " + str(i + 1))
            print("Solution: Avoid loop of unknown size that could grow and cause DoS vulnerability")
            print("Risk: Medium")  
            print("Confidence: High\n")
            
            report.write("\nBlock Gas Limit Bug Detected at Line: " + str(i + 1))
            report.write("\nSolution: Avoid loop of unknown size that could grow and cause DoS vulnerability")
            report.write("\nRisk: Medium")  
            report.write("\nConfidence: High\n")
            
            score += 12
            global syntax
            syntax += 1
    return score
            
#Check Payable Fallback - Syntax Bug
''' 
This check catches if a contract contains an external Fallback
function for transfer of ether. Without being marked as payable
contract could through error and be inactive without this component

Mark Fallback function with payable otherwise contract 
cannot recieve ether

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_fallback(file):
    code = enumerate(open(file))
    key = "function "
    mark = "payable"
    left = 'function '
    right = '('
    score = 0
    
    #Check if fall back function is marked as payable 
    for i, line in code:
        if (key in line):
            name = line[line.index(left)+len(left):line.index(right)]
            if ((len(name) == 0) and (mark not in line)):
                print("\nPayable Fallback Bug Detected at Line: " + str(i + 1))
                print("Solution: Mark Fallback function with payable otherwise contract cannot recieve ether")
                print("Risk: Medium")  
                print("Confidence: Medium\n")

                report.write("\nPayable Fallback Bug Detected at Line: " + str(i + 1))
                report.write("\nSolution: Mark Fallback function with payable otherwise contract cannot recieve ether")
                report.write("\nRisk: Medium")  
                report.write("\nConfidence: Medium\n")
                
                score += 8
                global syntax
                syntax += 1
    return score

#Check Contract Lock - DAO Bug
''' 
This check checks wether a contract contains a lock modifier for 
reentracy attack. As well as wether conditions of require, true
condition guard for reentracy conditions by checking external calls
that are unprotected. 

Use a blockreentracy contract lock mechanism so only a single 
contract function is executed

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_contract_lock(file):
    code = enumerate(open(file))
    key = "modifier"
    end = "}"
    length = 6;
    start = False
    first = "require"
    second = "= true"
    third = "_;"
    fourth = "= false"
    pass_one = False;
    pass_two = False;
    pass_three = False;
    pass_four = False;
    safe = False
    score = 0
    mod_in_line = False;
    line_num = 0
    
    #Search for modifiers that apply the block reentracy or reentracy gaurd logic
    for i, line in code:
        if((start == True) and (end in line) and (len(line) <= length)):
            start = False
            if ((pass_one == True) and (pass_two == True) and (pass_three == True) and (pass_four == True)):
                safe = True
            if ((safe == False) and (mod_in_line == True)):            
                print("\nReentracy Bug Detected in contract at line: " + str(line_num))
                print("Solution: Use a blockreentracy contract lock mechanism so only a single contract function is executed")
                print("Risk: Medium") 
                print("Confidence: Medium\n") 
        
                report.write("\nReentracy Bug Detected in contract at line: "  + str(line_num))
                report.write("\nSolution: Use a blockreentracy contract lock mechanism so only a single contract") 
                report.write("\nfunction is executed")
                report.write("\nRisk: Medium") 
                report.write("\nConfidence: Medium\n") 
        
                score += 8
                global dao
                dao += 1
                
            pass_one = False;
            pass_two = False;
            pass_three = False;
            pass_four = False;
            mod_in_line = False;
            safe = False;
        if(key in line):
            start = True
            mod_in_line = True
            line_num = i + 1
        if ((first in line) and (pass_two == False) and (pass_three == False) and (pass_four == False) and (start == True)):
            pass_one = True
        if ((second in line) and (pass_one == True) and (pass_three == False) and (pass_four == False)and (start == True)):
            pass_two = True
        if ((third in line) and (pass_one == True) and (pass_two == True) and (pass_four == False)and (start == True)):
            pass_three = True
        if ((fourth in line) and (pass_one == True) and (pass_two == True) and (pass_three == True)and (start == True)):
            pass_four = True

    return score

        
#Check Require - DAO Bug (Withdraw)
''' 
This check checks wether a contract with the withdraw function
conducts a require verfication of amount and balance state variable
to ensure funds are not in correctly extracted by an attacker 

Condition need this to check require balance and amount first
before any operations in withdraw function

Parameters:
    file: File to analyse statically
    func_name: Withdraw function name
    state_var: Balance of funds avaliable state variable name
    with_amount_var: Amount to be deducted/transfered variable name

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_withdraw_a(file, func_name, state_var, with_amount_var):
    code = enumerate(open(file))
    bigger_equals = ">="
    less_equals = "<="
    keyword = "require"
    start = False
    start_char = "{"
    end_char = "}"
    line_var = 0;
    found = False
    score = 0
    
    #Search if balance and amount is checked using require as first port of call
    for i, line in code:
        if ((func_name in line) and (start_char in line)):
            start = True
            line_var = i + 1
            
        if ((end_char in line) and  (start_char not in line) and (found == False) and (start == True)):
            start = False
            print("\nWithdraw Function Call Bug Detected at Line: " + str(line_var))
            print("Solution: We need this to check require balance and amount first")
            print("Risk: Medium")  
            print("Confidence: Medium\n")
            
            report.write("\nWithdraw Function Call Bug Detected at Line: " + str(line_var))
            report.write("\nSolution: We need this to check require balance and amount first")
            report.write("\nRisk: Medium")  
            report.write("\nConfidence: Medium\n")
            
            score += 8
            global dao
            dao += 1
            
        if ((end_char in line) and  (start_char not in line) and (found == True)):
            start = False
            found = False;
            
        if ((keyword in line) and (state_var in line) and (with_amount_var in line) and (start == True)):
            if ((bigger_equals in line) or (less_equals in line)):
                found = True
    return score

#Check State Variable Update - DAO Bug (Withdraw)
''' 
This check checks wether a contract with the withdraw function
conducts an update to the Balance state variable prior to any 
operations such as call, send or transfer. 

Condition to Update state variable before call to 
prevent reetrancy multiple calls from attacker  

Parameters:
    file: File to analyse statically
    func_name: Withdraw function name
    state_var: Balance of funds avaliable state variable name
    with_amount_var: Amount to be deducted/transfered variable name

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_withdraw_b(file, func_name, state_var, with_amount_var):
    code = enumerate(open(file))
    found = False
    call_made = False
    subtract = "-"
    call = "call"
    send = "send"
    transfer = "transfer"
    score = 0
    
    #Check if state variable balance is updated after call/send/transfer this is a security violation
    for i, line in code:
        if(((call in line) or (send in line) or (transfer in line)) and (with_amount_var in line) and (found == False)):
            call_made = True
            print("\nWithdraw Function Call Bug Detected at Line: " + str(i +1))
            print("Solution: Update state variable balance before call")
            print("Risk: High")  
            print("Confidence: Medium\n")
            
            report.write("\nWithdraw Function Call Bug Detected at Line: " + str(i +1))
            report.write("\nSolution: Update state variable balance before call")
            report.write("\nRisk: High")  
            report.write("\nConfidence: Medium\n")
            
            score += 12
            global dao
            dao += 1
          
        if ((call_made == False) and (state_var in line) and (with_amount_var in line) and (subtract in line)):
            found = True
    return score

#Check External Call Update - DAO Bug
''' 
This check checks wether a contract that calls an external function
from another contract is marked as either trusted or untrusted. If 
untrusted this could be vulnerable to an attack invoked by the 
adversary.

Be aware that subsequent calls also inherit untrust state. 
Unknown trust, label function either trusted/untrusted

Parameters:
    file: File to analyse statically

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_external_call(file):
    code = enumerate(open(file))
    keyword = "external"
    keyword_trust = "trusted"
    keyword_un_trust = "untrusted"
    keyword_func = "function"
    start = False
    end = "}"
    score = 0
    global dao
    
    #Check if function external is either marked trusted/untrusted or called as untrusted
    for i, line in code:
        if ((keyword_func in line) and (keyword_un_trust in line)):
            print("\nUntrusted Function Bug Detected at Line: " + str(i +1))
            print("Solution: Be aware that subsequent calls also inherit untrust state")
            print("Risk: low") 
            print("Confidence: High\n")
            
            report.write("\nUntrusted Function Bug Detected at Line: " + str(i +1))
            report.write("\nSolution: Be aware that subsequent calls also inherit untrust state")
            report.write("\nRisk: low") 
            report.write("\nConfidence: High\n")
            
            score += 6
            dao += 1

        #Bad Case external call is untrusted
        if ((end in line) and (len(line) <= 2)):
            start = False
                
        if ((start == True) and (keyword_un_trust in line)):
            print("\nUntrusted Function External Call Bug Detected at Line: " + str(i +1))
            print("Solution: Be aware that subsequent calls also inherit untrust state")
            print("Risk: High") 
            print("Confidence: High\n")
            
            report.write("\nUntrusted Function External Call Bug Detected at Line: " + str(i +1))
            report.write("\nSolution: Be aware that subsequent calls also inherit untrust state")
            report.write("\nRisk: High") 
            report.write("\nConfidence: High\n")
            
            score +=18
            dao += 1

        if ((keyword_func in line) and (keyword in line)):
            start = True
        
        #Check Label
        if ((keyword_func in line) and (keyword_trust not in line) and (keyword_un_trust not in line)):
            print("\nUntrusted Function Bug Detected at Line: " + str(i +1))
            print("Solution: Unknown trust, label function either trusted/untrusted")
            print("Risk: Medium") 
            print("Confidence: High\n")
            
            report.write("\nUntrusted Function Bug Detected at Line: " + str(i +1))
            report.write("\nSolution: Unknown trust, label function either trusted/untrusted")
            report.write("\nRisk: Medium") 
            report.write("\nConfidence: High\n")
            
            score += 12
            dao += 1

    return score

#Check Checks-Effects-Interactions Pattern - DAO Bug (Withdraw)
''' 
This check checks wether a contract with the withdraw function
conducts the Checks-effects-interactions pattern when withdrawing
funds from the balance. This pattern can ensure that all prerequiestes 
before executing a the entire withdrawal. This pattern will prevent 
reclusive calls by managing the reentracy state. 

Incoporate the Check-Effect-Interacts pattern, ensure that order is
correct. Inlcuding all three components will act as a reentracy gaurd.
However if out of order, contract withdraw function could still be
vulnerable to DAO reentracy attack.  

Parameters:
    file: File to analyse statically
    func_name: Withdraw function name
    state_var: Balance of funds avaliable state variable name
    with_amount_var: Amount to be deducted/transfered variable name

Returns: 
    score: Score calculated to determine contract security rating
'''
def check_effects_interactions_pattern(file, func_name):
    code = enumerate(open(file))
    check_one = "require"
    check_two = "assert"
    new_function = "function"
    update = "="
    start = False
    end = "}"    
    inter_send = "send"
    inter_trans = "transfer"
    inter_call = "call"
    less = "<"
    big = '>'
    
    first = False
    Second = False
    third = False
    
    check_found = False
    effect_found = False
    interact_found = False
    
    single_check = False
    single_effect = False
    single_interact = False
    
    function_line = 0;
    score = 0
    global dao
    
    #Search if Check Effect Interactions is violated either in order or missing
    for i, line in code:
        #Move onto next function
        if ((end in line) and (len(line) <= 2) and (start == True)):
            #Output Phase
            #Check Missing
            if ((check_found == False) and (single_check == False)):
                print("\nCheck-Effect-Interaction Bug Detected at Line: " + str(function_line))
                print("Solution: Check is missing")
                print("Risk: High") 
                print("Confidence: Medium\n")
                
                report.write("\nCheck-Effect-Interaction Bug Detected at Line: " + str(function_line))
                report.write("\nSolution: Check is missing")
                report.write("\nRisk: High") 
                report.write("\nConfidence: Medium\n")
                
                score += 12  
                dao += 1

            #Check Order
            if (single_check == True):
                print("\nCheck-Effect-Interaction Bug Detected at Line: " + str(function_line))
                print("Solution: Check is out of order")
                print("Risk: Medium")
                print("Confidence: Medium\n")
                
                report.write("\nCheck-Effect-Interaction Bug Detected at Line: " + str(function_line))
                report.write("\nSolution: Check is out of order")
                report.write("\nRisk: Medium")
                report.write("\nConfidence: Medium\n")
                
                score += 8
                dao += 1
  
            #Effect Missing
            if ((effect_found == False) and (single_effect == False)):
                print("\nCheck-Effect-Interaction Bug Detected at Line: " + str(function_line))
                print("Solution: Effect is missing")
                print("Risk: High")  
                print("Confidence: Medium\n")
                
                report.write("\nCheck-Effect-Interaction Bug Detected at Line: " + str(function_line))
                report.write("\nSolution: Effect is missing")
                report.write("\nRisk: High")  
                report.write("\nConfidence: Medium\n")
                
                score += 12
                dao += 1
   
            #Effect Order     
            if (single_effect == True):
                print("\nCheck-Effect-Interaction Bug Detected at Line: " + str(function_line))
                print("Solution: Effect is out of order")
                print("Risk: Medium")  
                print("Confidence: Medium\n")
                
                report.write("\nCheck-Effect-Interaction Bug Detected at Line: " + str(function_line))
                report.write("\nSolution: Effect is out of order")
                report.write("\nRisk: Medium")  
                report.write("\nConfidence: Medium\n")
                
                score += 8
                dao += 1
  
            #Interact Missing
            if ((interact_found == False) and (single_interact == False)):
                print("\nCheck-Effect-Interaction Bug Detected at Line: " + str(function_line))
                print("Solution: Interact is missing")
                print("Risk: High")   
                print("Confidence: Medium\n")  
                
                report.write("\nCheck-Effect-Interaction Bug Detected at Line: " + str(function_line))
                report.write("\nSolution: Interact is missing")
                report.write("\nRisk: High")   
                report.write("\nConfidence: Medium\n")
                
                score += 12
                dao += 1
           
            #Interact Order
            if (single_interact == True):
                print("\nCheck-Effect-Interaction Bug Detected at Line: " + str(function_line))
                print("Solution: Interact is out of order")
                print("Risk: Medium")      
                print("Confidence: Medium\n")
                
                report.write("\nCheck-Effect-Interaction Bug Detected at Line: " + str(function_line))
                report.write("\nSolution: Interact is out of order")
                report.write("\nRisk: Medium")      
                report.write("\nConfidence: Medium\n")
                
                score += 8
                dao += 1
  
            #Reset Variables
            start = False
            first = False
            Second = False
            third = False
            check_found = False
            effect_found = False
            interact_found = False
            single_check = False
            single_effect = False
            single_interact = False
            function_line = 0;
        #Come accross new function
        if ((new_function in line) and (func_name in line) and (start == False)):
            start = True 
            first = True  
            function_line = i + 1

        #Check Phase
        if (((check_one in line) or (check_two in line)) and (first == True) and (single_effect == False) and (interact_found == False) and (single_interact == False)):
            check_found = True
            Second = True
        #Check Phase out of order
        if((Second == False) and (first == True) and ((check_one in line) or (check_two in line))):
            single_check = True;
        #Effect Phase
        if ((Second == True) and  (first == True) and (update in line) and (less not in line) and (big not in line)):
            effect_found = True
            third = True
        #Effect But no Check
        if ((update in line) and (less not in line) and (first == True) and (big not in line) and (Second == False) and (effect_found == False)):
            single_effect = True 
        #Interact Phase
        if (((third == True) and (start == True) and (update not in line) and  ((inter_call in line) or (inter_send in line) or (inter_trans in line)))):
            interact_found = True
        #Interact But no Check/Effect
        if (((inter_call in line) or (inter_send in line) or (inter_trans in line)) and (third == False) and (interact_found == False) and (start == True) and (update not in line)):
            single_interact = True 

    return score

#Calculate DAO Score
''' 
This calculats score for a DAO withdraw contract static
analysis. 90 is the highest and most secure and <49 would
be a very unsafe smart contract security wise  

Parameters:
    score: Points accumulated from check functions

Returns: 
    score: Score calculated as a '%' of score security rating
'''
def calc_complex_score(score):
    #Score correspond to percentage
    if (score < 10):
        return 90
    if (score < 25):
        return 80
    if (score < 50):
        return 70
    if (score < 100):
        return 60
    if (score > 100):
        return 49
    
#Calculate General Contract Score
''' 
This calculats score for a general contract static
analysis. 100 is the highest and most secure and <49 would
be a very unsafe smart contract security wise  

Parameters:
    score: Points accumulated from check functions

Returns: 
    score: Score calculated as a '%' of score security rating
'''
def calc_score(score):
    #Score correspond to percentage
    if (score < 50):
        return 100
    if (score < 100):
        return 95
    if (score < 200):
        return 90
    if (score < 300):
        return 85
    if (score < 400):
        return 80
    if (score < 500):
        return 75
    if (score < 600):
        return 70
    if (score < 700):
        return 65
    if (score < 800):
        return 60
    if (score < 900):
        return 55
    if (score < 1000):
        return 50
    if (score > 1000):
        return 49

#Call Checks General Contract
''' 
This calls and accumulates the score of a static analysis on 
a general contract  

Parameters:
    file: File to analyse statically
    score: Points accumulated from check functions

Returns: 
    score: Score calculated as a number from function checks accumulated
'''
def call_simple_checks(file, score):
    #Call all functions for standard check
    score += compiler_issue(file)
    score += check_safe_math(file) 
    score += check_type_infer(file)
    score += check_loop_condition(file)
    score += check_integer_operations(file)   
    score += check_transfer(file)
    score += check_tx_origin(file)
    score += check_function_visibility(file)
    score += check_external_call(file)
    score += check_balance_equality(file)
    score += check_block_timestamp(file)
    score += check_delegate_call(file)
    score += check_loop_function(file)
    score += check_owner_power(file)
    score += check_constructor_init(file)
    #score += check_loc_var_shadow(file)
    score += check_state_var_shadow(file)
    score += check_bytes(file)
    score += check_block_variable(file)
    score += check_block_number(file)
    score += check_block_gas(file)
    score += check_fallback(file)
    score += check_unary(file)
    score += check_div_multiply(file)
    score += check_bool_const(file)
    score += check_arr_length(file)
    score += check_init_storage_var(file)
    score += check_address_zero(file)
    score += check_map_struct_delete(file)
    score += check_assemble_shift(file)
    score += check_self_destruct(file)
    score += check_contract_lock(file)
    return score

#Call Checks DAO Withdraw Contract
''' 
This calls and accumulates the score of a static analysis on 
a DAO withdraw contract  

Parameters:
    file: File to analyse statically
    score: Points accumulated from check functions

Returns: 
    score: Score calculated as a number from function checks accumulated
'''
def check_complex_checks(file, score, func_name, state_var, with_amount_var):
    #Call all functions for withdraw DAO check
    score+=check_withdraw_a(file, func_name, state_var, with_amount_var)
    score+=check_withdraw_b(file, func_name, state_var, with_amount_var)
    score+=check_effects_interactions_pattern(file, func_name)
    return score

#Analyse DAO Withdraw
''' 
This calculates the score and generates 
output of the static analysis

Parameters:
    N/A

Returns: 
    N/A
'''
def handlephase3():
    score = 0
    filename = "Tests/" + fname.get()
    score = check_complex_checks(filename, score, withname.get(), balname.get(), amountname.get())
    print("Total Bug Points: " + str(score))
    report.write("\nTotal Bug Points: " + str(score))
    score = calc_complex_score(score)
    
    #Print or write score to file or console
    if (score < 50):
        print("DAO Bugs Detected: " + str(dao))
        report.write("\nDAO Bugs Detected: " + str(dao) + "\n" )
        
        print("Smart Contract Score: <50%")
        report.write("\nSmart Contract Score: <50% \n")

    else:
        print("DAO Bugs Detected: " + str(dao))
        report.write("\nDAO Bugs Detected: " + str(dao) + "\n" )
        
        print("Smart Contract Score: " + str(score) +"%" )
        report.write("\nSmart Contract Score: " + str(score) +"%\n" )

#Analyse Standard Contract
''' 
This calculates the score and generates 
output of the static analysis

Parameters:
    N/A

Returns: 
    N/A
'''
def handlephase2():
    global test2
    test2 = True
    sc = 0
    filename = "Tests/" + var.get()
    sc = call_simple_checks(filename, sc)
    print("Total Bug Points: " + str(sc))
    report.write("\nTotal Bug Points: " + str(sc))
    sc = calc_score(sc)

    #Print or write score to file or console
    if (sc < 50):
        print("Overflow/Underflow Bugs Detected: " + str(over_under))
        report.write("\nOverflow/Underflow Bugs Detected: " + str(over_under) + "\n" )
        
        print("Syntax Bugs Detected: " + str(syntax))
        report.write("\nSyntax Bugs Detected: " + str(syntax) + "\n" )
        
        print("DAO Bugs Detected: " + str(dao))
        report.write("\nDAO Bugs Detected: " + str(dao) + "\n" )
        
        print("Smart Contract Score: <50%")
        report.write("\nSmart Contract Score: <50% \n")

    else:
        print("Overflow/Underflow Bugs Detected: " + str(over_under))
        report.write("\nOverflow/Underflow Bugs Detected: " + str(over_under) + "\n" )
        
        print("Syntax Bugs Detected: " + str(syntax))
        report.write("\nSyntax Bugs Detected: " + str(syntax) + "\n" )
        
        print("DAO Bugs Detected: " + str(dao))
        report.write("\nDAO Bugs Detected: " + str(dao) + "\n" )
        
        print("Smart Contract Score: " + str(sc) +"%" )
        report.write("\nSmart Contract Score: " + str(sc) +"%\n" )

#Withdraw DAO UI Display
''' 
This displays the UI to interact for the
withdraw DAO static analysis

Parameters:
    N/A

Returns: 
    N/A
'''
def phase3():
    #Create UI for user input and interactions
    root1 = Tk()
    root1.geometry('500x400')
    root1.title("PySolSweep Static Analayis Tool")
    label_0 = Label(root1, text="Withdraw DAO Function Analysis",width=40,font=("bold", 14))
    label_0.place(x=50,y=53)
    label_1 = Label(root1, text="Solidity File Name",width=30,font=("bold", 10))
    label_1.place(x=50,y=130)
    entry_1 = Entry(root1, width=30)
    global fname
    fname = entry_1
    entry_1.place(x=260,y=130)
    label_2 = Label(root1, text="Withdraw Function Name",width=30,font=("bold", 10))
    label_2.place(x=40,y=180)
    entry_2 = Entry(root1, width=30)
    global withname
    withname = entry_2
    entry_2.place(x=260,y=180)
    label_4 = Label(root1, text="Balance State Variable Name",width=30,font=("bold", 10))
    label_4.place(x=40,y=230)
    entry_3 = Entry(root1, width=30)
    global balname
    balname = entry_3
    entry_3.place(x=260,y=230)
    label_5 = Label(root1, text="Variable Amount Variable Name",width=30,font=("bold", 10))
    label_5.place(x=40,y=280)
    entry_4 = Entry(root1, width=30)
    global amountname
    amountname = entry_4
    entry_4.place(x=260,y=280)
    root1.iconbitmap("Resources/img.ico")
    Button(root1, text='Start Withdraw DAO Function Analysis',width=50,bg='brown',fg='white', command=handlephase3).place(x=100,y=330)
    # it is use for display the registration form on the window
    root1.mainloop()

#Standard Contract UI Display
''' 
This displays the UI to interact for the
standard contract static analysis

Parameters:
    N/A

Returns: 
    N/A
'''
def phase2():
    #Create UI for user input and interactions
    root2 = Tk()
    root2.geometry('500x400')
    root2.title("PySolSweep Static Analayis Tool")
    label_0 = Label(root2, text="Static Analysis",width=20,font=("bold", 20))
    label_0.place(x=80,y=53)
    label_1 = Label(root2, text="Solidity File Name",width=30,font=("bold", 10))
    label_1.place(x=50,y=130)
    entry_1 = Entry(root2, width=30)
    global var
    var = entry_1
    entry_1.place(x=260,y=130)
    root2.iconbitmap("Resources/img.ico")
    Button(root2, text='Start Static Analysis',width=30,bg='brown',fg='white', command=handlephase2).place(x=140,y=280)
    # it is use for display the registration form on the window
    root2.mainloop()

#Load Screen
''' 
Loading from main to second screen

Parameters:
    N/A

Returns: 
    N/A
'''
def inter2():
    #Create UI delay for better UX
    time.sleep(1)
    root.destroy()
    phase3()

#Load Screen
''' 
Loading from main to second screen

Parameters:
    N/A

Returns: 
    N/A
'''
def inter():
    #Create UI delay for better UX
    time.sleep(1)
    root.destroy()
    phase2()

#Load Screen
''' 
Main Function which allows user to either
engage in a standard or withdraw function
static analysis tool. 

Parameters:
    N/A

Returns: 
    N/A
'''
def main():
    #Simple Checks
    score = 0;
    bigfile = "Tests/mixbugs.txt"
    #score = call_simple_checks(bigfile, score)
    root.geometry('500x400')
    root.title("PySolSweep Static Analayis Tool")
    label_0 = Label(root, text="PySolSweep Static Analayis Tool",width=28,font=("bold", 20))
    label_0.place(x=20,y=53)
    Button(root, text='Standard Analysis',width=20,bg='brown',fg='white', command=inter).place(x=180,y=150)
    Button(root, text='Withdraw DAO Function Analysis',width=30,bg='brown',fg='white', command=inter2).place(x=140,y=250)
    
    #Set Icon Image
    root.iconbitmap("Resources/img.ico")
    # it is use for display the registration form on the window

    root.mainloop()
    
    
    #Close Report
    report.close()
        
    
if __name__ == "__main__":
    main()
