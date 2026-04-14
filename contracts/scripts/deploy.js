async function main() {
  const IdentityRegistry = await ethers.getContractFactory("IdentityRegistry");
  const TransactionRegistry = await ethers.getContractFactory("TransactionRegistry");
  const RiskRegistry = await ethers.getContractFactory("RiskRegistry");

  const identity = await IdentityRegistry.deploy();
  await identity.waitForDeployment();

  const transaction = await TransactionRegistry.deploy();
  await transaction.waitForDeployment();

  const risk = await RiskRegistry.deploy();
  await risk.waitForDeployment();

  console.log("IdentityRegistry:", await identity.getAddress());
  console.log("TransactionRegistry:", await transaction.getAddress());
  console.log("RiskRegistry:", await risk.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
