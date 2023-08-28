import re

with open('paste.txt', 'r') as f:
    content = f.read()

parts = re.split(r'(---\n)', content)

output = ""
for i in range(0, len(parts), 2):
    question = parts[i].strip()
    answer = parts[i+1].strip()
    
    output += f"""
Prompt:
### Instruction:
Use the Task below and the Input given to write the Response, which is a programming code that can solve the Task.

### Task:
Optimize a code snippet written in Python. {question} 

### Input:
{answer}

### Response:
"""

with open('output.txt', 'w') as f:
    f.write(output)