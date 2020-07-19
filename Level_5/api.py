import urllib3
import requests
import json


def getCipher(ptext):
    api_url = "https://172.27.26.181:9999/eaeae"
    password = "23da0cb6084f4f1cc0ad8c07e4a2216c"
    teamname = "TrojanHorse"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    d1 = {"password": password, "teamname": teamname, "plaintext": ptext}
    try:
        x = requests.post(url=api_url, data=json.dumps(d1), verify=False)
        return x.json()['ciphertext']
    except Exception as e:
        print('Error is', e)
        return 0


def main():
    plaintext = 'ffgghhii'
    cip = getCipher(plaintext)
    print(cip)


if __name__ == '__main__':
    main()
