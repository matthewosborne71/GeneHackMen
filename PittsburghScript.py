import TwitterFunctions as TF

path = r"C:\\Users\\Matthew Osborne\\Documents\\python_code\\GeneHackMen\\Data\\"
FileName = r"PittsburghPull"

Queries = ["Pittsburgh Shooting","Synagogue Shooting","Squirrel Hill","Thoughts and Prayers"]

TF.SearchTwitter(path,Queries,FileName)
