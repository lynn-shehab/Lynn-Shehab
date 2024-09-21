import streamlit as st

st.write("Lynn Shehab's Streamlit App")
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset from the URL
data_url = 'https://linked.aub.edu.lb/pkgcube/data/c87c6b00fb7268d151508e7ec14e0f98_20240908_173516.csv'
data = pd.read_csv(data_url)

# Define the tourism facilities
tourism_facilities = ['Total number of hotels', 'Total number of restaurants', 'Total number of cafes', 'Total number of guest houses']

# Melt the DataFrame for easier plotting
melted_tourism_data = data.melt(id_vars=['Town'], value_vars=tourism_facilities,
var_name='Facility', value_name='Total')


# Title and Subtitle
st.subheader("MSBA 325 - Building Interactive Visualizations with Streamlit Assignment")

# Bar Chart Interactivity
st.header("Comparison of Tourism Facilities Across Towns")

# **Interactivity 1: Dual Dropdowns to select two facility types for comparison**
facility_1 = st.selectbox("Select the First Facility Type:", options=tourism_facilities,
index=0)

facility_2 = st.selectbox("Select the Second Facility Type:", options=[f for f in
tourism_facilities if f != facility_1], index=0)

# Filter the data based on the selected facility types
facility_data_1 = melted_tourism_data[melted_tourism_data['Facility'] == facility_1]
facility_data_2 = melted_tourism_data[melted_tourism_data['Facility'] == facility_2]

# Merge the data for the two facilities into one DataFrame for comparison
merged_data = facility_data_1[['Town', 'Total']].rename(columns={'Total': f'{facility_1} Total'})
merged_data = merged_data.merge(facility_data_2[['Town', 'Total']].rename(columns={'Total': f'{facility_2} Total'}), on='Town', how='inner')

# Interactivity 2: Slider to filter towns based on the minimum total facilities across both types
min_facilities = st.slider("Minimum Total Facilities in a Town (across both selected types):", min_value=0, max_value=int(merged_data[[f'{facility_1} Total', f'{facility_2} Total']].max().max()), value=0)

# Filter towns based on the minimum total facilities threshold
filtered_data = merged_data[(merged_data[f'{facility_1} Total'] >= min_facilities) & (merged_data[f'{facility_2} Total'] >= min_facilities)]

# Visualization: Grouped Bar Chart for comparing two selected facilities
bar_chart = px.bar(filtered_data,
                   x='Town',
                   y=[f'{facility_1} Total', f'{facility_2} Total'],
                   title=f"Bar Chart Visualizing the Comparison of {facility_1} and {facility_2} Across Towns (Min {min_facilities} Facilities)",
                   labels={'variable': 'Total Count', 'Town': 'Town'},
                   barmode='group',
                   height=500)

# Display the bar chart
st.plotly_chart(bar_chart)

# Sunburst Chart Interactivity
st.subheader("Hierarchical View of Tourism Facilities by Town")

# Interactivity 1: Slider to filter towns with at least a certain number of total facilities
total_facility_threshold = st.slider("Select Minimum Total Facilities to Include in the Sunburst Chart:", 0, int(melted_tourism_data['Total'].max()), 0)

# Calculate total facilities per town
town_totals = melted_tourism_data.groupby('Town')['Total'].sum().reset_index()

# Filter towns based on threshold
filtered_towns = town_totals[town_totals['Total'] >= total_facility_threshold]['Town']

# Filter original data based on filtered towns
filtered_sunburst_data = melted_tourism_data[melted_tourism_data['Town'].isin(filtered_towns)]

# Interactivity 2: Select color scheme for the Sunburst chart
color_scheme = st.selectbox("Select a Color Scheme for Sunburst Chart:", options=['Rainbow', 'Viridis', 'Cividis', 'Plotly'])

# Interactivity 3: Option to aggregate data by Town or Facility
aggregation_level = st.radio("Select Aggregation Level:", ('Town Level', 'Facility Level'))

# Sunburst chart based on aggregation level

if aggregation_level == 'Town Level':
  sunburst_chart = px.sunburst(filtered_sunburst_data,
                              path=['Town', 'Facility'],
                              values='Total',
                              title=f'Sunburst Chart of Tourism Facilities by Town (Min {total_facility_threshold} Total Facilities)',
                              color='Facility',
                              color_continuous_scale=color_scheme)

# Aggregate at facility level to show overall facility distribution across towns

else:
    sunburst_chart = px.sunburst(filtered_sunburst_data,
                                 path=['Facility', 'Town'], 
                                 values='Total', 
                                 title=f'Sunburst Chart of Facility Distribution by Town (Min {total_facility_threshold} Total Facilities)', 
                                 color='Facility', 
                                 color_continuous_scale=color_scheme)


# Display the sunburst chart
st.plotly_chart(sunburst_chart)

# Insights section
st.write("### Insights:")
st.write(f"- The bar chart allows you to compare the {facility_1} and the {facility_2} across all towns. You can filter towns based on a minimum threshold for more targeted analysis.")
st.write("- The sunburst chart gives a hierarchical view of tourism facilities by town. With the ability to choose aggregation levels and color schemes, you can gain different perspectives on the data.")


