# A proof of concept prototype to use pyparsing to parse common rust pitfalls

from optparse import OptionParser
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


def overUnderFlowCheck(content: str):
    variable = Word(alphas)
    arith_op = oneOf("+ - * /")
    equation = variable + arith_op + variable
    equation.ignore(cppStyleComment)

    def printInfo(s: str, loc: int, tokens: ParseResults):
        print(
            "Warning: overflow & underflow at line: %d %s"
            % (lineno(loc, s), line(loc, s))
        )

    equation.setParseAction(printInfo)
    equation.searchString(content)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", dest="filename", default="")
    (options, _) = parser.parse_args()

    with open(options.filename, "r") as f:
        content = f.read()
        overUnderFlowCheck(content)
