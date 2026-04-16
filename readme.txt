Programming Assignment (2-CA)
Maximus Fernandez

Discussion with other students:
None.

Use of AI:
I used Claude Opus 4.7 and Codex VS Code extension (GPT-5.4) during this project.

I used these tools for:
- reviewing the assignment requirements
- identifying grading-critical details such as output formatting, final newline behavior, and the debugging workflow
- reviewing my interpreter for parsing, simulation, and output issues
- checking whether my program's output matched the provided reference program in the instructions
- rewriting the explanation of some parts of the implementation

Sometimes I would stop and manually fix the documentation and clarity in the code.

Prompts I used (Claude Opus 4.7):
- "Read the assignment instructions in programming-assignment.tex and give me a concise checklist of everything my 2-counter automaton (2CA) must do to get full credit.  Note the professor announcements attached to the project."
- "Does this cover necessary CLI, I/O formatting, rules for simulating, greedy epsilon behavior mentioned, handling with wildcards, acceptance conditions, the 11-second time limit, and other details for grading"
- "Sounds good. Based on the loaded files, can you propose a design for a python interpreter. I want you to break it into small functions, explain what each function is responsible for, and suggest a good data structure for storing transitions (I'm assuming hashmap/dict might be the correct way). Don't start coding yet"
- "implement the parser. Note the examples in the loaded automaton files. It should be able to remove comments and whitespace, support epsilon transitions, and expand according to wildcard conditions givenf"
- "lets implement the simulator now. make sure to follow the rules provided like being able to determine counter signs, prefer non-epsilon moves over episilon when both are available, decrement counters with floor at zero, halt when there is no transition that exists, and accept only when input is empty and both counters are zero"
- "tell me exactly what my output should look like for grading, identify any formatting details that could cause a diff mismatch even if logic is correct"

Prompts I used (GPT-5.4 Codex extension):
- "Review the assignment files and summarize the interpreter requirements
- "check my_interpreter.py for missing or incorrect behavior"
- "Compare the output of the my_interpreter.py to the reference material in the instructions and note any differences that may impact my grade
- "Check if the my_interpreter.py aligns with the blackboard announcement material"
- "write some debugging code to trace the steps made by the interpreter"
- "Explain how the regex parser works again so I can double check"



