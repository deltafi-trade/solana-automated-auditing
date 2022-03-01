from solaudit.checkers import *


class TestCheckers:
    def test_overUnderFlowChecker(self, program, parser):
        content = """
            fn test(a: u32, b: u32) -> u32 {
                if a + b > 0 {
                    a = b;
                    a += b;
                }
                return a;
            }
        """
        parser.parseString(content)
        assert len(overUnderFlowChecker(program)) == 2

    def test_missingSingerCheckChecker(self, program, parser):
        content = """
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

                // check that the current admin has signed this operation
                // if !admin.is_signer {
                //     return Err(ProgramError::MissingSigner);
                // }
                
                config.admin = new_admin.pubkey();
                
                Ok(())
            }
        """
        parser.parseString(content)
        assert len(missingSignerCheckChecker(program)) == 1

    def test_accountConfusionsChecker(self, program, parser):
        content = """
            pub struct Config {
                pub admin: Pubkey,
                pub fee: u64,
            }
            
            pub struct User {
                pub userauthority: Pubkey,
                pub balance: u64,
            }
            pub struct Info {
                pub state: u8,
                pub balance: u64,
            }
        """
        parser.parseString(content)

        assert len(account_confusions_checker(program)) == 2

    def test_missing_rent_exempt_checker(self, program, parser):
        content = """
                fn initialize(program_id: &Pubkey, accounts: &[AccountInfo]) -> ProgramResult {

                    let escrow_account = next_account_info(account_info_iter)?;
                    let rent = &Rent::from_account_info(next_account_info(account_info_iter)?)?;
                //    if !rent.is_exempt(escrow_account.lamports(), escrow_account.data_len()) {
                //        return Err(EscrowError::NotRentExempt.into());
                //    }
                    Ok(())
                }
        """
        parser.parseString(content)

        assert len(missing_rent_exempt_checker(program)) == 1

    def test_missing_ownership_checker(self, program, parser):
        content = """
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

                let mut token_swap = SwapInfo::unpack(&swap_info.data.borrow())?;
                // Do some token swap

                
                Ok(())
            }
        """
        parser.parseString(content)

        assert len(missing_ownership_checker(program)) == 2
