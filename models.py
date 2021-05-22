import pandas as pd
import json
import os


class CsvModel(object):
    '''
    This class reads CSV file using pandas. This pandas data frame will be available as "data" attribute of class object.
    While reading large files you can set chunk_size and optimize_memory which will fit in large dataset in memory.
    If chunk_size is provided it will read CSV file in chunks and return iterable dataframe object else it will
    return a list of dataframe object .
    If optimize_memory is set to true it will typecast 64 bit int and float values to 16 bit values for saving memory.
    '''

    def __init__(self, data_path, chunk_size=None, optimize_memory=False):
        self.data_path = data_path
        self.chunk_size = chunk_size
        self.optimize_memory = optimize_memory
        self.data = self._setData()

    def _setData(self):
        '''
        Validates data available in data_path and raises JSONDecodeError if invalid data is provided
        args: data_path (string: optional), chink_size(integer: optional), optimize_memory(boolean: optional)
        return: dict
        '''
        dtypes_dict = {}
        # If optimize_memory is true then it converts int64 and float64 datatypes present in dataset to int16 or
        # float16. This reduces memory footprint of data loaded in the RAM.
        if self.optimize_memory:
            dtypes_dict = self._optimizeMemory()
        try:
            data = pd.read_csv(self.data_path, chunksize=self.chunk_size, dtype=dtypes_dict)
        except pd.errors.EmptyDataError:
            print('File present in %s is empty' % self.data_path)
            exit(1)
        except Exception as e:
            print('Failed with exception while reading data from %s with exception %s' % (self.data_path, e))
            exit(1)
        if not self.chunk_size:
            data = [data]
        return data
    
    def _optimizeMemory(self):
        '''
        This methods returns a dictionary which can be passed to panda data frame reader to downcast 
        datatypes of 64 bit int and float to 16 bit values.
        '''
        dtypes_dict = {}
        try:
            # Reading csv file partially and loading into memory as pandas datframe.
            data_frames = pd.read_csv(self.data_path, chunksize=10)
        except pd.errors.EmptyDataError:
            print('File present in %s is empty' % self.data_path)
            exit(1)
        except Exception as e:
            print('Failed with exception while reading data from %s with exception %s' % (self.data_path, e))
            exit(1)
        else:
            # data_frames is an iterable object. Getting first dataframe object by using next magic function
            data_frame = data_frames.__next__()
            dtypes_dict = list()
            # iterating through dataframe columns and downcasting 64bit int and float values to 16bit values.
            for x in data_frame.dtypes.tolist():
                if x=='int64':
                    dtypes_dict.append('int16')
                elif(x=='float64'):
                    dtypes_dict.append('float16')
                else:
                    dtypes_dict.append('object')
                    
            dtypes_dict = dict(zip(data_frame.columns.tolist(),dtypes_dict))
        return dtypes_dict


class ContractModel(object):
    '''
    Responsible for fetching Contract data
    '''

    def __init__(self, data_path):
        self.data_path = data_path
        self.included_locations = []
        self.excluded_peril = []
        self.max_amount = 0
        self._setDataFromSource()
        self._setContractAttributes()

    def _setDataFromSource(self):
        '''
        Validates data available in data_path and raises JSONDecodeError if invalid data is provided
        args: data_path (string: optional), chink_size(integer: optional)
        return: dict
        '''
        self.data = None
        if not os.path.exists(self.data_path):
            print('Contract file is not available inside %s' % self.data_path)
            exit(1)
        with open(self.data_path, 'r') as fp:
            try:
                self.data = json.loads(fp.read())
            except json.decoder.JSONDecodeError:
                print('Invalid json format supplied in contract file %s' % self.data_path)
                exit(1)
            except Exception as e:
                print('Failed to read Contract file %s with error %s' % (self.data_path, e))
                exit(1)
        
    
    def _setContractAttributes(self):
        '''
        This method sets max_amount, excluded_peril and included_locations attributes of a Contract.
        '''
        setattr(self, 'max_amount', self.data.get('MaxAmount', 0))
        for each_coverage in self.data['Coverage']:
            if each_coverage.get('Attribute') == 'Peril':
                setattr(self, 'excluded_peril', each_coverage.get('Exclude', []))
            elif each_coverage.get('Attribute') == 'Location':
                setattr(self, 'included_locations', each_coverage.get('Include', []))

class DealsModel(CsvModel):
    '''
    Responsible for fetching Deals data. Requires file path to contract csv file.
    '''

    def __init__(self, data_path, chunk_size=None, optimize_memory=False):
        data_path = data_path
        super().__init__(data_path, chunk_size, optimize_memory)
        

class LossModel(CsvModel):
    '''
    Responsible for fetching Losses data. Requires file path to loss csv file.
    '''

    def __init__(self, data_path, chunk_size=None, optimize_memory=False):
        data_path = data_path
        super().__init__(data_path, chunk_size, optimize_memory)

        
