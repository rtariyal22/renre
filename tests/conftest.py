import os
import pytest
import tempfile
import json

@pytest.fixture
def contract_sample():
    '''
    Contract fixture
    Returns: dictionary containing contract details
    '''
    return {"Coverage": [{ "Attribute": "Location", "Include": [
        "USA", "Canada"]}, { "Attribute": "Peril", "Exclude": [
        "Tornado"]}], "MaxAmount": 3000}

@pytest.fixture
def contract_file(contract_sample):
    '''
    Creates a temporary csv file, writes contract details in it and return's it path
    Args: contract_sample fixture
    Returns: String  
    '''
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(json.dumps(contract_sample))
    return path

@pytest.fixture
def invalid_contract_file():
    '''
    Creates a temporary empty csv file and return's it path
    Args: None
    Returns: String  
    '''
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp:
        tmp.write('sample data')
    return path


@pytest.fixture
def deal_sample():
    '''
    Deal sample fixutre: Comma seperated values
    Args: None
    Returns: String  
    '''
    return '''DealId,Company,Peril,Location
    1,WestCoast,Earthquake,USA
    2,WestCoast,Hailstone,Canada
    3,AsianCo,Hurricane,Philippines
    4,AsianCo,Earthquake,New Zealand
    5,GeorgiaInsurance,Hurricane,USA
    6,MidWestInc,Tornado,USA
    '''

@pytest.fixture
def invalid_deal_file():
    '''
    Creates a temporary empty csv file and return's it path
    Args: None
    Returns: String  
    '''
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp:
        tmp.write('')
    return path


@pytest.fixture
def deal_file_path(deal_sample):
    '''
    Creates a temporary csv file, writes deals details in it and return's it path
    Args: deal fixture
    Returns: String  
    '''
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(deal_sample)
    return path


@pytest.fixture
def loss_sample():
    '''
    Loss sample fixutre: Comma seperated values
    Args: None
    Returns: String  
    '''
    return '''EventId,DealId,Loss
    1,1,2000
    2,1,1500
    3,5,4000
    4,6,1000
    '''

@pytest.fixture
def invalid_loss_file():
    '''
    Creates a temporary empty csv file and return's it path
    Args: None
    Returns: String  
    '''
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp:
        tmp.write('')
    return path

@pytest.fixture
def loss_file_path(loss_sample):
    '''
    Creates a temporary csv file, writes loss details in it and return's it path
    Args: loss fixture
    Returns: String  
    '''
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(loss_sample)
    return path