fn initialize(program_id: &Pubkey, accounts: &[AccountInfo]) -> ProgramResult {

    let escrow_account = next_account_info(account_info_iter)?;
    let rent = &Rent::from_account_info(next_account_info(account_info_iter)?)?;

    // Solana accounts holding an Account, Mint, or Multisig must contain enough SOL
    // to be considered rent exempt. Otherwise the accounts may fail to load.

    // if !rent.is_exempt(escrow_account.lamports(), escrow_account.data_len()) {
    //     return Err(EscrowError::NotRentExempt.into());
    // }

    Ok(())
}
