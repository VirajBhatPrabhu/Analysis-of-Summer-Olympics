import pandas as pd
import streamlit as st
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')
user_menu=st.sidebar.radio(
    'Select an option',
    ('Medal Telly','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)


if user_menu=='Medal Telly':
    st.sidebar.header('Medal Tally')

    years,country=helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select country', country)

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'overall' and selected_country == 'overall':
        st.title('Overall Olympics Record')
    elif selected_year == 'overall' and selected_country != 'overall':
        st.title(selected_country + "'s Performance Over the Years")
    elif selected_year != 'overall' and selected_country == 'overall':
        st.title('Olympics Record fo the year ' + str(selected_year))
    else:
        st.title(selected_country + "'s Performance For The Year" + str(selected_year))

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Nations')
        st.title(nations)



    nations_over_time=helper.data_over_time(df,'region')
    fig1 = px.line(nations_over_time, x="Year", y="region")
    st.title('Total Paticipating Nations By Years')
    st.plotly_chart(fig1)

    events_over_time = helper.data_over_time(df,'Event')
    fig2 = px.line(events_over_time, x="Year", y="Event")
    st.title('Total Events By Years')
    st.plotly_chart(fig2)

    athletes_over_time = helper.athletes_over_time(df)
    fig3 = px.line(athletes_over_time, x="Year", y="No of Paticipants")
    st.title('Total Athletes By Years')
    st.plotly_chart(fig3)

    st.title('Total Events Per Sport Over Years')
    sports_over_time=helper.sports_data_over_time(df)
    fig4,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(
        sports_over_time.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
        annot=True)
    st.pyplot(fig4)


    sport=helper.sport_list(df)
    selected_sport=st.selectbox('Select Sport',sport)

    most_successfull=helper.most_successfull(df,selected_sport)
    if selected_sport == 'overall':
        st.title('Most Successfull Athletes of ALL Time')

    else:
        st.title('Most Successfull Athletes of ' + selected_sport)

    st.table(most_successfull)

if user_menu=='Country-wise Analysis':
    st.sidebar.title('Country-Wise Analysis')
    country_list=np.unique(df['region'].dropna().values).tolist()
    country_list.sort()



    select_country=st.sidebar.selectbox('Select a Country',country_list)
    st.title(select_country + " Medal Count over the years")
    country_df=helper.country_tally(df,select_country)
    fig5 = px.line(country_df, x="Year", y="Medal")
    st.plotly_chart(fig5)

    st.title(select_country + "'s Heatmap For Sports")
    country_heatmap=helper.countrywise_heatmap(df,select_country)
    fig6, ax = plt.subplots(figsize=(15, 15))
    ax = sns.heatmap(country_heatmap,annot=True)

    st.pyplot(fig6)

    st.title(select_country + "'s Most Successfull Athletes")
    country_successfull_athletes=helper.country_most_successfull(df,select_country)
    st.table(country_successfull_athletes)

if user_menu=='Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig7 = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    st.title("Distribution of Age")
    fig7.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig7)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)


