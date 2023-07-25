# This is a sample Python script.
import base64
import requests
import json


def sendSms():
    url = "https://sms-service.kenyahmis.org/api/sender"
    payload = json.dumps({
        "destination": "0718222605",
        "msg": "Dear Physhamern huyu ntu",
        "sender_id": "0718222605",
        "gateway": "40149"
    })
    headers = {
        'Accept': 'application/json',
        'api-token': 'cWMu5tZWjZdIcJEPbrK5hUhcBwdWtVKDEWRER24SKM9343I',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    print(response.json())


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def get_past_appointments():
    url = "https://ushauriapi.kenyahmis.org/past_appointments/"

    payload = json.dumps({
        "phone_no": "0712311264"  # "0718373569" # 0712311264
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
        # if not res_list[4] == 'Re-Fill' and not index == 0:
        # if not "1234500001".lower() in res_list[1].lower() and not index == 0:
        # continue
        formatted_res = "\t|\t".join("{:<21}".format(item) for item in res_list)
        # print(formatted_res)

        data = requests.post(
            "https://ushauriapi.kenyahmis.org/api/edit_appointment/get/client/apps",
            json={
                "clinic_number": res_list[1],
                "phone_no": "0712311264"
            }
        ).json()
        if data["success"]:
            for i, res1 in enumerate(data["arr_data"]):
                # if i == 0:
                # print("".join(list(res1.keys())))
                print(res_list[1],[str(key) for key in res1.keys()])
                print(res_list[3], [str(value) for value in res1.values()])
                print("-"   * 200)
                # f = "\t|\t".join("{:<21}".format(item) for item in res.values())

            # print("\n", data["arr_data"])
            # print(f)
        # else:
        #     print("\r", index, "...", end="")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    get_past_appointments()
    # sendSms()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
