import requests
import hashlib

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check API and try again')
    return res.text


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main():
    try:
        with open('passwords.txt', 'r') as stuff:
            passwords = stuff.read().splitlines()
    except FileNotFoundError:
        print("Error: passwords.txt file not found")
        return

    for password in passwords:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times. Change your password you Ammonite')
        else:
            print(f'{password} was not found. Good job!')

    print('All passwords checked.')


if __name__ == '__main__':
    main()
