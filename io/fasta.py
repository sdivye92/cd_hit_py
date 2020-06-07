from cd_hit.error import *

def read_fasta(file_path):
    import os
    import pandas as pd
    if not os.path.exists(file_path):
        raise FileNotFoundError("File {0} does not exist: '{0}'".format(file_path))
    elif not os.path.isfile(file_path):
        raise InvalidFileTypeError("File {0} is not of valid type: '{0}'".format(file_path))
    try:
        with open(file_path) as f:
            content = f.read()
            seq_lst = [seq.strip('\n').split('\n') for seq in content.split('>') if seq.strip('\n')]
        return pd.DataFrame(seq_lst, columns=["Header", "Sequence"])
    except:
        raise FileParsingError("Error occured in parsing file {0}".format(file_path))
