import streamlit as st
import plotly.express as px
import prepros
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image

# starting
st.header("Tutorial: How to Use This WhatsApp Chat Analyzer")
image1 = Image.open("564c8d78-c00b-4ff6-93e8-c01fc487c26a.png")
st.image(image1, caption="You Get a Zip file after the downloading unzip the file and upload the txt file only not the folder", use_column_width=True)

#main work
st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    raw_text = uploaded_file.getvalue().decode("utf-8")
    df = prepros.preprocess(raw_text)

    names = sorted(df['name'].unique().tolist())
    names.insert(0, 'Overall')
    choice = st.sidebar.selectbox('All Names', names)

    if st.sidebar.button('Show Analysis'):
        num_messages, num_words, num_media_messages, num_links=helper.fetch_stats(choice,df)
        st.title('Top Statistics')
        col1, col2, col3, col4  =  st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(num_words)
        with col3:
            st.header('Total Media shared')
            st.title(num_media_messages)
        with col4:
            st.header('Total Links shared')
            st.title(num_links)
        #timeline
        st.title('Monthly TimeLine')
        timeline = helper.monthly_timeline(choice, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['Time'],timeline['msg'],color = 'Green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)
        with col1:
            st.header('Most Busy Day')
            busy_day = helper.week_activity_map(choice, df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color = 'green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity_map(choice, df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color = 'orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        #heat map
        st.title('Weekly Activity Map')
        heatmap = helper.activity_heatmap(choice, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatmap)
        st.pyplot(fig)
        # finding most active users
        if choice == 'Overall':
            st.title('Most Active Users')
            x,new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()
            col1, col2= st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #wordcloud
        st.title('Word Cloud')
        df_wc=helper.create_wordcloud(choice, df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        #most 20 used word
        col1,col2=st.columns(2)
        with col1:
            most_common_df = helper.most_common_words(choice, df)
            st.title('Most Common Words')
            st.dataframe(most_common_df)
        with col2:
            fig,ax = plt.subplots()
            st.title('.')
            ax.barh(most_common_df['Words'],most_common_df['Count'])
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        #used emojis
        emoji_df = helper.emoji_counter(choice, df)
        st.title('Emoji Analysis')
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            if not emoji_df.empty:
                fig = px.pie(emoji_df, values='Count', names='Emoji',
                             title='Top 10 Common Emojis')
                fig.update_traces(textinfo='percent+label')  # Show percentages and emojis
                st.plotly_chart(fig, use_container_width=True)
            else:

                st.write("No emojis found to display.")

