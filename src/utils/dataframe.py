
import pandas

def flatten_dataframes(dataframes : pandas.Series):
    """
    Flatten a Series with DataFrame objects.

    Passes makes sure the output has index both from the series, and each dataframe
    """
    
    out = []

    outer_index = dataframes.index.names
    for idx, df in dataframes.items():
        inner_index = df.index.names
        if len(outer_index) == 1:
            idx = [ idx ]
        
        df = df.copy().reset_index() # avoid mutating input

        # add outer index data to the inner dataframes
        for k, v in zip(outer_index, idx):
            df[k] = v

        out.append(df)

    index = outer_index + inner_index
    df = pandas.concat(out)
    df = df.set_index(index)
    return df
