import pandas as pd

# Load the CSV files
input_events = pd.read_csv(f'C:\DV\dv-project\Dataset\icu\inputevents.csv')
d_labitems = pd.read_csv(f'C:\DV\dv-project\Dataset\icu\d_items.csv')

# Display the first few rows of each dataframe
print("Input Events Data:")
print(input_events.head())

print("\nLab Items Data:")
print(d_labitems.head())

# Check for unique itemids in both datasets
unique_input_itemids = input_events['itemid'].unique()
unique_lab_itemids = d_labitems['itemid'].unique()

print("\nUnique itemids in input events:")
print(unique_input_itemids)

print("\nUnique itemids in lab items:")
print(unique_lab_itemids)

# Create a mapping of itemid to label for easier lookups
labitem_map = pd.Series(d_labitems.label.values, index=d_labitems.itemid).to_dict()

# Count how many input events are mapped to known labels
input_events['abbreviation'] = input_events['itemid'].map(labitem_map).fillna('Unknown')

# Display aggregated data
aggregated_data = input_events.groupby('itemid').agg(
    frequency=('itemid', 'size'),
    order_category_name=('ordercategoryname', 'first'),
    chart_time=('starttime', 'min'),
    abbreviation=('abbreviation', 'first')
).reset_index()

print("\nAggregated Data:")
print(aggregated_data)

unknown_abbreviations = aggregated_data[aggregated_data['abbreviation'] == 'Unknown']
print("\nItems with Unknown abbreviations:")
print(unknown_abbreviations)
