import os


HOSTS_FILE_PATH = '/etc/hosts'

def spell_url(url: str):
    if url.startswith('http://'):
        return url[7:]
    elif url.startswith('https://'):
        return url[8:]
    elif not url.startswith('www.'):
        return f'www.{url}'
    else:
        return url


def deny_access_to_site(url: str):
    url = spell_url(url)

    with open(HOSTS_FILE_PATH, 'a') as f:
        f.write(f'127.0.0.1 {url}')

    return True

def allow_access_to_site(url: str):
    content_to_save = []

    url = spell_url(url)

    with open(HOSTS_FILE_PATH, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if url in line:
                lines.remove(line)
                break
        content_to_save = lines

    with open(HOSTS_FILE_PATH, 'w') as f:
        f.writelines(content_to_save)

    return True