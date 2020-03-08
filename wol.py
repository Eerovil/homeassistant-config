import requests
import json


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Scanner")
    parser.add_argument("--mac", help="Mac", required=True)
    parser.add_argument("--ip", help="IP", required=True)
    parser.add_argument("--router", help="router hostname", required=True)
    parser.add_argument("--password", help="", required=True)

    args = vars(parser.parse_args())

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Sec-Fetch-Dest': 'empty',
        'X-Requested-With': 'XMLHttpRequest',
        'If-Modified-Since': '0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        'DNT': '1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Origin': '{router}'.format(router=args.get('router')),
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': '{router}/'.format(router=args.get('router')),
        'Accept-Language': 'en-US,en;q=0.9,fi;q=0.8',
        'Cookie': 'Session=0; Authentication=YWRtaW46TTA1YXJ0',
    }

    resp = requests.get(
        '{router}/getCustomizationData'.format(router=args.get('router')),
        headers=headers,
        verify=False
    )
    resp = requests.get(
        '{router}/getWebGuiFlag'.format(router=args.get('router')),
        headers=headers,
        verify=False
    )
    resp = requests.get(
        '{router}/init'.format(router=args.get('router')),
        headers=headers,
        verify=False
    )
    
    
    print('{router}/UserLoginCheck?action=check'.format(router=args.get('router')))

    resp = requests.put(
        '{router}/UserLoginCheck?action=check'.format(router=args.get('router')),
        headers=headers,
        data=json.dumps({
            "Input_Account": "admin",
            "Input_Passwd": args.get('password')
        }),
        verify=False
    )
    print(resp.content)
    resp = requests.put(
        '{router}/UserLoginCheck?action=add_login_entry'.format(router=args.get('router')),
        headers=headers,
        data=json.dumps({
            "Input_Account": "admin",
            "Input_Passwd": args.get('password')
        }),
        verify=False
    )
    print(resp.content)
    session_key = resp.json()[0]['sessionId']
    print('session key: {}'.format(session_key))

    resp = requests.put(
        '{router}/cgi-bin/Home_Networking?action=WOLCommand&sessionkey={session}'.format(
            router=args.get('router'), session=session_key
        ),
        headers=headers,
        data=json.dumps({
            "MAC": args.get('mac'),
            "IP": args.get('ip')
        }),
        verify=False
    )
    print(resp.content)


