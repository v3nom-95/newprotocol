// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RiskRegistry {
    address public owner;
    mapping(address => uint256) private riskScores;
    event RiskScoreStored(address indexed user, uint256 score);
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

    function storeRiskScore(address user, uint256 score) external onlyOwner {
        require(user != address(0), "Invalid user");
        require(score <= 100, "Score out of range");
        riskScores[user] = score;
        emit RiskScoreStored(user, score);
    }

    function getRiskScore(address user) external view returns (uint256) {
        return riskScores[user];
    }
}
