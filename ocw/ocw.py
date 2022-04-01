import requests, json
from requests.exceptions import HTTPError

class ocw(object):
    '''This is a class that wraps the Online Checkwriter API'''
    __url = None

    def __init__(self,url,header):
        self.__url = url
        self.__header = header

    ###Bank Accounts
    def get_bank_accounts(self):
        '''This returns the bank accounts defined in online checkwriter
        It takes no parameters and we use it to test our connection
        returns a success value, either True or False, and a list of dicts with
        the current bankaccountIds
        '''
        u = f'{self.__url}/bankAccounts?perPage&page&term'
        payload = {}
        try:
            response = requests.request("GET", u, headers=self.__header, data=payload)
            response.raise_for_status()
            r = response.json()
            ba = r['data']['bankAccounts']
            return ba
        except HTTPError as e:
            d = response.json()
            return f'{e.response.status_code}',d["errorMsg"]
    
    ###Payees
    def get_payees(self,page='1'):
        if page == '1':
            u = f'{self.__url}/payees?perPage=1000'
        else:
            u = f'{self.__url}/payees?perPage=1000&page={page}'
        payload = {}
        try:
            response = requests.request("GET", u, headers=self.__header, data=payload)
            response.raise_for_status()
            r = response.json()
            p = r['data']
            return p
        except HTTPError as e:
            d = response.json()
            return f'{e.response.status_code}',d["errorMsg"]

    def get_payee_by_id(self,payeeId):
        u = f'{self.__url}/payees/{payeeId}'
        payload = {}
        try:
            response = requests.request("GET", u, headers=self.__header, data=payload)
            response.raise_for_status()
            return response.text
        except HTTPError as e:
            d = response.json()
            return f'{e.response.status_code}',d["errorMsg"]

    def create_payees(self,payee_data):
        u = f'{self.__url}/payees'
        data = []
        payees = {}
        if isinstance(payee_data, list):
            for x in payee_data:
                p = {
                    'name' : x['payee'],
                    'address1' : x['address_1'],
                    'address2': x['address_2'] if x['address_2'] else "",
                    'city': x['city'],
                    'state': x['state'],
                    'zip': x['zip'],

                }
                data.append(p)
            payees = {'payees' : data}
            payload = json.dumps(payees)
        else:
            payload = json.dumps({
                "payees" : [
                    {
                        "name" : payee_data['payee'],
                        "address1" : payee_data['address_1'],
                        "address2": payee_data['address_2'] if payee_data['address_2'] else "",
                        "city": payee_data['city'],
                        "state": payee_data['state'],
                        "zip": payee_data['zip']
                    }
                ]
            })
        try:
            response = requests.request("POST", u, headers=self.__header, data=payload)
            response.raise_for_status()
            r = response.json()
            l_payees = r['data']['payees']
            d_pid = {}
            for a in l_payees:
                d_pid[a['payeeId']] = a['name']
            return d_pid
        except HTTPError as e:
            d = response.json()
            return f'{e.response.status_code}',d["errorMsg"]
    
    def update_payee(self,pid,payload):
        u = f'{self.__url}/payees/pid'
        try:
            response = requests.request("POST", u, headers=self.__header, data=payload)
            response.raise_for_status()
            return response.text
        except HTTPError as e:
            d = response.json()
            return f'{e.response.status_code}',d["errorMsg"]

    def delete_payee(self,payeeId):
        u = f'{self.__url}/payees/{payeeId}'
        payload = {}
        try:
            response = requests.request("DELETE", u, headers=self.__header, data=payload)
            response.raise_for_status()
            return response.text
        except HTTPError as e:
            d = response.json()
            return f'{e.response.status_code}',d["errorMsg"]

    ###Checks
    def retrieve_all_checks(self,payeeId):
        '''Retrieves all checks that have been created in the system'''
        u = f'{self.__url}/checks?perPage=&page&status&term'
        payload = {}
        try:
            response = requests.request("GET", u, headers=self.__header, data=payload)
            response.raise_for_status()
            return response.text
        except HTTPError as e:
            d = response.json()
            return f'{e.response.status_code}',d["errorMsg"]

    def get_check(self,checkId):
        '''Gets a check by the check Id'''
        u = f'{self.__url}/checks/{checkId}'
        payload = {}
        try:
            response = requests.request("GET", u, headers=self.__header, data=payload)
            response.raise_for_status()
            return response.text
        except HTTPError as e:
            d = response.json()
            return f'{e.response.status_code}',d["errorMsg"]

    def create_check(self,payload):
        '''Create a check within the system. A Payee must be deifned in the
        system already to create a check for that entity
        :param:     payload=this is a dict of bank account Ids that contain a
                    list of payee Ids to be paid
        returns the check Id and check number for each check created'''
        u = f'{self.__url}/checks'
        try:
            response = requests.request("POST", u, headers=self.__header, data=payload)
            response.raise_for_status()
            cd = response.json()
            cid = cd["data"]["checks"][0]["checkId"]
            return cid
        except HTTPError as e:
            d = response.json()
            return f'{e.response.status_code}',d["errorMsg"]

    def update_check(self,checkId,data):
        '''Update a check'''
        u = f'{self.__url}/checks/{checkId}'
        try:
            response = requests.request("POST", u, headers=self.__header, data=data)
            response.raise_for_status()
            cd = response.json()
            cid = cd["data"]["checks"][0]["checkId"]
            return cid
        except HTTPError as e:
            d = response.json()
            return f'{e.response.status_code}',d["errorMsg"]

    def print_checks(self,checkIds):
        '''Prints the check Ids supplied as a list
        :param:     checkIds=a list of check Ids
        returns the urls for pdf fiels for the checks
        '''
        u = f'{self.__url}/checks/print'
        if isinstance(checkIds,str):
            payload = json.dumps({
                "paper_type" : 1,
                "checkId" : [
                    checkIds
                ]
            })
        else:
            payload = json.dumps({
                "paper_type" : 1,
                "checkId" : checkIds
            })            
        try:
            response = requests.request("POST", u, headers=self.__header, data=payload)
            response.raise_for_status()
            r = response.json()
            url = r["data"]["url"]
            return url
        except HTTPError as e:
            d = response.json()
            return f'{e.response.status_code}',d["errorMsg"]