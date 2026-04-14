const { expect } = require("chai");

describe("QAI Registries", function () {
  it("stores and retrieves identity hash", async function () {
    const [owner, user] = await ethers.getSigners();
    const IdentityRegistry = await ethers.getContractFactory("IdentityRegistry");
    const identity = await IdentityRegistry.deploy();
    await identity.waitForDeployment();

    const didHash = "0x" + "11".repeat(32);
    await identity.registerIdentity(user.address, didHash);
    expect(await identity.getIdentity(user.address)).to.equal(didHash);
  });

  it("stores and retrieves risk score", async function () {
    const [owner, user] = await ethers.getSigners();
    const RiskRegistry = await ethers.getContractFactory("RiskRegistry");
    const risk = await RiskRegistry.deploy();
    await risk.waitForDeployment();

    await risk.storeRiskScore(user.address, 77);
    expect(await risk.getRiskScore(user.address)).to.equal(77);
  });
});
