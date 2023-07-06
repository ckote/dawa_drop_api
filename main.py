# This is a sample Python script.
import base64
import requests
import json


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def get_past_appointments():
    url = "https://ushauriapi.kenyahmis.org/past_appointments/"

    payload = json.dumps({
        "phone_no": "0712311264"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    header = [
        "APP*UPN*New appointment Date*Appointment Type*Appointment Other*Appointment Kept*Old appointment Id*On DCM"
    ]
    body = [
        f"{result.split('*')[0]}*{base64.b64decode(result.split('*')[1]).decode()}"
        for result in
        map(
            lambda result: result["message"], response.json()['result']
        )
    ]
    results = header + body
    print('-' * 20 * 12)
    for index, res in enumerate(results):
        res_list = res.split("*")
        if index == 1:
            print('-' * 20 * 12)
        if not res_list[4] == 'Re-Fill' and not index == 0:
            continue
        formatted_res = "\t|\t".join("{:<21}".format(item) for item in res_list)
        print(formatted_res)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    get_past_appointments()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
