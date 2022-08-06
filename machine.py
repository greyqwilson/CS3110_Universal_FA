#Deterministic Finite State Automata Project
# Brian Kang, Jie Lin, Greyson Wilson
# 
# CS3110 Summer 2022
# Professor Young
# 
# This program is designed to simulate deterministic finite state automata, or DFA's
# A description of the machine is input via a plain text file, formatted as such:
#   Number of states    |5
#   Final states        |1 3
#   Alphabet            |a b c d
#   Transition Table    |(current_state read_symbol next_state) ie (0 a 1)
#   ...                 |...
#   Test input strings  |bad
#   ...                 |..
#   Delimiter (@)       |@
#
# Multiple machines may be simulated one after the other.
# A summary of the input strings will be printed after simulating all machines 
#   described in the file.
# 
# ******
# To Run: python machine.py
#    or   python3 machine.py
# #


FILE_NAME = 'input.txt'

def PrtFileFormatNotice():
    "Print information on file formatting"
    print("File is formatted as so:")
    print("number of states (integer, no spaces)")
    print("final states (integers, spaces between states)")
    print("alphabet (spaces between symbols)")
    print("transition function ie: (current_state symbol_read, next_state) \nOne transition per line!")
    print("test input strings (one test string per line!)")
    print("an @ delimiter to mark separations of machines")

def GetFileInput():
    try:
        file = open(FILE_NAME, mode= 'r')
        machines = []
        while True:
            machine = [] #([numStates, finalStates, alphabet, [tTable], inputStrings])

            #Read/save number of states
            line = file.readline().rstrip()
            if line == "":
                #May have reached end of file
                break
            numStates = int(line)
            machine.append(numStates)

            #Read/save final states
            finalStates = []
            #Clear whitespace
            line = file.readline().rstrip()
            #If empty string, formatting of data in file incorrect, quit
            if line == "":
                return
            #Split up the line by spaces if possible, otherwise just take the whole line
            finalSt = line.split(" ") if line.__len__() > 1 else line
            #Add them into final state and then into the first entry of the list machine
            for s in finalSt:
                finalStates.append(int(s))
            machine.append(finalStates)
            #print(finalStates)

            #Read alphabet
            line = file.readline().rstrip()
            if line == "":
                return
            alphabets = line.split(" ")
            machine.append(alphabets)

            #Read/save the entirety of the transition table
            tTable = []
            while True:
                line = file.readline().rstrip()
                if line != "" and line.startswith("("):
                    #Trim the parentheses off transition
                    line = line[1:-1]
                    tokens = line.split(" ")
                    transition = []
                    #Add to transition list one-by-one. middle entry MUST be a char/str
                    transition.append(int(tokens[0]))
                    transition.append(tokens[1])
                    transition.append(int(tokens[2]))
                    tTable.append(transition)
                else:
                    #print(tTable)
                    break
            machine.append(tTable)

            #Read/save test input strings
            testInput = []
            #error conditions?
            testInput.append(line)
            while True:
                #Have we reached the end of the file or the next machine?
                line = file.readline().rstrip()
                if line != "" and line != "@":
                    testInput.append(line)
                else:
                    #print(testInput)
                    break
            machine.append(testInput)
            machines.append(machine)
        #print(machines)
        return machines    
            
    except:
        print("Something went wrong when reading the file")
        PrtFileFormatNotice()
        return "Error reading file"
    
    finally:
        file.close()

def Accept():
    print("+++String accepted! Checking next string")
    return True

def Reject():
    print("---Rejecting string. Checking next string")
    return False

#Only too late into the project did I realize the structure could have been a dictionary, but this is fast enough
def NextState(st, sym, table, DE_CHECK=False):
    "Does O(n) search of transition table for matching transition. Return next state. DE_CHECK flag for checking moves of each string"
    for line in table:
        # if 0 == 0 and 0 == 0123456789 
        if st == line[0] and sym == line[1]:
            if DE_CHECK:
                print("Moving:", st, "-->", line[2])
            return line[2]
    #If you're seeing this line, the file is missing transitions
    print("Next state is undefined for Current State (" + str(st) + ") and Current Sym (" + str(sym) + ")")

def main():
    print("State machine processing starts!")

    state = 0
    symbol = 'a'
    machines = GetFileInput()
    allResults = []
    #Loop through all machines, enumerating them
    for mNumber, m in enumerate(machines):
        numStates = m[0]
        finStates = m[1]
        alphabet = m[2]
        transitions = m[3]
        testStrings = m[4]

        #Save machine info for printout
        machineInfo = []
        machineInfo.append("Number of states:" + str(numStates))
        machineInfo.append("Final states:" + str(finStates))
        machineInfo.append("Alphabet:" + str(alphabet) + "\nTransitions:")
        for count, t in enumerate(transitions):
            if count > 10:
                machineInfo.append("\t...")
                break
            else:
                machineInfo.append("\t" + str(t))

        results = []
        validString = True
        print("Testing machine", mNumber + 1)
        for inStr in testStrings:
            print("Now testing string", inStr)
            for sym in inStr:
                #Check in alphabet
                if sym in alphabet:
                    state = NextState(state, sym, transitions)
                    #Check dead ends
                    checkDead = False
                    for letter in alphabet:
                        if state == NextState(state, letter, transitions, DE_CHECK=False):
                            #We might be stuck in a dead end so check
                            checkDead = True
                            
                        else:
                            checkDead = False
                            break
                    #If we might be in a dead end...
                    if checkDead:
                        if state not in finStates:
                            print("Caught in dead end state")
                            validString = False
                            break

                #Not in alphabet at this point \/  \/  \/

                #if empty string, aka ^, this will no be accepted by a DFA
                elif sym == '^':
                    #We should reject
                    validString = False

                #An unknown symbol, so reject
                else:
                    validString = False
                    break

            #Make decision, end of input string
            if state in finStates and validString:
                Accept()
                results += [inStr + "   ++ Accepted"]
            
            elif not validString:
                #Already rejected, so no reject message
                Reject()
                results += [inStr + "   -- Rejected"]

            else:
                Reject()
                results += [inStr + "   -- Rejected"]

            #Reset state and valid flag
            state = 0
            validString = True
            print("")

        #Done checking test strings
        results = machineInfo + results
        allResults.append(results)

    #Print results
    for mNumber, r in enumerate(allResults):
        print("\nFinite state automaton #",mNumber + 1)
        for result in r:
            print(result)
                
main()