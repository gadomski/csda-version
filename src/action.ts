import * as core from "@actions/core";
import { Manifest, GitHub } from "release-please";
import { registerCsdaReleaseStrategy } from "./csda-release-strategy.js";

async function main(): Promise<void> {
  await registerCsdaReleaseStrategy();

  const token = core.getInput("token", { required: true });
  const configFile = core.getInput("config-file");
  const manifestFile = core.getInput("manifest-file");
  const [owner, repo] = (process.env.GITHUB_REPOSITORY || "").split("/");

  const gh = await GitHub.create({ owner, repo, token });

  const manifest = await Manifest.fromManifest(
    gh,
    gh.repository.defaultBranch,
    configFile,
    manifestFile,
  );

  const prs = (await manifest.createPullRequests()).filter((pr) => pr);
  core.setOutput("prs_created", prs.length > 0);
  if (prs.length) {
    core.setOutput("pr", JSON.stringify(prs.map((pr) => pr!.number)));
  }
}

main().catch((err) => {
  core.setFailed(`release-please failed: ${err.message}`);
});
