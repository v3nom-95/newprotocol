// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract IdentityRegistry {
    address public owner;
    mapping(address => bytes32) private identityHashes;
    event IdentityRegistered(address indexed user, bytes32 didHash);
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

    function registerIdentity(address user, bytes32 didHash) external onlyOwner {
        require(user != address(0), "Invalid user");
        require(didHash != bytes32(0), "Invalid DID hash");
        identityHashes[user] = didHash;
        emit IdentityRegistered(user, didHash);
    }

    function getIdentity(address user) external view returns (bytes32) {
        return identityHashes[user];
    }
}
