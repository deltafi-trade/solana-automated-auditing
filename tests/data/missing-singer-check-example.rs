fn update_admin(program_id: &Pubkey, accounts: &[AccountInfo]) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let config = ConfigAccount::unpack(next_account_info(account_iter)?)?;
    let admin = next_account_info(account_iter)?;
    let new_admin = next_account_info(account_iter)?;

    // ...
    // Validate the config account...
    // ...
    
    if admin.pubkey() != config.admin {
        return Err(ProgramError::InvalidAdminAccount);
    }
    
    config.admin = new_admin.pubkey();
    
    Ok(())
}
