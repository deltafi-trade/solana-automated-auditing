# deltafi-audit-tool

A simple solana semantic parsing and detaction tool 

### How to add a new cases

+ Add handle function in to store information needed in `models.py`
+ Associate the handle function with a parser in `parser.py`
+ Add a checker to implement check logic using newly added information in `models.py` 

