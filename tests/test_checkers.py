from solaudit.checkers import *
from solaudit.models import Program
from solaudit.parsers import getProgramParser, comment


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

        parser.ignore(comment)
        parser.parseString(content)

        assert len(missing_rent_exempt_checker(program)) == 1

    def test_arbitrary_signed_program_invocation_checker(self, program, parser):
        content = """
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
        """

        parser.ignore(comment)
        parser.parseString(content)

        assert len(arbitrary_signed_program_invocation_checker(program)) == 1
