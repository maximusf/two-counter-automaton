# Programming Assignment (2-CA)
# by Maximus Fernandez

## AI Prompts (Claude Opus 4.6)

I chose to create a claude project over a regular chat because it provides persistent context across sessions, so I don't have to repeatedly reintroduce files. It also uses a RAG-like approach where relevant parts of files are selectively pulled in, which makes it easier to scale than loading everything into the context window. It also makes it easier to update any shared files (like abc.txt) at any time and supports running multiple parallel conversations that all reference the same underlying context.

I gave the claude project the following files:

- programming-assignment.tex (instructions for the programming assignment to make sure I didn't miss any details)
- course-notes.pdf (descriptions of most methods we learn in class to understand technical scope of project)
- ab.txt
- abc.txt (Corrected file abc.txt)
- abcd.txt
- semibalanced.txt
- match_delim1.txt
- match_delim2.txt
- equals01.txt
- txt file with the Blackboard announcements labeled "Two important FAQs" and "IMPORTANT"

I skipped the input files on purpose, and the pl script was not accepted by claude.

In my opinion, this was much more context than was necessary and probably ate through a lot more tokens as a result. However, I didn't think the amount of tokens was going to be a problem for this project.

From there, I started a new chat session and asked the following:

```
"Can you review all the files in the project"
```

It then described the programming-assignment.txt in a couple of lines about building an interpreter that reads a 2-CA description from a file, then simulates it on input strings, then printing the computation trace and ACCEPT/REJECT.

It also gave me a table describing each of the files I attached to the project

I then asked it the following:

```
"I'm planning to use python for this project, can you make a list of clear requirements in the form of a checklist 
