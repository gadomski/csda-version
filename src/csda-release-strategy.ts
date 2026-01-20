import { registerVersioningStrategy } from "release-please";
import { Version } from "release-please/build/src/version.js";
import type {
  VersioningStrategy,
  VersionUpdater,
} from "release-please/build/src/versioning-strategy.js";
import type { ConventionalCommit } from "release-please/build/src/commit.js";

const DEFAULT_VERSION_URL =
  "https://raw.githubusercontent.com/gadomski/csda-release-please/refs/heads/main/version.txt";

export interface CsdaReleaseStrategyOptions {
  baseVersion: string;
}

export class CsdaVersionUpdate implements VersionUpdater {
  private baseVersion: Version;

  constructor(baseVersion: string) {
    this.baseVersion = Version.parse(baseVersion);
  }

  bump(version: Version): Version {
    if (
      version.major === this.baseVersion.major &&
      version.minor === this.baseVersion.minor &&
      version.patch === this.baseVersion.patch &&
      version.preRelease !== undefined
    ) {
      const preReleaseNum = parseInt(version.preRelease, 10);
      if (!isNaN(preReleaseNum)) {
        return new Version(
          this.baseVersion.major,
          this.baseVersion.minor,
          this.baseVersion.patch,
          String(preReleaseNum + 1),
        );
      }
    }

    return new Version(
      this.baseVersion.major,
      this.baseVersion.minor,
      this.baseVersion.patch,
      "0",
    );
  }
}

export class CsdaReleaseStrategy implements VersioningStrategy {
  private baseVersion: string;

  constructor(options: CsdaReleaseStrategyOptions) {
    this.baseVersion = options.baseVersion;
  }

  determineReleaseType(
    _version: Version,
    _commits: ConventionalCommit[],
  ): VersionUpdater {
    return new CsdaVersionUpdate(this.baseVersion);
  }

  bump(version: Version, commits: ConventionalCommit[]): Version {
    return this.determineReleaseType(version, commits).bump(version);
  }
}

export async function registerCsdaReleaseStrategy(
  name: string = "csda",
  versionUrl: string = DEFAULT_VERSION_URL,
): Promise<void> {
  const response = await fetch(versionUrl);
  if (!response.ok) {
    throw new Error(
      `Failed to fetch version from ${versionUrl}: ${response.status}`,
    );
  }
  const baseVersion = (await response.text()).trim();

  registerVersioningStrategy(
    name,
    () => new CsdaReleaseStrategy({ baseVersion }),
  );
}
