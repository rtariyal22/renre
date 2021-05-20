import pandas as pd
import pytest
from models import DealsModel, ContractModel, LossModel
from main import get_covered_deals, simulate_expected_loss

def test_failed_exit_if_invali_loss_file_path():
    with pytest.raises(SystemExit) as e:
        LossModel(data_path='random.csv')
    assert e.type == SystemExit
    assert e.value.code == 1


def test_failed_exit_if_invalid_loss_file_data(invalid_loss_file):
    with pytest.raises(SystemExit) as e:
        LossModel(data_path=invalid_loss_file)
    assert e.type == SystemExit
    assert e.value.code == 1

def test_simulate_expected_loss(contract_file, deal_file_path, loss_file_path):
    deal_data_frame, contract_object = get_covered_deals(contract_file_path=contract_file, deal_file_path=deal_file_path)
    expected_claims_dataframe = simulate_expected_loss(deal_data_frame, contract_object, loss_file_path=loss_file_path)
    expected_claims_dataframe = expected_claims_dataframe.reset_index()
    # Create an empty list
    row_list =[]
    # Iterate over each row
    for rows in expected_claims_dataframe.itertuples():
        # Create list for the current row
        my_list =[rows.Peril, rows.Loss]
        # append the list to the final list
        row_list.append(my_list)
    assert len(row_list) == 2
    assert row_list == [['Earthquake', 3500], ['Hurricane', 3000]]