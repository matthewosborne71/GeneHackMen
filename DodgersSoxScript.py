import GetAPICred as Cred
import TwitterFunctions as TF
import logging
import pandas as pd

# Get our clients
clients = Cred.get_twitter_client()[2:]

# These are our queries
Queries = ['Dodgers','Red Sox','LADetermined','Ball Park','World Series','Game 4',
            'Rich Hill','Eduardo Rodriguez','Home Run','Single','Base Hit','Dodger Stadium',
            'Dodger Dog','Machado','RedSox','Mookie Betts','MLB','DoDamage','inning',
            'Joe Buck','Ump']

Queries = pd.DataFrame(Queries,columns = ['query'])

# Get a since_id as a baseline
since_id = clients[1].get_user('RedSox').status.id_str

# Set the input data
path = r"C:\\Users\\Matthew Osborne\\Documents\\python_code\\GeneHackMen\\Data\\WorldSeries\\"
FileName = "WorldSeries"
Stopper = 600

# make a log file
logging.basicConfig(filename = path + FileName + "_DataPull" '.log',
                    format = '%(asctime)s - %(message)s',
                    level = logging.INFO)


logging.info("About to run the Query Script!")
# Pull the data
TF.SearchTwitter(clients,since_id,path,Queries,FileName,Stopper)
logging.info("All done with World Series!")
