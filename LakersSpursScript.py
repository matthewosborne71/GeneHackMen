import GetAPICred as Cred
import TwitterFunctions as TF
import logging
import pandas as pd


# Get Our clients
clients = Cred.get_twitter_client()[0:1]

# We're searching for these strings
Queries = ['Lakers','Spurs','Lebron','LakeShow','GoSpursGo','LakersSpurs','Derozan','Lonzo Ball',
            'Lemarcus Aldridge','Patty Mills','Javale McGee','Popovich','Luke Walton','Lakers Defense','Rondo','San Antonio']

# Put the queries in a pandas dataframe
Queries = pd.DataFrame(Queries,columns = ['query'])

# Get a since_id for the data
since_id = clients[1].get_user('Lakers').status.id_str

# Set the input data
path = r"C:\\Users\\Matthew Osborne\\Documents\\python_code\\GeneHackMen\\Data\\LakersSpurs\\"
FileName = "LakersSpurs"
Stopper = 400

# Create a log file
logging.basicConfig(filename = path + FileName + "_DataPull" '.log',
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)


logging.info("About to run the Query Script!")
# Run the queries
TF.SearchTwitter(clients,since_id,path,Queries,FileName,Stopper)
logging.info("All done with Lakers Spurs!")
