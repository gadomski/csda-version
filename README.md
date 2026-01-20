# csda-version

A Github action to calculate the next [CSDA version](#csda-version) for the checked-out repository.
To use with [release-please](https://github.com/googleapis/release-please):

```yaml
  steps:
    - uses: actions/checkout@v6
    - name: CSDA Version
      id: csda-version
      uses: gadomski/csda-version
    - uses: googleapis/release-please-action@v4
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        release-type: simple
        release-as: ${{ steps.csda-version.outputs.version }}
```

> [!IMPORTANT]
> You must use `release-type` in your Github Action YAML, you cannot use [Manifest Driven](https://github.com/googleapis/release-please/blob/main/docs/manifest-releaser.md) releasing.
> This is because `release-as` is ignored for manifest-driven releases.

## CSDA version

A CSDA version is formatted like `vYY.PI.SP-X`, where:

- `YY` is the last two digits of the year,
- `PI` is the "program increment", which is like a normal calendar quarter except that PI `1` starts Oct 1
- `SP` is the sprint number
- `X` is the release number in this sprint
