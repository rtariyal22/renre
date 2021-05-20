#!/usr/bin/python

import models as insurance_models
import constants as CONSTANTS


def get_covered_deals(contract_file_path=None, deal_file_path=None):
    '''
    Reads deal's data frame filters its data based on the contract.
    args: contract_file(String: optional), deal_file_path(String: optional)
    Returns panda data frame object and contract object
    '''
    # Initializing a contract
    contract_object = insurance_models.ContractModel(data_path=contract_file_path)

    # Initailizing a deal
    deal_object = insurance_models.DealsModel(data_path=deal_file_path)
    
    # setting deal's data frame
    deal_data_frame = deal_object.data

    # setting Deal ID as deal data frame index
    deal_data_frame = deal_data_frame.set_index(CONSTANTS.DEAL_ID_COL)

    # Filtering deals based on locations included in contract
    included_locations = contract_object.included_locations
    deal_data_frame = deal_data_frame[deal_data_frame[CONSTANTS.LOCATION_COLUMN].isin(included_locations)]

    # Getting list of peril excluded from contract
    excluded_peril = contract_object.excluded_peril

    # Filtering deals based on excluded peril 
    deal_data_frame = deal_data_frame[~deal_data_frame[CONSTANTS.PERIL_COL].isin(excluded_peril)]
    print('Deals covered by the reinsurance contract: \n %s\n' % deal_data_frame)
    return deal_data_frame, contract_object

def simulate_expected_loss(deal_data_frame, contract_object, loss_file_path=None):
    # Initializing losses
    loss_obj = insurance_models.LossModel(data_path=loss_file_path)
    
    # setting losses data frame
    losses_data_frame = loss_obj.data

    # setting Deal ID as loss data frame index
    losses_data_frame = losses_data_frame.set_index(CONSTANTS.DEAL_ID_COL)

    # Merging losses data frame into deal data frame using Deald ID as index
    expected_claims_dataframe = deal_data_frame.merge(losses_data_frame, left_index=True, right_index=True)
    
    # Capping maximum claim amount of loss due to peril with max amount mentioned in contract.
    expected_claims_dataframe.loc[expected_claims_dataframe[CONSTANTS.LOSS_COL] > contract_object.max_amount, CONSTANTS.LOSS_COL] = contract_object.max_amount
    
    # Calculating total loss occured for each peril.
    expected_claims_dataframe = expected_claims_dataframe.groupby(CONSTANTS.PERIL_COL).sum()
    
    # Removing EventId column from dataframe
    expected_claims_dataframe.drop(CONSTANTS.EVENT_ID_COL, axis='columns', inplace=True)
    print ('InsureCo potential claim on the reinsurance contract: \n %s' % expected_claims_dataframe)
    return expected_claims_dataframe


if __name__ == '__main__':
    deal_data_frame, contract_object = get_covered_deals()
    simulate_expected_loss(deal_data_frame, contract_object)