import pandas as pd

def getData(path:str,category:str,filename:str):
    data = pd.read_csv(path+'/'+category+'/'+filename,
                        thousands=',')  # , index_col=0
    return data
    