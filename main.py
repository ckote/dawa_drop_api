# This is a sample Python script.
import base64
import requests
import json

print(base64.b64encode("1689441"))
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

    results = [f"{result.split('*')[0]}*{base64.b64decode(result.split('*')[1]).decode()}" for result in map(lambda result: result["message"], response.json()['result'])]
    for res in results:
        res_list = res.split("*")
        formatted_res = "\t".join("{:<20}".format(item) for item in res_list)
        print(formatted_res)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    get_past_appointments()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
