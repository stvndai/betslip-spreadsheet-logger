import pandas as pd


def write(filePath, data):

    
    df = pd.DataFrame([data])

    df.to_csv(filePath, mode='a', index=False, header=False)
    
    print("writen to file " + filePath + "\n") 
    print(data)
