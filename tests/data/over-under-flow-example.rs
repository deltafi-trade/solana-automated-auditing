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