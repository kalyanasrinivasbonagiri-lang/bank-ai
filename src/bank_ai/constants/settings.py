BANKING_DISCLAIMER = (
    "BankAI is a banking guidance assistant. It explains banking processes from "
    "available documents, but it cannot access live balances, transactions, or personal accounts."
)

LIMITATION_LINES = [
    "BankAI does not perform banking transactions.",
    "BankAI cannot access live account balances or personal banking data.",
    "BankAI answers only from indexed or uploaded source material when banking details are requested.",
]

SAMPLE_PROMPTS = [
    "How to deposit money?",
    "What is the process for withdrawal?",
    "How to use ATM?",
    "How to check balance?",
    "How to fill a deposit slip?",
    "What is KYC?",
]

TOPIC_ALIASES = {
    "deposit": ["deposit", "cash deposit", "money deposit", "put money in account"],
    "withdrawal": ["withdrawal", "take money", "withdraw cash"],
    "atm": ["atm", "debit machine", "cash machine"],
    "balance": ["balance check", "check money", "account balance"],
    "kyc": ["kyc", "identity verification"],
}
