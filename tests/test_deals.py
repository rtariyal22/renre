import pytest
from models import DealsModel, ContractModel
from main import filter_covered_deals

def test_failed_exit_if_invali_deal_file_path():
    '''
    Test if DealsModel class exits with system code 1 if non existing csv file is provided to it.
    '''
    with pytest.raises(SystemExit) as e:
        DealsModel(data_path='random.csv')
    assert e.type == SystemExit
    assert e.value.code == 1


def test_failed_exit_if_invalid_deal_file_data(invalid_deal_file):
    '''
    Test if ContractModel class exits with system code 1 if empty csv file is provided to it.
    '''
    with pytest.raises(SystemExit) as e:
        DealsModel(data_path=invalid_deal_file)
    assert e.type == SystemExit
    assert e.value.code == 1


def test_covered_deals_with_chunk_file_enabled(contract_file, deal_file_path):
    '''
    Test covered deals conforming to contract with chunk file feature enabled.
    '''
    _simulate_deals(contract_file, deal_file_path, 10000, False)


def test_covered_deals_with_memory_optimization_enabled(contract_file, deal_file_path):
    '''
    Test covered deals conforming to contract with memory optimization feature enabled.
    '''
    _simulate_deals(contract_file, deal_file_path, None, True)


def test_covered_deals_with_chunk_and_memory_optimization_enabled(contract_file, deal_file_path):
    '''
    Test covered deals conforming to contract with chunk files and memory optimization feature enabled.
    '''
    _simulate_deals(contract_file, deal_file_path, 10000, True)

def test_covered_deals_with_chunk_and_memory_optimization_disabled(contract_file, deal_file_path):
    '''
    Test covered deals conforming to contract with memory optimization feature disabled.
    '''
    _simulate_deals(contract_file, deal_file_path, 10000, True)


def _simulate_deals(contract_file, deal_file_path, chunk_size, optimize_memory):
    '''
    Helper function to test deals.
    '''
    # Initializing a contract
    contract_object = ContractModel(data_path=contract_file)
    
    # Initailizing a deal
    deal_object = DealsModel(data_path=deal_file_path, chunk_size=chunk_size, optimize_memory=optimize_memory)    

    if chunk_size:
        deal_data_frame = deal_object.data.__next__()
    else:
        deal_data_frame = deal_object.data[0]

    # Finding deals covered by reinsurance contract
    filtered_deals = filter_covered_deals(deal_data_frame, contract_object)

    # Removing index
    filtered_deals = filtered_deals.reset_index()

    # Converting dataframe to a python list
    row_list =[]
    # Iterate over each row
    for rows in filtered_deals.itertuples():
        # Create list for the current row
        my_list =[rows.DealId, rows.Company, rows.Peril, rows.Location]
        # append the list to the final list
        row_list.append(my_list)
    
    # Checking if filtered deals are matching with constraints defined in contract
    assert len(row_list) == 3
    assert row_list == [[1, 'WestCoast', 'Earthquake', 'USA'], 
    [2, 'WestCoast', 'Hailstone', 'Canada'], 
    [5, 'GeorgiaInsurance', 'Hurricane', 'USA']]