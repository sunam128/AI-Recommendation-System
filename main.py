import time #control the loading state of the app
import pandas as pd #dataset manipulation
from colorama import init,Fore #colored inputs
#initialize colorama
init(autoreset=True)
#load dataset
try:
    df=pd.read_csv("imdb_top_1000.csv")
except FileNotFoundError:
    print(Fore.RED+"Dataset not found")
    raise SystemExit #stop running the code
#extract the genres
genres=sorted({
    g.strip()#removing extra spaces
    for xs in df['Genre'].dropna().str.split(",")#spliting into
    #several genres
    for g in xs
})
#loading state
def dots():
    for _ in range(5):
        print(Fore.RED+".",end="",flush=True)
        time.sleep(0.5)
#recommender function
def recommend(genre=None,rating=None,n=5):
    #copy the dataset
    d=df
    #filter the movies by genres
    if genre:
        #check if the genre exists
        d=d[d["Genre"].str.contains(genre,case=False,na=False)]
    #minimum rating icase user has not provided
    if rating is not None:
        d=d[d['IMDB_Rating']>=rating]
    #movie not found
    if d.empty:
        return "No recommended movies found."
    #shuffle the dataset so that results are random
    d=d.sample(frac=1).reset_index(drop=True)
    #return the top movies found
    return[
        (row["Series_Title"],row["IMDB_Rating"])
         for _,row in d.head(n).iterrows()
    ]
#function-display the recommended movies
def display(recs,name):
    print(Fore.MAGENTA+f"Recommended Movies for {name}\n")
    for i,(title,rating) in enumerate(recs,1): #enumerate means check every output given
        print(f"{Fore.CYAN}{i}.{title}(IMBD Rating:{rating})")
#ask the user for genre
def get_genre():
    print(Fore.GREEN+"Available genres:\n")
    for i,g in enumerate(genres,1):
        print(f"{Fore.LIGHTMAGENTA_EX}{i}.{g}")
    print()#print a blank new line
    while True:
        choice=input(Fore.YELLOW+"Select a Genre:").strip() #.strip() removes unnecessary spaces
        #check if it's a digit
        if choice.isdigit():
            choice=int(choice)#if user did not enter a number
            #check if the number exists in the list
            if 1<=choice<=len(genres):
                return genres[choice-1]#indexing is always a digit behind
        else:#user entered a genre name
            for genre in genres:
                if choice.lower()==genre.lower():#find in the list
                    return genre
        print(Fore.RED+"Invalid genre. Try again.\n")
#ask the user for rating
def get_rating():
    rating=input(Fore.YELLOW+"Enter minimum rating:").strip()
    return float(rating)#convert into a decimal to match the dataset
#main program
print(Fore.CYAN+"Welcome to the movie recommendation system!")
print(Fore.GREEN+"Finding movie recommendations for you...")
name=input(Fore.YELLOW+"Enter their name:")
genre=get_genre()
rating=get_rating()
print(Fore.BLUE+"Searching",end="")#push the next statement to its own line
dots()#loading animation
recs=recommend(genre,rating)
#display the recommended movies
if isinstance(recs,str):
    print(Fore.MAGENTA+recs)
else:
    #display available recommendations
    display(recs,name)