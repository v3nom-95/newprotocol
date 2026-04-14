// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract IdentityRegistry {
    mapping(address => bytes32) private identityHashes;
    event IdentityRegistered(address indexed user, bytes32 didHash);

    function registerIdentity(address user, bytes32 didHash) external {
        require(user != address(0), "Invalid user");
        require(didHash != bytes32(0), "Invalid DID hash");
        identityHashes[user] = didHash;
        emit IdentityRegistered(user, didHash);
    }

    function getIdentity(address user) external view returns (bytes32) {
        return identityHashes[user];
    }
}
