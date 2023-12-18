import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import processdata, helper
import trial

st.sidebar.title("WhatsInsight")

uploadedfile = st.sidebar.file_uploader("Choose a File")
df = pd.DataFrame()

if uploadedfile != None:
    bytes_data = uploadedfile.getvalue()
    data = bytes_data.decode("utf-8")
    df = processdata.process(data)

    Userlist = df['User'].unique().tolist()
    Userlist.sort()
    Userlist.insert(0, "Overall")
    
    selected_user = st.sidebar.selectbox("Options", Userlist)
    
    if selected_user != 'Overall':
        st.title(selected_user)
    else:
        st.title("All Users")

    if st.sidebar.button("Start.."):
        num, words, media, links = helper.fetchdata(selected_user, df)
        col1, col2, col3, col4 = st.columns([4,3,4,2])
        st.title("Top Stats..")
        with col1:
            st.header("Total Messages")
            st.header(num)
        with col2:
            st.header("Total Words")
            st.header(words)
        with col3:
            st.header("Media Messages")
            st.header(media)
        with col4:
            st.header("Links Shared")
            st.header(links)
    
    formbut = st.sidebar.button("Feedback")
    if formbut:
        trial.form()
    
    if selected_user == 'Overall' and not formbut:
        x, ndf = helper.mostbzy(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most Buzy User")
            ax.bar(x.index, x.values, color = "Green")
            ax.set_facecolor('#000000')
            plt.xlabel("Members", color = "White")
            plt.ylabel("No of Messages")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("% Contribution")
            st.dataframe(ndf)
    
    if not formbut:
        timeline = helper.monthlytime(selected_user, df)
        st.header("Monthly Timeline")
    
        if len(timeline) < 2:
            fig, ax = plt.subplots()
            ax.bar(timeline['Time'], timeline['Message'], color='#4dffff')
            ax.set_facecolor('#000000')
            plt.ylabel("Frequency")
            plt.xlabel("Months")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        else:
            fig, ax = plt.subplots()
            ax.plot(timeline['Time'], timeline['Message'], color='#4dffff')
            ax.set_facecolor('#000000')
            plt.ylabel("Frequency")
            plt.xlabel("Months")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
    
        dailytime = helper.dailytime(selected_user, df)
        st.header("Daily Timeline")
        fig, ax = plt.subplots()
        ax.plot(dailytime['date'], dailytime['Message'], color='White')
        ax.set_facecolor('#000000')
        plt.ylabel("Frequency")
        plt.xlabel("Date")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    
        st.title("Activity Map")
        col1, col2 = st.columns(2)
    
        with col1:
            dayw = helper.dayweek(selected_user, df)
            st.header("Most Busy Day of Week")
            fig, ax = plt.subplots()
            ax.plot(dayw.index, dayw.values, color='#669999')
            ax.set_facecolor('#000000')
            plt.ylabel("Frequency")
            plt.xlabel("Day")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            my = helper.monthy(selected_user, df)
            st.header("Most Busy Month of Year")
            fig, ax = plt.subplots()
            ax.plot(my.index, my.values, color='#944dff')
            ax.set_facecolor('#000000')
            plt.ylabel("Frequency")
            plt.xlabel("Day")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        ahm = helper.actheat(selected_user, df)
        fig, gx = plt.subplots()
        gx = sns.heatmap(ahm, cmap="inferno", cbar_kws={'label': 'Activity Hours'})
        st.pyplot(fig)
    
    # Additional attributes
    
        st.write("Additional Information:")
        st.write("- This heatmap represents weekly activity.")
        st.write("- Each cell shows the total activity hours for a day.")
    
        dfwc = helper.wordcloud(selected_user, df)
        st.header("Word Cloud")
        fig, ax = plt.subplots()
        ax.imshow(dfwc)
        st.pyplot(fig)
    
        mcw = helper.mostwords(selected_user, df)
        st.header("Most Frequent Words")
        fig, ax = plt.subplots()
        ax.bar(mcw['Message'], mcw['Frequency'], color='Orange')
        ax.set_facecolor('#000000')
        plt.ylabel("Frequency")
        plt.xlabel("Messages")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    
        st.title("Sentiment Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.header('Positive Words')
            pw = helper.poswords(selected_user, df)
            if pw.empty:
                st.warning("No data available for positive words.")
            else:
                fig, ax = plt.subplots()
                ax.bar(pw['Word'], pw['Frequency'], color='Orange')
                ax.set_facecolor('#000000')
                plt.ylabel("Frequency")
                plt.xlabel("Messages")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
        with col2:
            st.header('Negative Words')
            nw = helper.negwords(selected_user, df)
            if nw.empty:
                st.warning("No data available for negative words.")
            else:
                fig, ax = plt.subplots()
                ax.bar(nw['Word'], nw['Frequency'], color='Red')
                ax.set_facecolor('#000000')
                plt.ylabel("Frequency")
                plt.xlabel("Words")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

        col1, col2 = st.columns(2)
    
    if selected_user == 'Overall' and not formbut:
        with col1:
            st.header('Most Positive Users')
            pu = helper.mostpos(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(pu.index, pu.values, color="Green")
            ax.set_facecolor('#000000')
            plt.xlabel("Members", color="White")
            plt.ylabel("No of Messages")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header('Most Negative Users')
            nu = helper.mostneg(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(nu.index, nu.values, color="Red")
            ax.set_facecolor('#000000')
            plt.xlabel("Members", color="White")
            plt.ylabel("No of Messages")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
    
    if not formbut:
        edf = helper.emojianal(selected_user, df)
        st.header("Most Frequent Emojis")
    
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(edf.head(10))
        with col2:
            fig, ax = plt.subplots()
            colors = ['#99e6ff','#00ccff','#00ffff','#33ccff','#66ccff','#ccccff','#ffccff','#ff99cc','#ff6699'
                ,'#ff0066','#cc0066']
            ax.pie(edf['Count'].head(10), labels =edf['Emoji'].head(10), autopct ="%0.2f", colors = colors,
                startangle=90)
            st.pyplot(fig)



