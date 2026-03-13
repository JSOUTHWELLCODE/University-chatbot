import pandas as pd



#Windows df = pd.read_excel("Z:\Group project\Contact emails\CONTACT EMAILS.xlsx")

#Mac

df = pd.read_excel("/Users/Jonny/Desktop/University-chatbot/Contact emails/CONTACT EMAILS.xlsx")





department = df['Department'].head



# 3. Update only the first 15 rows of the 'Name' column
# .iloc[rows, columns] -> [0:15] means rows 0 to 14
df.iloc[0:15, df.columns.get_loc('Emails')] = df.iloc[0:15, df.columns.get_loc('Name')] + '@huddersfield.com'






print("Updated the first 15 names successfully!")



# Save it back to Excel so the changes stick
df.to_excel("/Users/Jonny/Desktop/University-chatbot/Contact emails/CONTACT EMAILS.xlsx", index=False)





















