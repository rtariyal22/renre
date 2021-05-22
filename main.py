#!/usr/bin/python
import pandas as pd
import models as insurance_models
import constants as CONSTANTS


def filter_covered_deals(deal_data_frame, contract_object):
    '''
    Reads deal's data frame and filters its data based on the contract.
    args: deal datframe, ContractModel
    Returns panda data frame object
    '''

    # setting Deal ID as deal data frame index
    deal_data_frame = deal_data_frame.set_index(CONSTANTS.DEAL_ID_COL)

    # Filtering deals based on locations included in contract
    included_locations = contract_object.included_locations
    deal_data_frame = deal_data_frame[deal_data_frame[CONSTANTS.LOCATION_COLUMN].isin(included_locations)]

    # Getting list of peril excluded from contract
    excluded_peril = contract_object.excluded_peril

    # Filtering deals based on excluded peril 
    filtered_deals = deal_data_frame[~deal_data_frame[CONSTANTS.PERIL_COL].isin(excluded_peril)]
    return filtered_deals

def filter_expected_loss(losses_data_frame, filtered_deals):    
    '''
    Reads losses's data frame and merges it with filtered deals.
    args: loss data frame, filtered_deals
    Returns panda data frame object
    '''

    # setting DealID column as loss data frame index
    losses_data_frame = losses_data_frame.set_index(CONSTANTS.DEAL_ID_COL)

    # Merging losses data frame into deal data frame using Deald ID as index
    expected_claims_dataframe = filtered_deals.merge(losses_data_frame, left_index=True, right_index=True)
    
    return expected_claims_dataframe


def simulate_expected_loss(filtered_deals_with_loss, contract_object):
    '''
    Reads merged deals and loss data and calculates the total sum of loss grouped by peril.
    It also caps maximum claim amount per event based on contract.
    args: merged deals and loss dataframe, ContractModel
    Returns panda data frame object
    '''
    # Capping maximum claim amount of loss due to peril with max amount mentioned in contract.
    filtered_deals_with_loss.loc[filtered_deals_with_loss[CONSTANTS.LOSS_COL] > contract_object.max_amount, 
    CONSTANTS.LOSS_COL] = contract_object.max_amount
    
    # Calculating total loss occured for each peril.
    expected_claims_dataframe = filtered_deals_with_loss.groupby(CONSTANTS.PERIL_COL).sum()
    
    # Removing EventId column from dataframe
    expected_claims_dataframe.drop(CONSTANTS.EVENT_ID_COL, axis='columns', inplace=True)
    return expected_claims_dataframe


if __name__ == '__main__':
    # Initializing a contract
    contract_object = insurance_models.ContractModel(data_path=CONSTANTS.CONTRACT_DATA)
    
    # Initailizing a deal by loading Deals.csv file. We are reading this file chunk by chunk.
    deal_object = insurance_models.DealsModel(
        data_path=CONSTANTS.DEALS_DATA, 
        chunk_size=CONSTANTS.CHUNK_SIZE, 
        optimize_memory=CONSTANTS.OPTIMIZE_MEMORY)
    
    # Initializing empty deals dataframe
    filtered_deals = pd.DataFrame([])
    
    # Iterating through each chunk of data frame and filtering out deals that matches contract
    for eachDealChunk in deal_object.data:
        # Finding deals covered by reinsurance contract
        filtered_deals = filtered_deals.append(filter_covered_deals(eachDealChunk, contract_object))
    print('Deals covered by the reinsurance contract: \n %s\n' % filtered_deals)

    # Initializing losses by loading Losses.csv file. We are reading this file chunk by chunk.
    loss_object = insurance_models.LossModel(
        data_path=CONSTANTS.LOSSES_DATA, 
        chunk_size=CONSTANTS.CHUNK_SIZE, 
        optimize_memory=CONSTANTS.OPTIMIZE_MEMORY)
    
    # Initializing empty losses dataframe.
    filtered_losses = pd.DataFrame([])

    # Iterating through each chunk of losses data frame and filtering out losses that matches deals.
    for eachLossChunk in  loss_object.data:
        # Finding losses for filtered deals
        filtered_losses = filter_expected_loss(eachLossChunk, filtered_deals)
    
    # Simulating expected losses for filtered deals based on their losses
    expected_loss = simulate_expected_loss(filtered_losses, contract_object)
    print ('InsureCo potential claim on the reinsurance contract: \n %s' % expected_loss)