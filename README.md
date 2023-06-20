# Dawa Drop

### Features
- `User Registration`: Create a user registration process that 
requires the user to provide their personal information, including 
name, phone number, address, and their HIV clinic's name and
location.

- `Prescription Verification`: Connect the app to KenyaEMR to verify 
that the user has an active prescription for ARVs from their clinic.

- `ARV Request`: Allow the user to request ARV delivery by selecting 
the desired delivery frequency (e.g., monthly, every three months)
, delivery date, and preferred delivery time.

- `Dispatch Management`: Notify the HIV clinic manager of the user's 
ARV request and provide them with the delivery details. The clinic
manager can then dispatch the ARVs to the user's address using a 
courier service.

- `Delivery Tracking`: Allow the user to track the delivery of their
ARVs in real-time to ensure timely delivery.

- `Feedback System`: Implement a feedback system to allow users to 
rate the courier service and provide feedback on their experience.

- `Security`: Ensure the app is secure and meets HIPAA compliance 
standards to protect the user's personal health information.

- `Optional Features`: Provide additional features such as appointment
scheduling, medication reminders, and resources for HIV education 
and support.

```json
{
    "MESSAGE_HEADER": {
        "SENDING_APPLICATION": "KENYAEMR",
        "SENDING_FACILITY": "12438",
        "RECEIVING_APPLICATION": "IL",
        "RECEIVING_FACILITY": "12438",
        "MESSAGE_DATETIME": "20230412082230",
        "SECURITY": "",
        "MESSAGE_TYPE": "ADT^A04",
        "PROCESSING_ID": "P"
    },
    "PATIENT_IDENTIFICATION": {
        "EXTERNAL_PATIENT_ID": {
            "ID": "",
            "IDENTIFIER_TYPE": "GODS_NUMBER",
            "ASSIGNING_AUTHORITY": "MPI"
        },
        "INTERNAL_PATIENT_ID": [
            {
                "ID": "0983678912",
                "IDENTIFIER_TYPE": "CCC_NUMBER",
                "ASSIGNING_AUTHORITY": "CCC"
            }
        ],
        "PATIENT_NAME": {
            "FIRST_NAME": "USHAURI",
            "MIDDLE_NAME": "TEST",
            "LAST_NAME": "TEST"
        },
        "MOTHER_NAME": {
            "FIRST_NAME": "",
            "MIDDLE_NAME": "",
            "LAST_NAME": ""
        },
        "DATE_OF_BIRTH": "19790615",
        "SEX": "M",
        "PATIENT_ADDRESS": {
            "PHYSICAL_ADDRESS": {
                "VILLAGE": "TEST",
                "WARD": "",
                "SUB_COUNTY": "ISUKHA WEST",
                "COUNTY": "KAKAMEGA",
                "GPS_LOCATION": "",
                "NEAREST_LANDMARK": ""
            },
            "POSTAL_ADDRESS": ""
        },
        "PHONE_NUMBER": "0788890377",
        "MARITAL_STATUS": "",
        "DEATH_DATE": "",
        "DEATH_INDICATOR": "",
        "DATE_OF_BIRTH_PRECISION": "ESTIMATED"
    },
    "NEXT_OF_KIN": [
        {
            "NOK_NAME": {
                "FIRST_NAME": "",
                "MIDDLE_NAME": "",
                "LAST_NAME": ""
            },
            "RELATIONSHIP": "",
            "ADDRESS": "",
            "PHONE_NUMBER": "",
            "SEX": "",
            "DATE_OF_BIRTH": "",
            "CONTACT_ROLE": ""
        }
    ],
    "PATIENT_VISIT": {
        "VISIT_DATE": "20230412",
        "PATIENT_SOURCE": "VCT",
        "HIV_CARE_ENROLLMENT_DATE": "20230412",
        "PATIENT_TYPE": "ART"
    },
    "OBSERVATION_RESULT": [
        {
            "UNITS": "",
            "VALUE_TYPE": "NM",
            "OBSERVATION_VALUE": "1",
            "OBSERVATION_DATETIME": "20230412",
            "CODING_SYSTEM": "",
            "ABNORMAL_FLAGS": "N",
            "OBSERVATION_RESULT_STATUS": "F",
            "SET_ID": "",
            "OBSERVATION_IDENTIFIER": "WHO_STAGE"
        }
    ]
}
```