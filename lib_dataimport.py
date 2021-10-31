import pandas as pd
import numpy as np
import scipy as sp

def read_data(filename="all_letters.csv"):
    # Read preprocessed CSV file
    df = pd.read_csv(filename, sep="\t", header=None)
    df.columns = ["Nb", "Author", "Content"]
    return df
