import pandas as pd

from thefuzz import fuzz, process  

#Windows df = pd.read_excel("Z:\Group project\Contact emails\CONTACT EMAILS.xlsx")

df = pd.read_excel("/Users/Jonny/Desktop/University-chatbot/Contact emails/Contact Emails.xlsx")








import pandas as pd
from thefuzz import fuzz, process

class Fuzzymatch:
    def __init__(self, path):
        self.path = path
        # Load the dataframe and store it in the class instance
        self.df = pd.read_excel(path)
        # Store the unique departments list
        self.departments = self.df['Department'].dropna().unique().tolist()

    def find_department(self, userinput, threshold=70):
        # Use self.departments to access the list created in __init__
        result = process.extractOne(userinput, self.departments, scorer=fuzz.token_set_ratio)

        if result:
            match_name, score = result
            
            if score >= threshold:
                # Use self.df to access the dataframe
                email = self.df.loc[self.df['Department'] == match_name, 'Emails'].item()
            
                print(f"Found match: {match_name} (Score: {score})")
                print(f"Email: {email}")
                return email # Returning the email makes it useful for your RAG engine
            else:
                print("I'm not sure which department you mean. Could you be more specific?")
                return None
        else:
            print("No match found.")
            return None


        








if __name__ == "__main__":

    matcher = Fuzzymatch("/Users/Jonny/Desktop/University-chatbot/Contact emails/CONTACT EMAILS.xlsx")
    matcher.find_department("Ipoint")




















