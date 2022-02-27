pub fn process_withdraw(program_id: &Pubkey, accounts: &[AccountInfo], amount: u64) -> ProgramResult {
    let account_info_iter = &mut accounts.iter();
    let vault = next_account_info(account_info_iter)?;
    let vault_authority = next_account_info(account_info_iter)?;
    let destination = next_account_info(account_info_iter)?;
    let token_program = next_account_info(account_info_iter)?;

    // ...
    // get signer seeds, validate account owners and signers, 
    // and verify that the user can withdraw the supplied amount
    // ...

    // verify that token_program is in fact the official spl token program
    // if token_program.key != &spl_token::id() {
    //     return Err(ProgramError::InvalidTokenProgram);
    // }    

    invoke_signed(
        &spl_token::instruction::transfer(
            &token_program.key,
            &vault.key,
            &destination.key,
            &vault_authority.key,
            &[&vault_authority.key],
            amount,
        )?,
        &[
            vault.clone(),
            destination.clone(),
            vault_owner_info.clone(),
            token_program.clone(),
        ],
        &[&seeds],
    )?;


    Ok(())
}
