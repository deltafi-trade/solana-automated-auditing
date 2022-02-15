# A proof of concept prototype to use pyparsing to parse common rust pitfalls

from pyparsing import *

code_example = """
let FEE: u32 = 1000; 

fn withdraw_token(program_id: &Pubkey, accounts: &[AccountInfo], amount: u32) -> ProgramResult {

    // ...
    // deserialize & validate user and vault accounts
    // ...
    
    if amount + FEE > vault.user_balance[user_id] {
        return Err(ProgramError::AttemptToWithdrawTooMuch);
    }
    
    // ...
    // Transfer `amount` many tokens from vault to user-controlled account ...
    // ...
    
    Ok(())
}
"""

variable = Word(alphas)
arith_op = oneOf("+ - * /")
equation = variable + arith_op + variable
equation.ignore(cppStyleComment)


def printInfo(s: str, loc: int, tokens: ParseResults):
    print(
        "Warning: overflow & underflow at line: %d %s"
        % (lineno(loc, s), " ".join(tokens.asList()))
    )


equation.setParseAction(printInfo)
equation.searchString(code_example)
