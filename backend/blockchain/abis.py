IDENTITY_REGISTRY_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}, {"internalType": "bytes32", "name": "didHash", "type": "bytes32"}],
        "name": "registerIdentity",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]

TRANSACTION_REGISTRY_ABI = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "txHash", "type": "bytes32"},
            {"internalType": "bytes", "name": "pqSignature", "type": "bytes"},
            {"internalType": "bytes32", "name": "metadataHash", "type": "bytes32"},
        ],
        "name": "storeTransaction",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]

RISK_REGISTRY_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}, {"internalType": "uint256", "name": "score", "type": "uint256"}],
        "name": "storeRiskScore",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]
