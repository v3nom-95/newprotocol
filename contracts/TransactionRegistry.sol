// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TransactionRegistry {
    address public owner;
    struct TransactionMeta {
        bytes pqSignature;
        bytes32 metadataHash;
        uint256 timestamp;
    }

    mapping(bytes32 => TransactionMeta) private txStore;
    event TransactionStored(bytes32 indexed txHash, bytes pqSignature, bytes32 metadataHash);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Invalid owner");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }

    function storeTransaction(bytes32 txHash, bytes calldata pqSignature, bytes32 metadataHash) external onlyOwner {
        require(txHash != bytes32(0), "Invalid tx hash");
        require(metadataHash != bytes32(0), "Invalid metadata hash");
        txStore[txHash] = TransactionMeta({
            pqSignature: pqSignature,
            metadataHash: metadataHash,
            timestamp: block.timestamp
        });
        emit TransactionStored(txHash, pqSignature, metadataHash);
    }

    function getTransaction(bytes32 txHash) external view returns (TransactionMeta memory) {
        return txStore[txHash];
    }
}
