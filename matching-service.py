import pandas as pd
from util import output_data

#Data Ingestion
students_data = pd.read_excel("data/raw/students_data.xlsx")
reviews_data = pd.read_excel("data/processed/reviews_data.xlsx")


students_df = pd.DataFrame(students_data)
reviews_df = pd.DataFrame(reviews_data)

#Data Preprocessing
students_df.columns = students_df.iloc[1].str.strip()
students_df = students_df[2:].reset_index(drop=True)


# Convert both first and last names to lowercase to avoid case mismatch
students_df['Name'] = students_df['Name'].str.lower()
students_df['Last Name'] = students_df['Last Name'].str.lower()

reviews_df['Item'] = reviews_df['Item'].str.lower()
reviews_df['Last Name'] = reviews_df['Last Name'].str.lower()

#Match By Name and Last Only 
match_df_1 = pd.merge(students_df, reviews_df, 
                     left_on=['Name', 'Last Name'], 
                     right_on=['Item', 'Last Name'], 
                     how='inner')

match_df_1 = match_df_1.drop_duplicates(subset=["Name", "Last Name"])
output_data("data/processed", "match-dataset-1.xlsx", match_df_1)

print(f"Matched {len(match_df_1)} reviews by name and last name. Dataset saved to data/processed.")

#Match By Name Only 
match_df_2 = pd.merge(students_df, reviews_df, 
                     left_on=['Name'], 
                     right_on=['Item'], 
                     how='inner')

match_df_2 = match_df_2.drop_duplicates(subset=["Name", "Last Name_x"])
output_data("data/processed", "match-dataset-2.xlsx", match_df_2)

print(f"Matched {len(match_df_2)} reviews by first name only. Dataset saved to data/processed.")

#Match By Last Name Only 
match_df_3 = pd.merge(students_df, reviews_df, 
                     left_on=['Last Name'], 
                     right_on=['Last Name'], 
                     how='inner')

match_df_3 = match_df_2.drop_duplicates(subset=["Name", "Last Name_x"])
output_data("data/processed", "match-dataset-3.xlsx", match_df_3)
    
print(f"Matched {len(match_df_3)} reviews by last name only. Dataset saved to data/processed.")

#TODO: Investigate datasets