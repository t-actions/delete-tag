# Delete Tag Actions

Github Actions to delete tag as well as release

## Usage

```yaml
- uses: t-actions/delete-tag@master
  with:
    # Tag name (Required)
    tag: ''

    # Github token for related repository
    # Default: ${{ github.token }}
    token: ''

    # Only delete the tag and keep the release if it is not empty
    # Default is empty
    keep_release: ''

    # Ingore error when deleting tag if it is not empty (404 won't be treated as error)
    # Default is empty
    ignore_error: ''
```
