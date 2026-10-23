# Security

## Secret handling

- The project reads the API key only from the `DASHSCOPE_API_KEY` process environment variable.
- Real secrets must never be written to source code, `.env.example`, documentation, tests, logs, or Git history.
- The `.env` family is ignored by Git. The script does not load `.env` files automatically.
- API authorization headers are never printed.

## If a secret is exposed

1. Revoke the exposed key in the Alibaba Cloud Model Studio console.
2. Create a replacement key and configure it as a local environment variable.
3. Remove the secret from the current files and rewrite affected Git history if it was committed.
4. Review repository, package, and CI logs for further exposure.

## Reporting

Please report security problems privately to the repository owner instead of opening a public issue
that contains credentials or personal data.
