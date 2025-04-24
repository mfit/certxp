Check certificate expiry date

## Usage

This script checks the SSL certificate expiry date for one or more domains.

### Command-line Arguments

- `domains`: One or more domain names to check, passed as arguments.
- `--days`: (Optional) Number of days to check for certificate expiration. Defaults to 14.
- `--file`: (Optional) Path to a file containing domains (one per line). Lines starting with `#` or empty lines are ignored.

### Examples

1. Check a single domain:
   ```bash
   python check.py example.com
   ```

2. Check multiple domains:
   ```bash
   python check.py example.com anotherdomain.com
   ```

3. Check domains from a file:
   ```bash
   python check.py --file domains.example
   ```

4. Specify a custom cutoff for expiration (e.g., 30 days):
   ```bash
   python check.py example.com --days 30
   ```

5. Combine file input and custom cutoff:
   ```bash
   python check.py --file domains.example --days 30
   ```


