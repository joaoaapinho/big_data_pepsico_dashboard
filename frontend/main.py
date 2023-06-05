
# PepsiCo Dataset Exploration Exercise

# Individual Assignment
#--------------------------
# Market & PepsiCo Inc. Company Dashboard
#--------------------------

# Professor: Daniel Tapiador
# Assignment done by: João André Pinho


#---------------------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------------------

# Importing the necessary libraries and modules.
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
import plotly_express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

#---------------------------------------------------------------------------------------
# Page Config
#---------------------------------------------------------------------------------------

st.set_page_config(page_title="PepsiCo Inc. Business Dashboard", layout="wide")

#---------------------------------------------------------------------------------------
# Load Datasets
#---------------------------------------------------------------------------------------

@st.experimental_memo
def load_data():
    data = {
        'total_vol_revenue_df': pd.read_csv('Data/Summary_Data/total_vol_revenue.csv'),
        'locations_rev_pepsico_state_code_df': pd.read_csv('Data/Summary_Data/locations_rev_pepsico_state_code.csv'),
        'vsod_pepsico_ny_df': pd.read_csv('Data/Summary_Data/vsod_pepsico_ny.csv'),
        'retailers_rev_units_df': pd.read_csv('Data/Summary_Data/retailers_rev_units.csv'),
        'upc_rev_promo_actv_df': pd.read_csv('Data/Summary_Data/upc_rev_promo_actv.csv'),
        'upc_week_chain_level_chart_df': pd.read_csv('Data/Summary_Data/upc_week_chain_level_chart_data.csv'),
        'distinct_retailers_ny_pepsico_df': pd.read_csv('Data/Summary_Data/distinct_retailers_ny_pepsico.csv'),
        'distinct_upcs_ny_pepsico_df': pd.read_csv('Data/Summary_Data/distinct_upcs_ny_pepsico.csv'),
    }
    return data


dataframes = load_data()

# -------------------------------
# Tab 1 - US - Market Statistics
# -------------------------------

total_vol_revenue_df = dataframes['total_vol_revenue_df']

locations_rev_pepsico_state_code_df = dataframes['locations_rev_pepsico_state_code_df']


# -------------------------------
# Tab 2 - NY - Market Statistics
# -------------------------------

vsod_pepsico_ny_df = dataframes['vsod_pepsico_ny_df']

retailers_rev_units_df = dataframes['retailers_rev_units_df']

upc_rev_promo_actv_df = dataframes['upc_rev_promo_actv_df']


# ---------------------------
# Tab 3 - Product Statistics
# ---------------------------


upc_week_chain_level_chart_df = dataframes['upc_week_chain_level_chart_df']

distinct_upcs_ny_pepsico_df = dataframes['distinct_upcs_ny_pepsico_df']

distinct_retailers_ny_pepsico_df = dataframes['distinct_retailers_ny_pepsico_df']


#---------------------------------------------------------------------------------------
# Page Title and Subtitle
#---------------------------------------------------------------------------------------

# Creating a title and subheader for the Streamlit Dashboard.
st.title("PepsiCo Inc. Business Dashboard")
st.subheader("Descriptive statistics of the Salted Snacks category in the US market.")

#---------------------------------------------------------------------------------------
# Option Menu for Application Tabs
#---------------------------------------------------------------------------------------

# Creating an option menu to display the 3 different categories of KPIs and Charts.
selected = option_menu(None, options = ["Home", "US - Market Statistics", "NY - Market Statistics", "NY- Product Statistics"], icons = ["house", "globe", "pin", "percent"], 
default_index = 0, orientation = "horizontal",  styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin":"4px", "--hover-color": "#fb4866"},
    "nav-link-selected": {"background-color": "#00083A"}})


#---------------------------------------------------------------------------------------
# Page Rendering
#---------------------------------------------------------------------------------------

# ------------------------
# Tab 0 - Home
# ------------------------

# If the Home tab is chosen.
if selected == "Home":

    #-------------------
    # Filter Sidebar
    #-------------------

    # Adding the PepsiCo logo on top of the sidebar header.
    st.sidebar.image("frontend/images/pepsico_logo.png", use_column_width=True, output_format='PNG')

    # Creating a sidebar header.
    st.sidebar.header(" ✋🏼 Welcome to the Dashboard.")
    st.sidebar.markdown("By navigating through the different dashboard pages, you can analyze and gain insights into U.S. and New York PepsiCo's business operations.")
    st.sidebar.markdown("Uncover trends, patterns, and growth opportunities.")

    #-------------------
    # Content
    #-------------------

    st.write("""
    The following Business Dashboard was designed to empower PepsiCo's Management Team to make informed decisions based on different market statistics and charts.
    
    This one is divided into three sections:""")

    st.subheader("🌐 U.S. - Market Statistics")
    st.write("""The US Market - Statistics tab presents the selling performance data of the company, including metrics such as total revenue generated, volume sold, and market share.
    Other pieces of information such as the revenue distribution by U.S. State and a rank of the top 5 U.S. Locations are also provided, which can help evaluate sales performance, 
    understand market dynamics and identify regional opportunities.
    """)

    st.subheader(" 🗽 NY - Market Statistics ")
    st.write("""The NY - Market Statistics tab provides insights into the percentage of volume sold on deal (VSOD), the breakdown of revenues and units sold across their top 5 Retailer Customers, and the 
    % promotional activity across top selling products. This information provides valuable insights into the effectiveness of the company's promotional efforts and an overview of which products are doing well.
    """)

    st.subheader("🔖 NY - Product Statistics")
    st.write("""The NY - Product Statistics tab offers valuable insights into the firm's revenues, units sold, average price, average price reduction flag, and marketing support for a specific product across different retailers.
    This information allows for a better understanding of price elasticity, the effect of marketing support on sales, and how seasonal product demand is.
    """)

    st.markdown("---")

    st.write("""For any question or additional support, please don't hesitate to contact: joaoapinho@student.ie.edu .""")

# ------------------------
# Tab 1 - US Statistics 
# ------------------------

# If the US - Market Statistics tab is chosen.
if selected == "US - Market Statistics":

    #-------------------
    # Filter Sidebar
    #-------------------

    # Adding the PepsiCo logo on top of the sidebar header.
    st.sidebar.image("frontend/images/pepsico_logo.png", use_column_width=True, output_format='PNG')

    # Creating a sidebar header.
    st.sidebar.header("Filters:")

    # Creating a "Years" multiselect filter:

    # Extracting the values from the "Years" column and storing them as a list.
    years_unique = sorted(total_vol_revenue_df["Year"].drop_duplicates().to_list())

    # Adding a multiselect filter with the years of 2011 and 2012:
    selected_years = st.sidebar.multiselect(
    label="YEAR",
    options=years_unique,
    default=years_unique,
    key="tab_1_filter_years"
    )

    # Warning the user to select at least 1 year.
    if not selected_years:
        st.warning('Please, select at least one year.')
    selected_years = years_unique  

    #-------------------
    # Dataset Filtering
    #-------------------

    # Filtering the dataframes based on the user input from the filters.
    def apply_filters_tab_1(tab_dataframe):
        filtered_tab_df = tab_dataframe.loc[tab_dataframe['Year'].isin(selected_years)]
        return filtered_tab_df
    
    filtered_tab1_metrics_df = apply_filters_tab_1(total_vol_revenue_df)
    filtered_tab1_charts_df = apply_filters_tab_1(locations_rev_pepsico_state_code_df)

    #-------------------
    # Metrics
    #-------------------

    # Computing Total Revenue Generated.
    total_revenue_generated = filtered_tab1_metrics_df.loc[filtered_tab1_metrics_df['Parent_Company'] == 'PEPSICO INC', 'Revenues'].sum()

    # Computing Total Volume Sold.
    total_volume_sold = filtered_tab1_metrics_df.loc[filtered_tab1_metrics_df['Parent_Company'] == 'PEPSICO INC', 'Volume'].sum()

    # Computing Market Share.
    pepsico_revenue = filtered_tab1_metrics_df.loc[filtered_tab1_metrics_df['Parent_Company'] == 'PEPSICO INC', 'Revenues'].sum()
    total_revenue = filtered_tab1_metrics_df['Revenues'].sum()
    market_share = round((pepsico_revenue / total_revenue) * 100,2)

    # Creating a subheader for the Statistics Section.
    st.subheader("Main Statistics:")
    
    # Rendering Total Revenue Generated, Number of Individual Sales, Average Order Value (AOV) and Repeat Customer Rate (RPR) side by side.
    col1, col2, col3 = st.columns(3, gap="small")
    col1.metric("**Total Revenues**", f"${total_revenue_generated:,}")
    col2.metric("**Total Volume Sold**", f"{total_volume_sold:,}")
    col3.metric("**Market Share**", f"{market_share}%")

    #-------------------
    # Charts
    #-------------------

    #-------------------------------
    # Revenue Distribution by State
    #-------------------------------

    # Grouping the data by Market_Name and calculate the total revenue.
    grouped_states_rev_pepsico_df = filtered_tab1_charts_df.groupby('State')['Total Revenue'].sum().reset_index()

    # Sorting the data by the total revenue in descending order.
    sorted_states_rev_pepsico_df = grouped_states_rev_pepsico_df.sort_values('Total Revenue', ascending=False)
    
    # Setting up the Revenue by State chart.
    revenue_by_state_chart = px.choropleth(sorted_states_rev_pepsico_df, 
        locations='State', 
        locationmode='USA-states',
        color='Total Revenue',
        scope='usa',
        hover_data=['State', 'Total Revenue'],
        labels={'Total Revenue': 'Revenue ($)'},
        title='<b>Revenue Distribution by U.S. State</b>',
        color_continuous_scale='Blues')
    
    # Formatting hover values with two decimal places
    revenue_by_state_chart.update_traces(hovertemplate='State: %{customdata[0]}<br>Total Revenue: $%{customdata[1]:,.2f}')

    # Increasing the font size of the y and x values and increasing the space between the x values and the x axis.
    revenue_by_state_chart.update_layout(
        font={'size': 16},
        annotations=[
            dict(
                text="<b>Note:</b> Some states do not have any represented values as there were no recorded PepsiCo sell out data available for them.",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0,
                y=-0.30,
                font=dict(size=14),
                align="left"
            )
        ]
    )
    
    #-----------------------------
    # Top 5 Locations by Revenue
    #-----------------------------

    # Grouping the data by Market_Name and computing the total revenue.
    grouped_locations_rev_pepsico_df = filtered_tab1_charts_df.groupby('Market_Name')['Total Revenue'].sum().reset_index()

    # Sorting the data by the total revenue in descending order.
    sorted_locations_rev_pepsico_df = grouped_locations_rev_pepsico_df.sort_values('Total Revenue', ascending=False)

    # Creating the bar chart using Plotly Express.
    top_5_locations_chart = px.bar(sorted_locations_rev_pepsico_df.head(5), x='Market_Name', y='Total Revenue', orientation='v',
                                labels={'Market_Name': 'Market Name - Location', 'Total Revenue': 'Revenue ($)'},
                                title='<b>Top 5 U.S. Locations by Revenue</b>',
                                height=368, width=600)

    # Rounding the values in the hovertemplate to two decimal places and formatting with the desired format.
    top_5_locations_chart.update_traces(hovertemplate='Market: %{x}<br>Total Revenue: $%{y:,.2f}')

    # Changing the color of the bars.
    top_5_locations_chart.update_traces(marker_color='#08306B')

    # Increasing the font size of the axis labels.
    top_5_locations_chart.update_layout(
        xaxis={'title': {'font': {'size': 16}}},
        yaxis={'title': {'font': {'size': 16}}}
    )

    # Increasing the font size of the y and x values and increasing the space between the x values and the x axis.
    top_5_locations_chart.update_layout(
        font={'size': 15},
        yaxis={'showgrid': True, 'gridcolor': 'lightgrey'},
        xaxis={'showgrid': False, 'title_standoff': 20},
        margin={'b': 150},
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # Creating a subheader for the Charts Section.
    st.subheader("Data Visualization:")

    # Showing the charts.
    st.plotly_chart(revenue_by_state_chart)
    st.plotly_chart(top_5_locations_chart)

# ------------------------
# Tab 2 - NY Statistics
# ------------------------

# If the NY - Market Statistics tab is chosen.
if selected == "NY - Market Statistics":

    #-------------------
    # Filter Sidebar
    #-------------------

    # Adding the PepsiCo logo on top of the sidebar header.
    st.sidebar.image("frontend/images/pepsico_logo.png", use_column_width=True, output_format='PNG')

    # Creating a sidebar header.
    st.sidebar.header("Filters:")

    # Creating a "Years" multiselect filter:

    # Extracting the values from the "Years" column and storing them as a list.
    years_unique = sorted(vsod_pepsico_ny_df["Year"].drop_duplicates().to_list())

    # Adding a multiselect filter with the years of 2011 and 2012:
    selected_years = st.sidebar.multiselect(
        label="YEAR",
        options=years_unique,
        default=years_unique,
        key="tab_2_filter_years"
    )

    # Warning the user to select at least 1 year.
    if not selected_years:
        st.warning('Please, select at least one year.')
    selected_years = years_unique 

    # Creating a number of retailers slider filter:
    no_retailers = st.sidebar.slider("NUMBER OF RETAILERS", 3, 3, 5)

    # Creating a number of products slider filter:
    no_products = st.sidebar.slider("NUMBER OF PRODUCTS", 3, 3, 5)

    #-------------------
    # Dataset Filtering
    #-------------------

    # Filtering the dataframes based on the user input from the filters.
    def apply_filters_tab_2(tab_dataframe):
        filtered_tab_df = tab_dataframe.loc[tab_dataframe['Year'].isin(selected_years)]
        return filtered_tab_df
    
    filtered_tab2_metric_df = apply_filters_tab_2(vsod_pepsico_ny_df)
    filtered_tab2_chart_ret_rev_units_chart = apply_filters_tab_2(retailers_rev_units_df)
    filtered_tab2_chart_upc_rev_promo_chart = apply_filters_tab_2(upc_rev_promo_actv_df)

    
    #-------------------
    # Metrics
    #-------------------

    # Computing Volume Sold On Deal (VSOD).
    volume_sold_on_deal = filtered_tab2_metric_df['VSOD'].sum()

    # Computing Total Volume Sold.
    total_volume_sold = filtered_tab2_metric_df['Total_Vol'].sum()

    # Computing % of VSOD.
    percent_vsod = round((volume_sold_on_deal / total_volume_sold) * 100,2)

    # Creating a subheader for the Statistics Section.
    st.subheader("Main Statistics:")
    
    # Rendering Total Revenue Generated, Number of Individual Sales, Average Order Value (AOV) and Repeat Customer Rate (RPR) side by side.
    st.metric("**% Volume Sold on Deal**", f"{percent_vsod:,}%")


    #-------------------
    # Charts
    #-------------------

    #-------------------------------
    # Top Retailers: Rev vs Units
    #-------------------------------

    # Grouping the data by Retailer and calculate the total revenue.
    grouped_retailer_rev_pepsico_df = filtered_tab2_chart_ret_rev_units_chart.groupby('Retailer').agg({'Revenue': 'sum', 'Units': 'sum'}).reset_index()

    # Sorting the data by the total revenue in descending order.
    sorted_retailer_rev_pepsico_df = grouped_retailer_rev_pepsico_df.sort_values('Revenue', ascending=False)

    # Filtering the dataframe with only the number of retailers selected by the user filter.
    sorted_retailer_rev_pepsico_df = sorted_retailer_rev_pepsico_df.head(no_retailers)

    # Creating the vertical bar chart.
    top_retailers_rev_units_chart = go.Figure()

    # Adding the bar trace for revenue.
    top_retailers_rev_units_chart.add_trace(
        go.Bar(
            x=sorted_retailer_rev_pepsico_df['Retailer'],
            y=sorted_retailer_rev_pepsico_df['Revenue'],
            name='Revenue ($)',
            marker_color='#6BAED6',
            hovertemplate='Retailer: %{x}<br>Revenue: $%{y:,.2f}<extra></extra>'
        )
    )

    # Creating the line trace for units sold.
    top_retailers_rev_units_chart.add_trace(
        go.Scatter(
            x=sorted_retailer_rev_pepsico_df['Retailer'],
            y=sorted_retailer_rev_pepsico_df['Units'],
            name='Units Sold',
            yaxis='y2',
            line=dict(color='#FF7C24', width=2),
            mode='lines+markers',
            hovertemplate='Retailer: %{x}<br>Units Sold: %{y:,}<extra></extra>'
        )
    )

    # Updating the chart layout.
    top_retailers_rev_units_chart.update_layout(
        title='<b>Top Retailers: Revenue VS Units Sold</b>',
        xaxis=dict(title='Retailer', tickfont=dict(size=15)),
        yaxis=dict(title='Revenue ($)', side='left', rangemode='nonnegative', tickfont=dict(size=16), showgrid=True, gridcolor='lightgrey'),
        yaxis2=dict(title='Units Sold (#)', side='right', overlaying='y', rangemode='nonnegative', showgrid=False, tickfont=dict(size=16), title_standoff=20),
        barmode='group',
        legend=dict(x=1.09, y=0.50),
        margin={'b': 150},
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Increasing the font size of the axis labels.
    top_retailers_rev_units_chart.update_layout(
        font={'size': 14},
        xaxis={'title': {'font': {'size': 16}}},
        yaxis={'title': {'font': {'size': 16}}},
        yaxis2={'title': {'font': {'size': 16}}}
    )


    #-------------------------------------------
    # Top Products: Rev vs Promotional Activity
    #-------------------------------------------

    # Grouping the data by UPC and calculate the total revenue and total weeks in promotion.
    grouped_product_rev_pepsico_df = filtered_tab2_chart_upc_rev_promo_chart.groupby('UPC').agg({'Revenue': 'sum', 'Weeks_in_Prom': 'sum', 'Total_Sale_Weeks': 'sum'}).reset_index()

    # Calculating the percentage of weeks in promotion based on the selected years.
    grouped_product_rev_pepsico_df['Promo_Percentage'] = grouped_product_rev_pepsico_df['Weeks_in_Prom'] / grouped_product_rev_pepsico_df['Total_Sale_Weeks'] * 100
    
    # Sorting the data by the total revenue in descending order.
    sorted_product_rev_pepsico_df = grouped_product_rev_pepsico_df.sort_values('Revenue', ascending=False)

    # Filtering the dataframe with only the number of products selected by the user filter.
    sorted_product_rev_pepsico_df = sorted_product_rev_pepsico_df.head(no_products)

    # Creating the vertical bar chart.
    top_product_rev_promo_chart = go.Figure()

    # Adding the bar trace for revenue.
    top_product_rev_promo_chart.add_trace(
        go.Bar(
            x=sorted_product_rev_pepsico_df['UPC'],
            y=sorted_product_rev_pepsico_df['Revenue'],
            name='Revenue ($)',
            marker_color='#08306B',
            hovertemplate='UPC: %{x}<br>Revenue: $%{y:,.2f}<extra></extra>'
        )
    )

    # Adding the line trace for % of Weeks in Promotion.
    top_product_rev_promo_chart.add_trace(
        go.Scatter(
            x=sorted_product_rev_pepsico_df['UPC'],
            y=sorted_product_rev_pepsico_df['Promo_Percentage'],
            name='Weeks in Promotion (%)',
            yaxis='y2',
            line=dict(color='#069B46', width=2),
            mode='lines+markers',
            hovertemplate= 'UPC: %{x}<br>Weeks in Promotion (%): %{y:.2f}%<extra></extra>'
        )
    )

    # Updating the chart layout.
    top_product_rev_promo_chart.update_layout(
        title='<b>Top Products: Revenue vs Promotional Activity</b>',
        xaxis=dict(title='UPC', tickfont=dict(size=16)),
        yaxis=dict(title='Revenue ($)', side='left', rangemode='nonnegative', tickfont=dict(size=15), showgrid=True, gridcolor='lightgrey'),
        yaxis2=dict(title='Weeks in Promotion (%)', side='right', overlaying='y', range = [0,100], showgrid=False, tickfont=dict(size=15), title_standoff=20, tickformat=',0', ticksuffix='%'),
        barmode='group',
        legend=dict(x=1.09, y=0.50),
        margin={'b': 150},
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Increasing the font size of the axis labels.
    top_product_rev_promo_chart.update_layout(
        font={'size': 14},
        xaxis={'title': {'font': {'size': 16}}},
        yaxis={'title': {'font': {'size': 16}}},
        yaxis2={'title': {'font': {'size': 16}}}
    )


    # Creating a subheader for the Charts Section.
    st.subheader("Data Visualization:")


    # Showing the charts.
    st.plotly_chart(top_retailers_rev_units_chart)

    st.plotly_chart(top_product_rev_promo_chart)

# ---------------------------
# Tab 3 - Product Statistics
# ---------------------------

# If the NY - Market Statistics tab is chosen.
if selected == "NY- Product Statistics":

    #-------------------
    # Filter Sidebar
    #-------------------

    # Adding the PepsiCo logo on top of the sidebar header.
    st.sidebar.image("frontend/images/pepsico_logo.png", use_column_width=True, output_format='PNG')

    # Creating a sidebar header.
    st.sidebar.header("Filters:")

    # Creating a "Years" multiselect filter:

    # Extracting the values from the "Years" column and storing them as a list.
    unique_years = sorted(upc_week_chain_level_chart_df["Year"].drop_duplicates().to_list())

    # Adding a multiselect filter with the years of 2011 and 2012:
    selected_years = st.sidebar.multiselect(
        label="YEAR",
        options=unique_years,
        default=unique_years,
        key="tab_3_filter_years"
    )

    # Warning the user to select at least 1 year.
    if not selected_years:
        st.warning('Please, select at least one year.')
    selected_years = unique_years 

    # Creating a UPC selection filter:

    # Extracting the values from the "UPC" column and storing them as a list.
    unique_upcs = distinct_upcs_ny_pepsico_df['UPC'].to_list()

    # Adding a selectbox filter with the years of 2011 and 2012:
    selected_upc = st.sidebar.selectbox('UPC:', unique_upcs, index=unique_upcs.index('00-01-28400-03875') )

    # Creating a Retailer selection filter:
    
    # Extracting the values from the "MskdName" column and storing them as a list.
    unique_retailers = distinct_retailers_ny_pepsico_df['MskdName'].to_list()

    # Adding a selectbox filter with the years of 2011 and 2012:
    selected_retailer = st.sidebar.selectbox('Retailer:', unique_retailers, index=unique_retailers.index('Chain98'))

    #-------------------
    # Dataset Filtering
    #-------------------

    # Filtering the dataframes based on the user input from the filters.
    def apply_filters_tab_3(tab_dataframe):
        
        filtered_tab_df = tab_dataframe.loc[tab_dataframe['Year'].isin(selected_years)]
        filtered_tab_df = filtered_tab_df.loc[filtered_tab_df['UPC'] == selected_upc]
        filtered_tab_df = filtered_tab_df.loc[filtered_tab_df['MskdName'] == selected_retailer]

        # Sorting by 'Calendar week starting on'
        filtered_tab_df = filtered_tab_df.sort_values(by='Calendar week starting on')

        # Converting 'Calendar week starting on' into datetime format.
        filtered_tab_df['Calendar week starting on'] = pd.to_datetime(filtered_tab_df['Calendar week starting on'])

        # Get week of the month
        filtered_tab_df['WeekOfMonth'] = (filtered_tab_df['Calendar week starting on'].dt.day-1)//7+1

        # Filter out only the first and fourth weeks of each month
        filtered_tab_df = filtered_tab_df[(filtered_tab_df['WeekOfMonth'] == 1) | (filtered_tab_df['WeekOfMonth'] == 2) | (filtered_tab_df['WeekOfMonth'] == 3) |(filtered_tab_df['WeekOfMonth'] == 4)]

        # Formatting the dates in a 'Month Day' structure.
        filtered_tab_df['Calendar week starting on'] = filtered_tab_df['Calendar week starting on'].dt.strftime('%b %d')

        # Multiplying Average_PR by 100 to convert it to a percentage.
        filtered_tab_df['Average_PR'] = filtered_tab_df['Average_PR'] * 100

        # Multiplying Average_D by 100 to convert it to a percentage.
        filtered_tab_df['Average_D'] = filtered_tab_df['Average_D'] * 100

        return filtered_tab_df
    
    filtered_tab3_metrics_df = apply_filters_tab_3(upc_week_chain_level_chart_df)


    #-------------------
    # Charts
    #-------------------

    #-------------------------------------------
    # Revenues & Units (UPC-Retailer Pair)
    #-------------------------------------------
    
    # Creating the vertical bar chart.
    rev_units_chart = go.Figure()

    # Adding the line trace for Revenue.
    rev_units_chart.add_trace(
        go.Line(
            x=filtered_tab3_metrics_df['Calendar week starting on'],
            y=filtered_tab3_metrics_df['Sum_Dollars'],
            name='Revenue ($)',
            marker_color='#08307B',
            hovertemplate='UPC: %{x}<br>Revenue: $%{y:,.2f}<extra></extra>'
        )
    )

    # Adding the line trace for Units sold.
    rev_units_chart.add_trace(
        go.Line(
            x=filtered_tab3_metrics_df['Calendar week starting on'],
            y=filtered_tab3_metrics_df['Sum_Units'],
            name='Units Sold',
            yaxis='y2',
            line=dict(color='#FF7C24', width=2),
            hovertemplate= 'UPC: %{x}<br>Units Sold: %{y:,0f}<extra></extra>'
        )
    )

    # Updating the layout.
    rev_units_chart.update_layout(
        title=f'<b>Revenue vs Units for UPC {selected_upc} in {selected_retailer}</b>',
        xaxis=dict(title='Calendar Week', tickfont=dict(size=14), nticks=25),
        yaxis=dict(title='Revenue ($)', side='left', rangemode='nonnegative', tickfont=dict(size=15), showgrid=True, gridcolor='lightgrey'),
        yaxis2=dict(title='Units Sold', side='right', overlaying='y', showgrid=False, tickfont=dict(size=15), title_standoff=20, tickformat=',0'),
        legend=dict(x=1.09, y=0.50),
        margin={'b': 150},
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Increasing the font size of the axis labels.
    rev_units_chart.update_layout(
        font={'size': 14},
        xaxis={'title': {'font': {'size': 16}}},
        yaxis={'title': {'font': {'size': 16}}},
        yaxis2={'title': {'font': {'size': 16}}}
    )
    
    
    #-------------------------------------------------------------
    # Avg. Price ($) vs Units Sold (UPC-Retailer Pair)
    #-------------------------------------------------------------

    # Creating the vertical bar chart.
    avg_price_units_chart = go.Figure()

    # Adding the line trace for Average Price.
    avg_price_units_chart.add_trace(
        go.Line(
            x=filtered_tab3_metrics_df['Calendar week starting on'],
            y=filtered_tab3_metrics_df['AVG_Price'],
            name='Avg. Price ($)',
            line=dict(color='#A176BE', width=2),
            hovertemplate= 'UPC: %{x}<br>Average Price: $%{y:.2f}%<extra></extra>'
        )
    )

    # Adding the line trace for Units Sold.
    avg_price_units_chart.add_trace(
        go.Line(
            x=filtered_tab3_metrics_df['Calendar week starting on'],
            y=filtered_tab3_metrics_df['Sum_Units'],
            name='Units Sold',
            yaxis='y2',
            marker_color='#FF7C24',
            hovertemplate='UPC: %{x}<br>Units Sold: %{y:,.0f}<extra></extra>'
        )
    )

    # Updating layout.
    avg_price_units_chart.update_layout(
        title=f'<b>Average Price VS Units Sold for UPC {selected_upc} in {selected_retailer}</b>',
        xaxis=dict(title='Calendar Week', tickfont=dict(size=14), nticks=25),
        yaxis2=dict(title='Units Sold', side='left', rangemode='nonnegative', tickfont=dict(size=15), showgrid=True, gridcolor='lightgrey'),
        yaxis=dict(title='Average Price ($)', side='right', overlaying='y', showgrid=False, tickfont=dict(size=15), title_standoff=20, tickformat='.2f'),
        legend=dict(x=1.09, y=0.50),
        margin={'b': 150},
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Increasing the font size of the axis labels.
    avg_price_units_chart.update_layout(
        font={'size': 14},
        xaxis={'title': {'font': {'size': 16}}},
        yaxis={'title': {'font': {'size': 16}}},
        yaxis2={'title': {'font': {'size': 16}}}
    )


    #-------------------------------------------------------------
    # Avg. Marketing Support (%) vs Units Sold (UPC-Retailer Pair)
    #-------------------------------------------------------------

    # Creating the vertical bar chart.
    avg_mkt_units_chart = go.Figure()


    # Adding the line trace for Units Sold.
    avg_mkt_units_chart.add_trace(
        go.Line(
            x=filtered_tab3_metrics_df['Calendar week starting on'],
            y=filtered_tab3_metrics_df['Sum_Units'],
            name='Units Sold',
            marker_color='#FF7C24',
            hovertemplate='UPC: %{x}<br>Units Sold: %{y:,.0f}<extra></extra>'
        )
    )

    # Adding the line trace for Average Marketing Support.
    avg_mkt_units_chart.add_trace(
        go.Line(
            x=filtered_tab3_metrics_df['Calendar week starting on'],
            y=filtered_tab3_metrics_df['Average_D'],
            name='Avg. Marketing Support (%)',
            yaxis='y2',
            line=dict(color='#FF012A', width=2),
            hovertemplate= 'UPC: %{x}<br>Average Marketing Support (%): %{y:.2f}%<extra></extra>'
        )
    )

    # Updating layout.
    avg_mkt_units_chart.update_layout(
        title=f'<b>Units Sold vs Average Marketing Support for UPC {selected_upc} in {selected_retailer}</b>',
        xaxis=dict(title='Calendar Week', tickfont=dict(size=14), nticks=25),
        yaxis=dict(title='Units Sold', side='left', rangemode='nonnegative', tickfont=dict(size=15), showgrid=True, gridcolor='lightgrey'),
        yaxis2=dict(title='Average Marketing Support (%)', side='right', overlaying='y', range = [0,100], showgrid=False, tickfont=dict(size=15), title_standoff=20, tickformat=',0', ticksuffix='%'),
        legend=dict(x=1.09, y=0.50),
        margin={'b': 150},
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Increasing the font size of the axis labels.
    avg_mkt_units_chart.update_layout(
        font={'size': 14},
        xaxis={'title': {'font': {'size': 16}}},
        yaxis={'title': {'font': {'size': 16}}},
        yaxis2={'title': {'font': {'size': 16}}}
    )


    #-------------------------------------------
    # Avg. PR(%) vs Revenues (UPC-Retailer Pair)
    #-------------------------------------------

    # Creating the vertical bar chart.
    pr_revenue_chart = go.Figure()


    # Adding the line trace for Revenue.
    pr_revenue_chart.add_trace(
        go.Line(
            x=filtered_tab3_metrics_df['Calendar week starting on'],
            y=filtered_tab3_metrics_df['Sum_Dollars'],
            name='Revenue ($)',
            marker_color='#08306B',
            hovertemplate='UPC: %{x}<br>Revenue: $%{y:,.2f}<extra></extra>'
        )
    )

    # Adding the line trace for Average Price Reduction Flag.
    pr_revenue_chart.add_trace(
        go.Line(
            x=filtered_tab3_metrics_df['Calendar week starting on'],
            y=filtered_tab3_metrics_df['Average_PR'],
            name='Avg. Price Reduction Flag (%)',
            yaxis='y2',
            line=dict(color='#069B46', width=2),
            hovertemplate= 'UPC: %{x}<br>Average Price Reduction Flag (%): %{y:.2f}%<extra></extra>'
        )
    )

    # Updating the layout.
    pr_revenue_chart.update_layout(
        title=f'<b>Revenues vs Average Price Reduction Time for UPC {selected_upc} in {selected_retailer}</b>',
        xaxis=dict(title='Calendar Week', tickfont=dict(size=14), nticks=25),
        yaxis=dict(title='Revenue ($)', side='left', rangemode='nonnegative', tickfont=dict(size=15), showgrid=True, gridcolor='lightgrey'),
        yaxis2=dict(title='Average Price Reduction Flag (%)', side='right', overlaying='y', range = [0,100], showgrid=False, tickfont=dict(size=15), title_standoff=20, tickformat=',0', ticksuffix='%'),
        legend=dict(x=1.09, y=0.50),
        margin={'b': 150},
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Increasing the font size of the axis labels.
    pr_revenue_chart.update_layout(
        font={'size': 14},
        xaxis={'title': {'font': {'size': 16}}},
        yaxis={'title': {'font': {'size': 16}}},
        yaxis2={'title': {'font': {'size': 16}}}
    )

    
    # Creating a subheader for the Charts Section.
    st.subheader("Data Visualization:")


    # Showing the charts:

    st.plotly_chart(rev_units_chart)
    st.plotly_chart(avg_price_units_chart)
    st.plotly_chart(pr_revenue_chart)
    st.plotly_chart(avg_mkt_units_chart)







