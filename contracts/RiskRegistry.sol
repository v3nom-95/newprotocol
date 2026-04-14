// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RiskRegistry {
    mapping(address => uint256) private riskScores;
    event RiskScoreStored(address indexed user, uint256 score);

    function storeRiskScore(address user, uint256 score) external {
        require(user != address(0), "Invalid user");
        require(score <= 100, "Score out of range");
        riskScores[user] = score;
        emit RiskScoreStored(user, score);
    }

    function getRiskScore(address user) external view returns (uint256) {
        return riskScores[user];
    }
}
