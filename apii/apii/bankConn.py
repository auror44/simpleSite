import ssl
import requests

import json
import json
import ssl
import requests



ssl._create_default_https_context = ssl._create_unverified_context




class BankProcess():
    def __init__(self):
        self.client_id = '164579e9-848a-4496-9e64-40f94da0b5fd'
        self.client_secret = '5618de5a-76bb-4870-bbda-23ac4d16f319' # Tokens that are gathered from Portal to authenticate to API
        self.session_status=''
        self.session_info=''      
        self.available_Banks=''
        self.account_info=''
        self.device_id='3'
        self.auth_token=''
        self.session_id=''
    def create_token(self): #Create token to authenticate with API while communicating.       
        
        header = {'Content-Type':'application/x-www-form-urlencoded'}
        body = {'grant_type':'client_credentials','client_id':self.client_id, 'client_secret': self.client_secret}
        create_token = requests.post('https://sandbox.neonomics.io/auth/realms/sandbox/protocol/openid-connect/token',data=body,headers=header) #Request to generate token
        print(create_token.json().keys()) # Token info
        auth_token = create_token.json()['access_token'] #The token to use to communicate with API.
        self.auth_token=auth_token
        return auth_token
        
    def supported_banks(self,auth_token):
        supported_banks_header = {"Authorization":"Bearer "+str(auth_token),"x-device-id":"3","Accept":"application/json"}
        supported_banks_url = 'https://sandbox.neonomics.io/ics/v3/banks'
        supported_banks = requests.get(supported_banks_url,headers=supported_banks_header) #Request to fetch supported banks
        supported_banks=supported_banks.json()
        return supported_banks #Return supported banks in json format
        
    def available_banks(self,supported_banks):
        available_banks=[el for el in supported_banks if el['status']=='AVAILABLE'] #Return available banks by checking their status
        return available_banks

    def create_session(self,selected_bank,auth_token):

        session_id_header={"Authorization":"Bearer "+str(auth_token),"x-device-id":"19AA285F-75E0-4D9A-8B5C-83524AD266FE","Accept":"application/json","Content-Type":"application/json"}
        session_id_body='{"bankId":'+'"'+str(selected_bank['id'])+'"'+'}' #Starting a session with the selected bank
        session_id_json=requests.post('https://sandbox.neonomics.io/ics/v3/session',headers=session_id_header,data=session_id_body)
        self.session_info=session_id_json.json()
        session_id=str(session_id_json.json()['sessionId']) #Session id for bank
        self.session_id=session_id
        return session_id
    
    def session_status(self,auth_token,session_id):
        session_status_header={"Authorization":"Bearer "+str(auth_token),"x-device-id":"19AA285F-75E0-4D9A-8B5C-83524AD266FE","Accept":"application/json"}
        session_status=requests.get('https://sandbox.neonomics.io/ics/v3/session/'+session_id,headers=session_status_header) 
        self.session_status=session_status.json()

        
    def get_consent(self,auth_token,session_id):
        account_header={"Authorization":"Bearer "+str(auth_token),"x-device-id":"19AA285F-75E0-4D9A-8B5C-83524AD266FE","x-psu-ip-address":"","Accept":"application/json","x-session-id":session_id}
        accounts=requests.get('https://sandbox.neonomics.io/ics/v3/accounts',headers=account_header)
        print(accounts.json()) #For consent only done once

        consent_header={"Authorization":"Bearer "+str(auth_token),"x-device-id":"19AA285F-75E0-4D9A-8B5C-83524AD266FE","Accept":"application/json","x-redirect-url":"http://127.0.0.1:8000/dashboard/"}
        consent=requests.get(accounts.json()['links'][0]['href'],headers=consent_header)
        print(consent.json()['links'][0]['href'])
        return consent.json()['links'][0]['href']

    def connect_account(self,):
        
        account_header={"Authorization":"Bearer "+str(self.auth_token),"x-device-id":"19AA285F-75E0-4D9A-8B5C-83524AD266FE","x-psu-ip-address":"","Accept":"application/json","x-session-id":self.session_id}
        accounts=requests.get('https://sandbox.neonomics.io/ics/v3/accounts',headers=account_header)
        self.account_info=accounts.json()
        return accounts.json()
        

    def available_funds(self,account_info,amount): #Amount should be int.

        available_funds_header={"Authorization":"Bearer "+str(self.auth_token),"x-device-id":"19AA285F-75E0-4D9A-8B5C-83524AD266FE","x-psu-ip-address":"","Accept":"application/json","x-session-id":self.session_id,"Content-Type":"application/json"}
        
        available_funds_body={
          "account": {
            "iban": account_info[0]['iban']
          },
          "payer": "Yucel",
          "instructedAmount":{
            "amount": amount,
            "currency": "EUR"
          }
        }
        available_funds_body=json.dumps(available_funds_body)
        available_funds=requests.post('https://sandbox.neonomics.io/ics/v3/confirm-funds',headers=available_funds_header,data=available_funds_body)
        print(available_funds.json())
        return available_funds.json()

    def transfer_money(self,auth_token,session_id,account_info):
        transfer_data={
          "creditorAccount": {
            "iban": account_info[0]['iban']
          },
          "debtorAccount": {
            "iban": "DE44700222005102606851"
          },
          "debtorName": "Juan carlos",
          "creditorName": "Yucel",
          "remittanceInformationUnstructured": "My test payment",
          "instrumentedAmount": "100",
          "currency": "EUR",
          "remittanceInformationStructured": {
            "reference": "CO1235445HG56",
            "referenceType": "KID",
            "referenceIssuer": "Authority issuing the reference provided by the creditor"
          },
          "endToEndIdentification": "example-123456789-id",
          "paymentMetadata": {
            "creditorAddress": {
              "streetName": "Potetveien",
              "buildingNumber": "15",
              "postalCode": "0150",
              "city": "oslo",
              "country": "Norway"
            },
            "creditorAgent": {
              "identification": ['bic'],
              "identificationType": "BIC"
            },
            "paymentContextCode": "EPAY",
            "merchantCategoryCode": "5698",
            "merchantCustomerIdentification": "MDIwMGMwNTMtYmU3My00YzY1LWFhMWEtNjQyZDNkZjFlZjA5"
          }
        }
        transfer_data=json.dumps(transfer_data)
        print(transfer_data)
        transfer_header={"Authorization":"Bearer "+str(auth_token),"x-device-id":"19AA285F-75E0-4D9A-8B5C-83524AD266FE","x-psu-ip-address":"","Accept":"application/json","x-session-id":session_id,"Content-Type":"application/json","x-redirect-url":"http://my.redirect.com/callback"}
        transfer=requests.post('https://sandbox.neonomics.io/ics/v3/payments/sepa-credit',headers=transfer_header,data=transfer_data)

        print(transfer.json())
    
    def start(self):
        api_token = self.create_token()
        supported_banks=self.supported_banks(api_token)
        available_banks=self.available_banks(supported_banks) #Available banks
        selected_bank=available_banks[0]
        session_id=self.create_session(selected_bank,api_token)
        self.get_consent(api_token,session_id)
        account=self.connect_account(api_token,session_id)
        self.available_funds(api_token,session_id,account,100)
        #self.transfer_money(api_token,session_id,account)


