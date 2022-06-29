import whois

def is_registered(domain_name):
    whois_info = whois.whois(domain_name)
    return whois_info
a=is_registered("olenchuk.ru")

print(a)
