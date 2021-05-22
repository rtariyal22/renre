import pytest
from models import ContractModel


def test_failed_exit_if_invalid_contract_file_path():
    '''
    Test if ContractModel class exits with system code 1 if non existing json file is provided to it.
    '''
    with pytest.raises(SystemExit) as e:
        ContractModel(data_path='random.json')
    assert e.type == SystemExit
    assert e.value.code == 1

def test_failed_exit_if_invalid_contract_file_data(invalid_contract_file):
    '''
    Test if ContractModel class exits with system code 1 if invalid json file is provided to it.
    '''
    with pytest.raises(SystemExit) as e:
        ContractModel(data_path=invalid_contract_file)
    assert e.type == SystemExit
    assert e.value.code == 1

def test_contract_max_amount(contract_file, contract_sample):
    '''
    Test ContractModel max_amount should match max amout defined in contract
    '''
    contract_object = ContractModel(data_path=contract_file)
    assert contract_object.max_amount == contract_sample['MaxAmount']

def test_contract_included_location(contract_file, contract_sample):
    '''
    Test ContractModel included locations should included locations defined in contract
    '''
    contract_object = ContractModel(data_path=contract_file)
    assert contract_object.included_locations == contract_sample['Coverage'][0]['Include']

def test_contract_excluded_peril(contract_file, contract_sample):
    '''
    Test ContractModel excluded peril should exclude peril defined in contract
    '''
    contract_object = ContractModel(data_path=contract_file)
    assert contract_object.excluded_peril == contract_sample['Coverage'][1]['Exclude']
