# plugins-release-workflow
Automates the release workflow across all components, starting with the CLI, followed by the Wrappers, and concluding with the Plugins. This streamlined process ensures consistent and efficient deployment across the entire ecosystem.

## Dispatch plugin version updates
`.github/workflows/dispatch-workflow.yml` is called, after a release is published, by the manual
"Update dependent plugins" workflow of `ast-cli`, `ast-cli-java-wrapper`, `ast-cli-javascript-wrapper`
and `ast-cli-javascript-wrapper-runtime-cli`. It:
1. runs in the caller's `release` environment, from `main` only;
2. refuses a release that is a draft, a pre-release or not immutable;
   for a Java wrapper release, waits (up to 30 minutes) until the jar is on Maven Central;
3. sends a `repository_dispatch` event (`client_payload.version` = the tag) to every consumer repo;
4. waits for the update PRs and lists them in the job summary.

| Released repo | Event | Consumers |
|---|---|---|
| ast-cli | `cli-version-update` | ast-cli-java-wrapper, ast-cli-javascript-wrapper, ast-cli-javascript-wrapper-runtime-cli, ast-github-action, ast-teamcity-plugin, ast-visual-studio-extension |
| ast-cli-javascript-wrapper | `js-wrapper-version-update` | ast-vscode-extension |
| ast-cli-javascript-wrapper-runtime-cli | `js-runtime-wrapper-version-update` | ast-azure-plugin |
| ast-cli-java-wrapper | `java-wrapper-version-update` | ast-eclipse-plugin, ast-jetbrains-plugin, ast-cli-maven-plugin |

Caller example:
```yaml
on:
  workflow_dispatch:
    inputs:
      tag:
        description: Published release tag
        required: true
permissions:
  contents: read
jobs:
  update-dependent-plugins:
    permissions:
      contents: read
      id-token: write
    uses: Checkmarx/plugins-release-workflow/.github/workflows/dispatch-workflow.yml@<commit-sha>
    with:
      tag: ${{ inputs.tag }}
```
