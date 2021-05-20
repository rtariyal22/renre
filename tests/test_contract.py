import pytest
from models import ContractModel


def test_failed_exit_if_invalid_contract_file_path():
    with pytest.raises(SystemExit) as e:
        ContractModel(data_path='random.json')
    assert e.type == SystemExit
    assert e.value.code == 1

def test_failed_exit_if_invalid_contract_file_data(invalid_contract_file):
    with pytest.raises(SystemExit) as e:
        ContractModel(data_path=invalid_contract_file)
    assert e.type == SystemExit
    assert e.value.code == 1

def test_contract_max_amount(contract_file):
    contract_object = ContractModel(data_path=contract_file)
    assert contract_object.max_amount == 3000

def test_contract_included_location(contract_file):
    contract_object = ContractModel(data_path=contract_file)
    assert contract_object.included_locations == ["USA", "Canada"]

def test_contract_excluded_peril(contract_file):
    contract_object = ContractModel(data_path=contract_file)
    assert contract_object.excluded_peril == ["Tornado"]
