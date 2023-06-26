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


#### User Overview
- `A User` in OpenMRS is an account that a person may use to log into the system.Similar to User model in d-drop
- `Person` Every individual who is referred to in a patient record in OpenMRS is stored in the system as a Person. 
These include Patients, any patient relative or caretaker, Providers, and Users..
- `Link` maps a person to user
- The real-life person is represented by a Person record in OpenMRS, and a person may have more than one user account. 
If you want a patient to be able to view her record in OpenMRS, then you need to create a
user account and link it to the patient's person record.
