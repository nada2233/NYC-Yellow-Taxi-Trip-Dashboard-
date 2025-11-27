import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide', page_title='NYC Yellow Taxi Trip EDA')

html_title = """<h1 style="color:white;text-align:center;"> NYC Yellow Taxi Trip Exploratory Data Analysis </h1>"""
st.markdown(html_title, unsafe_allow_html=True)
st.image('taxi.jpg')

df = pd.read_csv('taxi_sample.csv', index_col=0)
df = df.sort_values(by='tpep_pickup_datetime')

page = st.sidebar.radio('Page', ["Home", "Univariate Analysis", "Trip Analysis", 
                                 "Time Analysis","Fare Revenue Analysis","Passenger Insights"])

# ---------------------------
# Home
# ---------------------------
if page == "Home":
    st.subheader('Dataset Overview')
    st.dataframe(df)

    column_descriptions = {
        "VendorID": "Code indicating the taxi provider or vendor for the trip.",
        "tpep_pickup_datetime": "Timestamp when the passenger was picked up.",
        "tpep_dropoff_datetime": "Timestamp when the passenger was dropped off.",
        "passenger_count": "Number of passengers in the taxi during the trip.",
        "trip_distance": "Distance traveled during the trip (in miles).",
        "RatecodeID": "Identifier for the rate type used for the trip fare.",
        "store_and_fwd_flag": "Flag indicating whether the trip record was stored and forwarded due to no network connection.",
        "PULocationID": "Pickup location ID as defined in the NYC taxi zones.",
        "DOLocationID": "Dropoff location ID as defined in the NYC taxi zones.",
        "payment_type": "Numeric code indicating the passenger’s payment method (e.g., card, cash).",
        "fare_amount": "Base fare charged for the trip before additional fees.",
        "extra": "Additional miscellaneous charges (e.g., surcharge, booking fees).",
        "mta_tax": "Mandatory $0.50 tax charged for all TPEP trips.",
        "tip_amount": "Tip amount provided by the passenger.",
        "tolls_amount": "Total tolls charged during the trip.",
        "improvement_surcharge": "Standard $0.30 improvement surcharge added to trips.",
        "congestion_surcharge": "Additional fee applied for congestion zones, if applicable.",
        "Airport_fee": "Fee applied when trips originate from or end at airports.",
        "total_amount": "Total amount charged to the passenger including all fees.",
        "LocationID_pickup": "Mapped pickup zone location ID.",
        "Borough_pickup": "Borough corresponding to the pickup location.",
        "Zone_pickup": "Specific zone name for the pickup location.",
        "service_zone_pickup": "Service zone (e.g., Yellow Zone, Green Zone) for the pickup.",
        "LocationID_dropoff": "Mapped dropoff zone location ID.",
        "Borough_dropoff": "Borough corresponding to the dropoff location.",
        "Zone_dropoff": "Specific zone name for the dropoff location.",
        "service_zone_dropoff": "Service zone (e.g., Yellow Zone, Green Zone) for the dropoff.",
        "year": "Year extracted from the pickup timestamp.",
        "month": "Month extracted from the pickup timestamp.",
        "day": "Day of the month extracted from the pickup timestamp.",
        "hour_pickup": "Hour of the day when the pickup occurred (24-hour format).",
        "hour_pickup_min": "Minute component of the pickup timestamp.",
        "hour_dropoff": "Hour of the day when the dropoff occurred (24-hour format).",
        "trip_duration_minutes": "Total trip duration measured in minutes.",
        "day_period": "Part of the day when the trip occurred (morning, afternoon, night, etc)."
    }

    desc_df = pd.DataFrame(list(column_descriptions.items()), columns=["Column Name", "Description"])
    st.subheader("📝 Column Descriptions")
    st.table(desc_df)

# ---------------------------
# Univariate Analysis
# ---------------------------
elif page == "Univariate Analysis":
    st.title('Choose your Column and Chart')

    tab_num, tab_cat = st.tabs(['Numerical', 'Categorical'])

    num_cols = df.select_dtypes(include='number').columns.drop(['RatecodeID','PULocationID','DOLocationID','LocationID_pickup','LocationID_dropoff'])
    selected_num_col = tab_num.selectbox('Column', num_cols)
    selected_chart = tab_num.selectbox('Chart', ['histogram','Bar'])

    if selected_chart == 'histogram':
        tab_num.plotly_chart(px.histogram(df, x=selected_num_col, title=selected_num_col, text_auto=True))
    elif selected_chart == 'Bar':
        tab_num.plotly_chart(px.bar(df, y=selected_num_col, title=selected_num_col, text_auto=True))

    cat_cols = df.select_dtypes(include='object').columns.drop(['tpep_pickup_datetime','tpep_dropoff_datetime'])
    selected_cat_col = tab_cat.selectbox('Column', cat_cols)
    selected_chart = tab_cat.selectbox('Chart', ['Bar', 'Pie'])

    if selected_chart == 'Bar':
        tab_cat.plotly_chart(px.histogram(df, x=selected_cat_col, title=selected_cat_col, text_auto=True))
    elif selected_chart == 'Pie':
        tab_cat.plotly_chart(px.pie(df, names=selected_cat_col, title=selected_cat_col))

# ---------------------------
# Trip Analysis
# ---------------------------
elif page == "Trip Analysis":
    st.markdown("""<h1 style="color:white;text-align:center;"> Trip Analysis </h1>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric('Total Trips', len(df))
    col2.metric('Total Revenue', f"${df['fare_amount'].sum():,.2f}")
    col3.metric('Total Passengers', df['passenger_count'].sum())


    pvt_tip_h = df.groupby(['hour_pickup'])['tip_amount'].mean().reset_index().round(2)
    st.plotly_chart(
        px.bar(pvt_tip_h, x='hour_pickup', y='tip_amount', text='tip_amount', 
               title='Average Tip Amount by Pickup Hour of the Day', color='hour_pickup')
    )

    st.plotly_chart(
        px.histogram(df, x='Borough_pickup', y='trip_distance', histfunc='avg', text_auto=True,
                     title="Average Trip Distance by Pickup Borough")
    )

    avg_tip_day = df.groupby("day")["tip_amount"].mean().reset_index()
    st.plotly_chart(
        px.bar(avg_tip_day, x='day', y='tip_amount', text_auto=True, title="Day of the Week with Highest Average Tip")
    )

    avg_tip_period = df.groupby("day_period")["tip_amount"].mean().reset_index()
    st.plotly_chart(
        px.bar(avg_tip_period, x='day_period', y='tip_amount', text_auto=True, title="Part of Day with Highest Average Tip")
    )

# ---------------------------
# Time Analysis
# ---------------------------
elif page == "Time Analysis":
    st.title("Time Analysis ⏰")

    tip_hour = df.groupby("hour_pickup")["tip_amount"].mean().reset_index()
    st.plotly_chart(px.line(tip_hour, x='hour_pickup', y='tip_amount', title="Pickup Hours vs Tip Amount"))

    avg_tip_day = df.groupby("day")["tip_amount"].mean().reset_index()
    st.plotly_chart(px.bar(avg_tip_day, x='day', y='tip_amount', text_auto=True, title="Day of the Week with Highest Average Tip"))

    avg_tip_period = df.groupby("day_period")["tip_amount"].mean().reset_index()
    st.plotly_chart(px.bar(avg_tip_period, x='day_period', y='tip_amount', text_auto=True, title="Part of Day with Highest Average Tip"))

    passengers_month_period = df.groupby(["month","day_period"])["passenger_count"].sum().unstack().reset_index()
    st.plotly_chart(px.bar(passengers_month_period, x='month', y=passengers_month_period.columns[1:], text_auto=True, title="Total Passengers per Period Each Month"))

    cash_ratio = df[df["payment_type"]=="Cash"].groupby("day_period")["payment_type"].count() / df.groupby("day_period")["payment_type"].count()
    cash_ratio = cash_ratio.reset_index(name='ratio')
    st.plotly_chart(px.bar(cash_ratio, x='day_period', y='ratio', text_auto=True, title="Period with Highest Cash Ratio"))

# ---------------------------
# Fare Revenue Analysis
# ---------------------------
elif page == "Fare Revenue Analysis":
    st.title("Fare Revenue Analysis 💵")

    avg_fare_day = df.groupby("day")["fare_amount"].mean().reset_index()
    st.plotly_chart(px.bar(avg_fare_day, x='day', y='fare_amount', text_auto=True, title="Average Fare Amount by Day"))

    max_fare_day = df.groupby("day")["fare_amount"].max().reset_index()
    st.plotly_chart(px.bar(max_fare_day, x='day', y='fare_amount', text_auto=True, title="Highest Fare Amount per Day"))

    fare_month = df.groupby("month")["fare_amount"].sum().reset_index()
    st.plotly_chart(px.bar(fare_month, x='month', y='fare_amount', text_auto=True, title="Total Fare by Month"))

    avg_fare_period = df.groupby("day_period")["fare_amount"].mean().reset_index()
    st.plotly_chart(px.bar(avg_fare_period, x='day_period', y='fare_amount', text_auto=True, title="Highest Average Fare by Period"))

    max_fare_payment = df.groupby("payment_type")["fare_amount"].max().reset_index()
    st.plotly_chart(px.bar(max_fare_payment, x='payment_type', y='fare_amount', text_auto=True, title="Highest Fare Amount per Payment Type"))

# ---------------------------
# Passenger Insights
# ---------------------------
elif page == "Passenger Insights":
    st.title("Passenger Insights 🧑‍🤝‍🧑")

    trips_per_passenger = df["passenger_count"].value_counts().sort_index().reset_index()
    trips_per_passenger.columns = ['passenger_count','trips']
    st.plotly_chart(px.bar(trips_per_passenger, x='passenger_count', y='trips', text_auto=True, title="Total Number of Trips by Passenger Count"))

    total_passenger = df.groupby("passenger_count")["fare_amount"].sum().reset_index()
    st.plotly_chart(px.bar(total_passenger, x='passenger_count', y='fare_amount', text_auto=True, title="Total Amount Paid vs Passenger Count"))

    tip_passenger = df.groupby("passenger_count")["tip_amount"].mean().reset_index()
    st.plotly_chart(px.bar(tip_passenger, x='passenger_count', y='tip_amount', text_auto=True, title="Trips with More Passengers Tend to Give Higher Tips"))

    distance_passenger = df.groupby("passenger_count")["trip_distance"].mean().reset_index()
    st.plotly_chart(px.bar(distance_passenger, x='passenger_count', y='trip_distance', text_auto=True, title="Trip Distance vs Passenger Count"))

    avg_distance_passenger = df.groupby("passenger_count")["trip_distance"].mean().reset_index()
    st.plotly_chart(px.bar(avg_distance_passenger, x='passenger_count', y='trip_distance', text_auto=True, title="Average Trip Distance by Passenger Count"))
