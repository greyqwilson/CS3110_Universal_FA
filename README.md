# CS3110_Universal_FA
A universal finite automaton that processes file-input descriptions of deterministic finite state automata.
 Brian Kang, Jie Lin, Greyson Wilson
 
 CS3110 Summer 2022
 Professor Young
 
 This program is designed to simulate deterministic finite state automata, or DFA's
 A description of the machine is input via a plain text file, formatted as such:
   Number of states    |5
   Final states        |1 3
   Alphabet            |a b c d
   Transition Table    |(current_state read_symbol next_state) ie (0 a 1)
   ...                 |...
   Test input strings  |bad
   ...                 |..
   Delimiter (@)       |@

 Multiple machines may be simulated one after the other.
 A summary of the input strings will be printed after simulating all machines 
   described in the file.
 
 ******
 To Run: python machine.py
    or   python3 machine.py
