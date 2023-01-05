import json

def check_if_encrypted(data):
    if data['encrypted'] == False:
        return False
    elif data['encrypted'] == True:
        print("The file supplied is encrypted.")
        print("You must decrypt your file before proceeding.")
        exit()


def load_json_into_memory(path):
    with open(path, "r") as f:
        return json.load(f)


def increase_indent_of_str_array(array, multiplier):
    prepended_array = []
    for row in array:
        prepended_array.append( ( '\t' * multiplier ) + row)
    array = prepended_array

    return array


def property_to_list(property):
    property_list = []
    
    if property['type'] == 1: # Login
        property_list = store_json_property_login_as_array(property)

    elif property['type'] == 2: # Secure Note
        property_list = store_json_property_secure_note_as_array(property)

    elif property['type'] == 3: # Credit Card
        property_list = store_json_property_card_as_array(property)

    elif property['type'] == 4: # Identity
        property_list = store_json_property_identity_as_array(property)

    else:
        print('Undefined Type: ', property)
        exit()
    
    return property_list


def sort_json_by_property_items_type(json_data):
    '''
    Sort the JSON object by the value of the "type" key within the "items" key
    '''
    json_data["items"] = sorted(json_data["items"], key=lambda x: x["type"])
    return json_data

def store_json_property_card_as_array(card):
    property_list = []

    property_type =  'Card'
    print(f'\t{property_type}')

    # supply verbose sub properties
    if verbose_mode == 1:
        property_list.extend(
            [
            f"favorite: {property['favorite']}",
            f"folderId: {property['folderId']}",
            f"id: {property['id']}",
            f"notes: {property['notes']}",
            f"organizationId: {property['organizationId']}",
            f"reprompt: {property['reprompt']}",
            f"type: {property['type']}",
            ]
        )

    # supply nominal sub properties
    property_list.extend(
        [
        f"name:             {property['name']}",
        f"Card Holder Name: {property['card']['cardholderName']}",
        f"Card Brand:       {property['card']['brand']}",
        f"Card Number:      {property['card']['number']}",
        f"Card Exp Month:   {property['card']['expMonth']}",
        f"Card Exp Year:    {property['card']['expYear']}",
        f"Card CV Code:     {property['card']['code']}"
        ]
    )

    property_list = increase_indent_of_str_array(property_list, 2)

    return property_list 


def store_json_property_identity_as_array(identity):
    property_list = []

    property_type =  'Identity'
    print(f'\t{property_type}')

    # supply verbose sub properties
    if verbose_mode == 1:
        property_list.extend(
            [
            f"collectionIds: {property['collectionIds']}",
            f"favorite: {property['favorite']}",
            f"folderId: {property['folderId']}",
            f"id: {property['id']}",
            f"notes: {property['notes']}",
            f"organizationId: {property['organizationId']}",
            f"reprompt: {property['reprompt']}",
            f"type: {property['type']}",
            ]
        )

    # supply nominal sub properties
    property_list.extend(
        [
        f"Full Name: {property['name']}",
        f"Title: {property['identity']['title']}",
        f"First Name: {property['identity']['firstName']}",
        f"Middle Name: {property['identity']['middleName']}",
        f"Last Name: {property['identity']['lastName']}",
        f"Address Line 1: {property['identity']['address1']}",
        f"Address Line 2: {property['identity']['address2']}",
        f"Address Line 3: {property['identity']['address3']}",
        f"City: {property['identity']['city']}",
        f"State: {property['identity']['state']}",
        f"Zip Code: {property['identity']['postalCode']}",
        f"Country: {property['identity']['country']}",
        f"Company: {property['identity']['company']}",
        f"E-mail: {property['identity']['email']}",
        f"Phone Number: {property['identity']['phone']}",
        f"SSN: {property['identity']['ssn']}",
        f"Username: {property['identity']['username']}",
        f"Passport Number: {property['identity']['passportNumber']}",
        f"License Number: {property['identity']['licenseNumber']}",
        ]
    )

    property_list = increase_indent_of_str_array(property_list, 2)
    return property_list 


def remove_string_formatting(array):
    # Remove new lines
    while '\n' in array:
        array = array.replace('\n', ' ')

    # Remove tabs
    while '\t' in array:
        array = array.replace('\t', ' ')

    # Remove excess spacing
    while '  ' in array:
        array = array.replace('  ', ' ')

    split_strings = []
    while len(array) > 40:
        split_strings.append(array[:40])
        array = array[40:]
    split_strings.append(array)

    secure_notes_tabs = ''
    for line in split_strings:
        secure_notes_tabs = secure_notes_tabs + '\n\t\t\t' + line
    split_strings = secure_notes_tabs
    return split_strings



def store_json_property_login_as_array(property):
    property_list = []
    uris = []

    # some login properties do not have URIs
    if 'uris' in property['login']:
        for uri in property['login']['uris']:
            uris.append(uri)
    property_type =  'Login'
    print(f'\t{property_type}')

    # Format Note
    if 'notes' in property:
        if property['notes'] == '':
            notes = ''
            pass
        elif property['notes'] == None:
            notes = ''
            pass
        else:
            notes = property['notes']
            notes = remove_string_formatting(notes)
    else:
        notes = ''

    # supply verbose sub properties
    if verbose_mode == 1:
        property_list.extend(
            [
            f"collectionIds: {property['collectionIds']}",
            f"favorite: {property['favorite']}",
            f"folderId: {property['folderId']}",
            f"id: {property['id']}",
            f"login URL(s): {uris}",
            f"organizationId: {property['organizationId']}",
            f"reprompt: {property['reprompt']}",
            f"type: {property['type']}",
            ]
        )

    # supply nominal sub properties
    property_list.extend(
        [
        f"name: {property['name']}",
        f"notes:" + notes,
        f"username: {property['login']['username']}",
        f"password: {property['login']['password']}",
        f"totp: {property['login']['totp']}"
        ]
    )

    property_list = increase_indent_of_str_array(property_list, 2)
    return property_list 


def store_json_property_secure_note_as_array(property):
    secure_note_list = []
    property_type = '\tSecure Note'
    print(f'{property_type}')

    # Format Secure Note
    secure_notes = property['notes']
    secure_notes = remove_string_formatting(secure_notes)

    # supply verbose sub properties
    if verbose_mode == 1:
        secure_note_list.extend(
            [
            f"collectionIds: {property['collectionIds']}",
            f"favorite: {property['favorite']}",
            f"folderId: {property['folderId']}",
            f"id: {property['id']}",
            f"type: {property['type']}",
            f"organizationId: {property['organizationId']}",
            f"reprompt: {property['reprompt']}",
            f"secureNote: {secure_note_list}",
            ]
        )
    
    # supply nominal sub properties
    secure_note_list.extend(
        [
        f"name: {property['name']}",
        f"notes: " + secure_notes
        # f"notes: {property['notes']}",
        ]
    )

    secure_note_list = increase_indent_of_str_array(secure_note_list, 2)
    return secure_note_list


if __name__ == "__main__":
    verbose_mode = 0
    json_var = load_json_into_memory("bitwarden_export.json")
    json_var = sort_json_by_property_items_type(json_var)
    check_if_encrypted(json_var)

    # Iterate through collections of JSON
    for collection in json_var:
        if collection == 'encrypted':
            continue

        if collection == 'folders':
            if verbose_mode == 1:
                print('Folders')
                for property in json_var['folders']:
                    print('\tName: ', property['name'])
                    print('\tID:   ', property['id'])
            else:
                pass

        if collection == 'items':
            print('Items')
            for property in json_var['items']:
                list_of_property = property_to_list(property)
                for line in list_of_property:
                    print(line)