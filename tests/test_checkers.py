from solaudit.checkers import missingSignerCheckChecker, overUnderFlowChecker
from solaudit.models import Program
from solaudit.parsers import getProgramParser


def test_overUnderFlowChecker():
    content = """
        fn test(a: u32, b: u32) -> u32 {
            if a + b > 0 {
                a = b;
                a += b;
            }
            return a;
        }
    """
    program = Program()
    parser = getProgramParser(program)

    parser.parseString(content)

    assert len(overUnderFlowChecker(program)) == 2


def test_missingSingerCheckChecker():
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
    program = Program()
    parser = getProgramParser(program)

    parser.parseString(content)

    assert len(missingSignerCheckChecker(program)) == 1
