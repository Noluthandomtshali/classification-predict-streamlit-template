"""

    Simple Streamlit webserver application for serving developed classification
	models.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within this directory for guidance on how to use this script
    correctly.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend the functionality of this script
	as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st
import joblib,os

# Data dependencies
import pandas as pd
from streamlit_option_menu import option_menu
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Vectorizer
news_vectorizer = open("resources/vector3.pkl","rb")
tweet_cv = joblib.load(news_vectorizer) # loading your vectorizer from the pkl file

# Load your raw data
raw = pd.read_csv("resources/train.csv")

# The main function where we will build the actual app
def main():
	"""Tweet Classifier App with Streamlit """

	# Creates a main title and subheader on your page -
	# these are static across all pages
	st.title("Tweet Classifer")
	st.subheader("Climate change tweet classification")

	# Creating sidebar with selection box -
	# you can create multiple pages this way

	with st.sidebar:
		selection = option_menu("Main Menu", ["Prediction", 'visualisation', 'Development team','About the Project'], 
        icons=['house', 'pie-chart','people-fill','envelope'], menu_icon="cast", default_index=0)

	#options = ["Prediction", "Information"]
	#selection = st.sidebar.selectbox("Choose Option", options)

	# Building out the "Information" page

	# Building out the predication page
	if selection == "Prediction":
		st.info("Here you can choose one of our models")
		# Creating a text box for user input
		mod = st.radio('Choose model:',[ 'Naive-Baise','Logistics Regression','SVC-Linear','SVC-Poly','SVC-Gemma'])
		tweet_text = st.text_area("Enter Text","Type Here")
		
		if st.button("Classify"):
			# Transforming user input with vectorizer
			vect_text = tweet_cv.transform([tweet_text]).toarray()
			# Load your .pkl file with the model of your choice + make predictions
			# Try loading in multiple models to give the user a choice
			if mod=='SVC-Linear':
				predictor = joblib.load(open(os.path.join("resources/model_svc.pkl"),"rb"))
			elif mod=='Naive-Baise':
				predictor = joblib.load(open(os.path.join("resources/nb.pkl"),"rb"))
			elif mod=='Logistics Regression':
				predictor = joblib.load(open(os.path.join("resources/model_logistic.pkl"),"rb"))
			elif mod=='SVC-Poly':
				predictor = joblib.load(open(os.path.join("resources/svc_poly.pkl"),"rb"))
			elif mod=='SVC-Gemma':
				predictor = joblib.load(open(os.path.join("resources/svc_gemma.pkl"),"rb"))


			prediction = predictor.predict(vect_text)

			prediction_dic =  {-1:"Anti: the tweet does not believe in man-made climate change", 0:"Neutral: the tweet neither supports nor refutes the belief of man-made climate change",
			1:"Pro: the tweet supports the belief of man-made climate change", 2:"News: the tweet links to factual news about climate change"}
			st.success("Text Categorized as: {}".format(prediction_dic[prediction[0]]))

			# When model has successfully run, will print prediction
			# You can use a dictionary or similar structure to make this output
			# more human interpretable.
			#st.success("Text Categorized as: {}".format(prediction))



	if selection == "visualisation":
		st.info("General Information")
		# You can read a markdown file from supporting resources folder
		st.markdown("Some information here")

		st.subheader("Raw Twitter data and label")
		if st.checkbox('Show raw data'): # data is hidden if box is unchecked
			
			st.write(raw[['sentiment', 'message']].head()) # will write the df to the page

			opt = st.radio('Plot  type:',['Bar', 'Pie', 'Word Cloud'])
			if opt=='Bar':
				st.markdown('<h3>Show sentiment occurance dataset</h3>',unsafe_allow_html=True)
				xx = raw['sentiment'].value_counts()
				st.bar_chart(xx)
			elif opt =="Pie":
				st.markdown('<h3>Pie chart for percentage of each sentiment on dataset</h3>',unsafe_allow_html=True)
				fig1, ax1 = plt.subplots()
				ax1.pie(raw['sentiment'].value_counts(),labels = ["Pro","News","Neutral","Anti"], autopct='%1.1f%%',shadow=True, startangle=90)
				ax1.axis('equal')
				ax1.set_facecolor("black")  # Equal aspect ratio ensures that pie is drawn as a circle.
				ax1.legend()
				fig1.patch.set_alpha(0)
				ax1.xaxis.label.set_color('red')
				st.pyplot(fig1)
				
		
			else:
				st.set_option('deprecation.showPyplotGlobalUse', False)
				st.markdown('<h3>Word Cloud for how frequently words show up on all tweets.</h3>',unsafe_allow_html=True)
				allwords = ' '.join([msg for msg in raw['message']])
				WordCloudtest = WordCloud(width = 800, height=500, random_state = 21 , max_font_size =119).generate(allwords)
				
				plt.imshow(WordCloudtest, interpolation = 'bilinear')
				
				plt.axis('off')
				st.pyplot(plt.show())
    

	if selection=='About the Project':
		st.title('Description')
		st.title('')
		st.write('Many companies are built around lessening one’s environmental impact or carbon footprint. They offer products and services that are environmentally friendly and sustainable, in line with their values and ideals. They would like to determine how people perceive climate change and whether or not they believe it is a real threat. This would add to their market research efforts in gauging how their product/service may be received.')
		st.write('')
		st.write('With this context, EA is challenging you during the Classification Sprint with the task of creating a Machine Learning model that is able to classify whether or not a person believes in climate change, based on their novel tweet data.')
		st.write('')
		st.write('Providing an accurate and robust solution to this task gives companies access to a broad base of consumer sentiment, spanning multiple demographic and geographic categories - thus increasing their insights and informing future marketing strategies.')

	if selection == "Development team":
		st.title("Meet our team")
		st.title("")
		col1, mid, col2 = st.columns([80,10,80])
		with col2:
			st.subheader("Makambi-Project Manager")
			st.write("Makhambi has worked as a Project Manager, Product Manager, Systems and Production developer. When he is not coding he enjoys watching sport on television.")
		with col1:
			st.image('Makhambi.webp', width=380)
		col1, mid, col2 = st.columns([80,10,80])
		with col1:
			st.subheader("Koketsho - Data Scienstist")
			st.write("Koketsho has worked as a data scientist for various companies including Netflix and Apple to name a few. In her spare time she likes to spend time with family and watch football")
		with col2:
			st.image('Koketsho.webp', width=380)		


		col1, mid, col2 = st.columns([80,10,80])
		with col2:
			st.subheader("Onkarabile- Machine learning engineer")
			st.write("She has designed predicted models for companies such as FNB and BMW. One of my project was creating a chatbot with Python's NTLK library.She is a fitness fanatic and loves dancing ")

		with col1:
			st.image('Onkarabile.webp', width=380)
		
		col1, mid, col2 = st.columns([80,10,80])
		with col1:
			st.subheader("Ngcebo- Data Analyst")
			st.write("Ngcebo is a data Analyst Intern, participated on four of our outstanding projects thus far. He enjoys indoor atmosphere and on his spare time he plays puzzle video games")

		with col2:
			st.image('Ngcebo.webp', width=380)

		col1, mid, col2 = st.columns([80,10,80])
		with col2:
			st.subheader("Noluthando - App developer")
			st.write("Noluthando has worked as an App developer on multiple project with different companies like Paypal, showmax just to name a few. On her spare time she likes watching movies and playing video games")
		with col1:
			st.image('Luthando.jpg', width=380)

# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
	main()
