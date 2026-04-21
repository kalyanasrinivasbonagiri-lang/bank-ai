ROUTE_DESCRIPTIONS = {
    "general": "Casual or non-domain chat without retrieval.",
    "rag": "Banking guidance questions grounded in local banking documents.",
    "upload": "Questions that depend on uploaded files or OCR results.",
    "summarize": "Summary of retrieved or uploaded content.",
    "follow_up": "Short context-dependent follow-up question.",
}

ROUTE_KEYWORDS = {
    "rag": [
        "deposit",
        "withdraw",
        "atm",
        "balance",
        "kyc",
        "form",
        "slip",
        "documents",
        "required",
        "guideline",
        "rule",
        "process",
        "procedure",
    ],
    "upload": ["upload", "file", "pdf", "image", "document", "scan"],
    "summarize": ["summarize", "summary", "brief"],
    "follow_up": ["this", "that", "it", "also", "what about", "and then"],
}
