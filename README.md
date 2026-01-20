# csda-release-please

A Github action to use [release-please](https://github.com/googleapis/release-please) with CSDA-specific versioning.
To use:

```yaml
- name: CSDA Release Please
  uses: gadomski/csda-release-please
  with:
    versioning-strategy: csda
```
