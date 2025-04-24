import ssl
import socket
from datetime import datetime
import click

def get_cert_expiry(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expiry = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            return expiry

@click.command()
@click.argument('domains', nargs=-1)
@click.option('--days', default=14, help='Number of days to check for certificate expiration.')
@click.option('--file', type=click.Path(exists=True), help='Path to a file containing domains (one per line).')
def check_certificate(domains, days, file):
    """Check the SSL certificate expiry date for given domains."""
    if file:
        with open(file, 'r') as f:
            domains = [
                line.split('#', 1)[0].strip()  # Ignore comments after '#'
                for line in f
                if line.strip() and not line.strip().startswith('#')  # Skip empty lines and full-line comments
            ]

    domain_info = []

    for domain in domains:
        try:
            expiry_date = get_cert_expiry(domain)
            days_until_expiry = (expiry_date - datetime.now(datetime.timezone.utc)).days
            domain_info.append((domain, expiry_date, days_until_expiry))
        except Exception as e:
            print(f'Error checking certificate for {domain}: {e}')

    ok_domains = [
        (domain, expiry_date, days_left)
        for domain, expiry_date, days_left in domain_info
        if days_left > days
    ]
    expiring_domains = [
        (domain, expiry_date, days_left)
        for domain, expiry_date, days_left in domain_info
        if days_left <= days
    ]

    print("\nDomains with certificates OK:")
    for domain, expiry_date, days_left in ok_domains:
        print(f'{domain.ljust(32)}\t{expiry_date}\t{days_left} days')

    print("\nDomains with certificates nearing expiration:")
    for domain, expiry_date, days_left in expiring_domains:
        print(f'\033[91m{domain.ljust(32)}\t{expiry_date}\t{days_left} days\033[0m')  # Red text

if __name__ == '__main__':
    check_certificate()
