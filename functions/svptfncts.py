## @package svptfncts

## Imports ##
import pickle
       
def saveData(data,filename):
    """
    Function to pickle and save data. 
    .pickle file containing data in current directory, 
    unless specified in file name.

    Parameters
    ----------
    data : obj
        The data to save in a pickle file
    filename : str
        Path/name to save the pickled data;
        '.pickle' extension added automatically
    """
    if '.pickle' not in filename: 
        file = open(filename+'.pickle','wb')
    else: 
        file = open(filename,'wb')
    pickle.dump(data,file)
    file.close()
        
def loadData(filename):
    """
    Function to load pickled data.

    Parameters
    ----------
    filename : str
        The path/name of pickled data file to load. 
        '.pickle' extension added automatically 

    Returns
    -------
    obj
        Unpickled Python object
    """
    if '.pickle' not in filename: 
        file = open(filename+'.pickle','rb')
    else: 
        file = open(filename,'rb')
    data = pickle.load(file)
    file.close()
    return data
