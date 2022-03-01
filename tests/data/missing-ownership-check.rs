fn withdraw_token_restricted(program_id: &Pubkey, accounts: &[AccountInfo], amount: u64) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let vault = next_account_info(account_iter)?;
    let admin = next_account_info(account_iter)?;
    let config = ConfigAccount::unpack(next_account_info(account_iter)?)?;
    let vault_authority = next_account_info(account_iter)?;
    
    
    if config.admin != admin.pubkey() {
        return Err(ProgramError::InvalidAdminAccount);
    }

    // if config.owner != program_id {
    //     return Err(ProgramError::InvalidConfigAccount);
    // }
    
    // ...
    // Transfer funds from vault to admin using vault_authority
    // ...
    
    Ok(())
}