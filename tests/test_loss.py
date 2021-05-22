import pytest
from models import DealsModel, ContractModel, LossModel
from main import filter_covered_deals, filter_expected_loss, simulate_expected_loss

def test_failed_exit_if_invali_loss_file_path():
    '''
    Test if LossModel class exits with system code 1 if non existing csv file is provided to it.
    '''
    with pytest.raises(SystemExit) as e:
        LossModel(data_path='random.csv')
    assert e.type == SystemExit
    assert e.value.code == 1


def test_failed_exit_if_invalid_loss_file_data(invalid_loss_file):
    '''
    Test if LossModel class exits with system code 1 if empty csv file is provided to it.
    '''
    with pytest.raises(SystemExit) as e:
        LossModel(data_path=invalid_loss_file)
    assert e.type == SystemExit
    assert e.value.code == 1


def test_simulate_expected_loss_with_chunk_file_enabled(contract_file, deal_file_path, loss_file_path):
    '''
    Test expected losses complies a deal with chunk file feature enabled.
    '''
    # Initializing a contract
    _simulate_losses(contract_file, deal_file_path, loss_file_path, 10000, False)


def test_simulate_expected_loss_with_memory_optimization_enabled(contract_file, deal_file_path, loss_file_path):
    '''
    Test expected losses complies a deal with memory optimization feature enabled.
    '''
    # Initializing a contract
    _simulate_losses(contract_file, deal_file_path, loss_file_path, None, True)


def test_simulate_expected_loss_with_chunk_and_memory_optimization_enabled(contract_file, deal_file_path, loss_file_path):
    '''
    Test expected losses complies a deal with chunk file and memory optimization feature enabled.
    '''
    # Initializing a contract
    _simulate_losses(contract_file, deal_file_path, loss_file_path, 10000, True)


def test_simulate_expected_loss_with_chunk_and_memory_optimization_disabled(contract_file, deal_file_path, loss_file_path):
    '''
    Test expected losses complies a deal with chunk file and memory optimization feature disabled.
    '''
    # Initializing a contract
    _simulate_losses(contract_file, deal_file_path, loss_file_path, None, False)


def _simulate_losses(contract_file, deal_file_path, loss_file_path, chunk_size, optimize_memory):
    '''
    Test expected losses complies a deal
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

    # Initializing losses
    loss_obj = LossModel(data_path=loss_file_path, chunk_size=chunk_size, optimize_memory=optimize_memory)

    if chunk_size:
        loss_data_frame = loss_obj.data.__next__()
    else:
        loss_data_frame = loss_obj.data[0]

    # Finding losses for filtered deals
    filtered_losses = filter_expected_loss(loss_data_frame, filtered_deals)

    # Calculating expected losses for filtered deals based on their losses
    expected_loss = simulate_expected_loss(filtered_losses, contract_object)
    expected_loss = expected_loss.reset_index()

    # Converting dataframe to a python list
    row_list =[]
    # Iterate over each row
    for rows in expected_loss.itertuples():
        # Create list for the current row
        my_list =[rows.Peril, rows.Loss]
        # append the list to the final list
        row_list.append(my_list)
    assert len(row_list) == 2
    assert row_list == [['Earthquake', 3500], ['Hurricane', 3000]]