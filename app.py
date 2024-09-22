import streamlit as st

st.write("Lynn Shehab's Streamlit App")
import streamlit as st
import pandas as pd
import plotly.express as px

data_url = 'https://linked.aub.edu.lb/pkgcube/data/c87c6b00fb7268d151508e7ec14e0f98_20240908_173516.csv'
data = pd.read_csv(data_url)
df = pd.read_csv(data_url)

tourism_facilities = ['Total number of hotels', 'Total number of restaurants', 'Total number of cafes', 'Total number of guest houses']

melted_tourism_data = data.melt(id_vars=['Town'], value_vars=tourism_facilities,
var_name='Facility', value_name='Total')


st.subheader("MSBA 325 - Building Interactive Visualizations with Streamlit Assignment")

st.header("Comparison of Tourism Facilities Across Towns")
st.write("- This bar chart below visualizes the total counts of different types of tourism facilities (hotels, restaurants, cafes, and guest houses) for each Lebanese town.")
st.write("- The X-Axis represents different Lebanese towns, whereas the Y-Axis represents the total count of the type of facility")

facility_1 = st.selectbox("Select the First Facility Type:", options=tourism_facilities, index=0)

facility_2 = st.selectbox("Select the Second Facility Type:", options=[f for f in tourism_facilities if f != facility_1], index=0)

if facility_1 and facility_2:
    st.write(f"- The interactivity of the bar chart allows you to compare the {facility_1} and the {facility_2} across all towns. You can filter towns based on a minimum threshold for more targeted analysis, and you can also isolate its legends.")

facility_data_1 = melted_tourism_data[melted_tourism_data['Facility'] == facility_1]
facility_data_2 = melted_tourism_data[melted_tourism_data['Facility'] == facility_2]

merged_data = facility_data_1[['Town', 'Total']].rename(columns={'Total': f'{facility_1} Total'})
merged_data = merged_data.merge(facility_data_2[['Town', 'Total']].rename(columns={'Total': f'{facility_2} Total'}), on='Town', how='inner')

min_facilities = st.slider("Minimum Total Facilities in a Town (across both selected types):", min_value=0, max_value=int(merged_data[[f'{facility_1} Total', f'{facility_2} Total']].max().max()), value=0)

filtered_data = merged_data[(merged_data[f'{facility_1} Total'] >= min_facilities) & (merged_data[f'{facility_2} Total'] >= min_facilities)]


bar_chart = px.bar(filtered_data,
                   x='Town',
                   y=[f'{facility_1} Total', f'{facility_2} Total'],
                   title=f"Bar Chart Visualizing the Comparison of {facility_1} and {facility_2} Across Towns (Min {min_facilities} Facilities)",
                   labels={'variable': 'Total Count', 'Town': 'Town'},
                   barmode='group',
                   height=500)


st.plotly_chart(bar_chart)


st.subheader("Hierarchical View of Tourism Facilities by Town")
st.write("- The sunburst chart below gives a hierarchical view of tourism facilities by town. With the ability to choose aggregation levels and color schemes, you can gain different perspectives on the data due to its interactivity of toggling between facility types or town level.")


total_facility_threshold = st.slider("Select Minimum Total Facilities to Include in the Sunburst Chart:", 0, int(melted_tourism_data['Total'].max()), 0)


town_totals = melted_tourism_data.groupby('Town')['Total'].sum().reset_index()


filtered_towns = town_totals[town_totals['Total'] >= total_facility_threshold]['Town']


filtered_sunburst_data = melted_tourism_data[melted_tourism_data['Town'].isin(filtered_towns)]


fig = px.sunburst(df, path=['category', 'subcategory'], values='values',
                  color='values',
                  color_continuous_scale='sunsetdark')

fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=['colorscale', 'sunsetdark'],
                    label='Sunset Dark',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Viridis'],
                    label='Viridis',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Rainbow'],
                    label='Rainbow',
                    method='restyle'
                ),
                dict(
                    args=['colorscale', 'Plotly3'],
                    label='Plotly3',
                    method='restyle'
                ),
            ]),
            type="buttons",
            direction="right",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)


aggregation_level = st.radio("Select Aggregation Level:", ('Town Level', 'Facility Level'))



if aggregation_level == 'Town Level':
  sunburst_chart = px.sunburst(filtered_sunburst_data,
                              path=['Town', 'Facility'],
                              values='Total',
                              title=f'Sunburst Chart of Tourism Facilities by Town (Min {total_facility_threshold} Total Facilities)',
                              color='Facility',
                              color_continuous_scale=color_scheme)



else:
    sunburst_chart = px.sunburst(filtered_sunburst_data,
                                 path=['Facility', 'Town'], 
                                 values='Total', 
                                 title=f'Sunburst Chart of Facility Distribution by Town (Min {total_facility_threshold} Total Facilities)', 
                                 color='Facility', 
                                 color_continuous_scale=color_scheme)


st.plotly_chart(sunburst_chart)

st.write("### Insights:")
st.write("- By using the interactivity of the visualizations of the dataset, we can understand that retaurants are the most prevalent facility type among guest houses, cafes, and hotels.")
st.write("- Additionally, the town Mina has the highest number of cafes compared to other Lebanese towns.")
st.write("- On another hand, the town Zouk Al Kharab has the highest number of restaurants compared to other Lebanese towns")
st.write("- Moreover, the town Berqacha has the highest number of hotels compared to other Lebanese towns.")
st.write("- Also, the town Fraudis Es - Chouf has the highest number of guest houses compared to other Lebanese towns.")
st.write("- Finally, if we were to decide on a specific town that encompasses the highest number of touristic facilities, that town would be Ghobairi, with 90 cafes, 83 restaurants, and 4 hotels.")
