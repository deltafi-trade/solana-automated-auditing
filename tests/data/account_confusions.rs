 // ------- Account Types -------- 
pub struct Config {
    pub admin: Pubkey,
    pub fee: u64,
}
 
pub struct User {
    pub user_authority: Pubkey,
    pub balance: u64,
}

pub struct Info {
    pub state: u8,
    pub balance: u64,
}