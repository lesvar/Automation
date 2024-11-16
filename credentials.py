from akamai.edgegrid import EdgeRc, EdgeGridAuth  # Import EdgeRc and EdgeGridAuth classes from the Akamai EdgeGrid library
from requests import Session  # Import the Session class from the requests library to manage HTTP sessions
from urllib.parse import urljoin  # Import urljoin to construct the full URL by combining the base URL and endpoint
from pathlib import Path  # Import Path from pathlib to manage file paths in a platform-independent way

# Load the .edgerc configuration file from the user's home directory
EDGERC = EdgeRc(str(Path.home().joinpath('.edgerc')))

# Define the section in the .edgerc file to use; 'default' is the typical section name
SECTION = 'default'

# Construct the base URL for Akamai API requests using the host value from the .edgerc file
baseurl = f'https://{EDGERC.get(SECTION, "host")}'

# Create a new session object to persist certain parameters across requests
session = Session()

# Set the session's authentication method using EdgeGridAuth, initialized with the .edgerc file and section
session.auth = EdgeGridAuth.from_edgerc(EDGERC, SECTION)

def _get_all_switch_keys(my_account):
    """
    Private function to retrieve all account switch keys for a given account name.

    Parameters:
        my_account (str): The name of the account to search for.

    Returns:
        dict: A dictionary containing the account switch keys related to the specified account.
    """
    # Define query parameters with the account name for searching switch keys
    qparam = {
        'search': my_account
    }
    
    # Send a GET request to the 'identity-management/v3/api-clients/self/account-switch-keys' endpoint
    # with the query parameters, and return the JSON response
    return session.get(urljoin(baseurl, 'identity-management/v3/api-clients/self/account-switch-keys'), params=qparam).json()

def generate_switch_key():
    """
    Prompts the user to input an account name, retrieves the switch keys for that account, 
    and allows the user to select a switch key.

    Returns:
        str: The selected account switch key.
    """
    # Prompt the user to input the account name to search for switch keys
    my_account = input('Enter account name: ')
    
    # Call the private function to get the switch keys for the input account
    accounts = _get_all_switch_keys(my_account)
    
    # Iterate over the retrieved accounts and display them to the user with an index number
    for i, account in enumerate(accounts, start=1):
        print(f'{i}: {account["accountName"]}')
    
    # Prompt the user to select the account switch key by its index number
    key_number = int(input('Enter key number: '))
    
    # Retrieve the selected switch key from the list based on the user's input
    switch_key = accounts[key_number - 1]['accountSwitchKey']
    
    # Return the selected switch key
    return switch_key

if __name__ == '__main__':
    # If the script is executed directly (not imported as a module), generate and print the switch key
    print(generate_switch_key())