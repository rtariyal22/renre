import pandas as pd
import pytest
from models import DealsModel, ContractModel
from main import get_covered_deals

def test_failed_exit_if_invali_deal_file_path():
    with pytest.raises(SystemExit) as e:
        DealsModel(data_path='random.csv')
    assert e.type == SystemExit
    assert e.value.code == 1


def test_failed_exit_if_invalid_deal_file_data(invalid_deal_file):
    with pytest.raises(SystemExit) as e:
        DealsModel(data_path=invalid_deal_file)
    assert e.type == SystemExit
    assert e.value.code == 1

def test_covered_deals(contract_file, deal_file_path):
    deal_data_frame, contract_object = get_covered_deals(contract_file_path=contract_file, deal_file_path=deal_file_path)
    assert contract_object.included_locations == ["USA", "Canada"]
    assert contract_object.excluded_peril == ["Tornado"]
    assert contract_object.max_amount == 3000
    # Removing index
    deal_data_frame = deal_data_frame.reset_index()
    # Create an empty list
    row_list =[]
    # Iterate over each row
    for rows in deal_data_frame.itertuples():
        # Create list for the current row
        my_list =[rows.DealId, rows.Company, rows.Peril, rows.Location]
        # append the list to the final list
        row_list.append(my_list)
    
    # Print the list
    assert len(row_list) == 3
    assert row_list == [[1, 'WestCoast', 'Earthquake', 'USA'], 
    [2, 'WestCoast', 'Hailstone', 'Canada'], 
    [5, 'GeorgiaInsurance', 'Hurricane', 'USA']]