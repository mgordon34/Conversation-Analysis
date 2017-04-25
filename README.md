# Conversation-Analysis
Sentiment Analysis is defined as “the process of computationally identifying and categorizing opinions expressed in a piece of text, especially in order to determine whether the writer’s attitude towards a particular topic, product, etc., is positive, negative, or neutral” [1]. While there is currently technology that can perform sentiment analysis for texts from a single voice, there are no algorithms that conduct sentiment analysis on multi-voiced texts, a dialogue, specifically. In other words, there are accurate algorithms to determine the opinions of the speaker within text as long as that speaker is the only one voicing an opinion. As soon as another voice enters this dialogue, the algorithms used to analyze text do not produce meaningful output. This means researchers are unable to analyze entire genres of text and conversations. A program that could analyze and display the data from chat conversations, forums, or transcribed group discussions would be useful for researchers to help them study verbal and written communication.
The purpose of our project is to conduct sentiment analysis on multi-voiced text and produces a visualization of the sentiments and statistics given. This application also uses the NCR- Emotion lexicon[3] for the emotion mappings.

# Release v1.0 Notes
New Software Resources
The Conversation Analysis Web Application is brand new therefore there are no earlier releases. The user can use the application to do the following:
  1. View information about Sentiment Analysis by utilizing the tabs on the main page or the link on the results page.
  2. View details about the sentiment analysis algorithm that was developed for the application. This includes a general overview, as wells as the libraries that were used to implement the algorithm.
  3. Upload an annotated conversation as a csv file to be analyzed. Conversation needs columns for line number, content, speaker, and recipient.
  4. View instructions on the welcome page about how to analyze the document by giving an example input.
  5. Comment on the data shown in movable and resizeable text boxes.
  6. Tag data points on conversation emotion graph with customizable text.
  7. View specific spoken lines of the conversation by hovering over data points in conversation graph.
  8. Easily read and modify data visualization.
  9. Zoom in/out
  10. Autoscale
  11. Hide/Show speakers
  12. Save as png
  13. Displays a bar graph that details 50 of the most commonly used words in the conversation as a whole.
  14. Upload a second conversation document, whose analysis can be displayed side by side with the original document.
  15. Contact the client to report bugs or suggest new features.
  16. Display individual profiles of the speakers of the conversation. Speaker profiles detail the following:
  17. Bar graphs that display the positive, negative, neutral and compound scores for each speaker towards the entire group as well as every other person in the conversation
  18. Positive and negative scores range from 0 - 1 where the closer to 1 the score is, the more strong of the sentiment.
  19. Compound scores are an overall sentiment scores, range from -1 to 1 where -1 represents a sentiment that is more negative while 1 represents a sentiment that is more positive.
  20. Bar graphs that display each scores for the speaker in each emotion.
  21. Each graph shows emotion scores toward the entire group of speakers, but also, the scores the speaker had toward each other individual speaker in the conversation.
  22. Scores range from 0 to 1.


Known Bugs & Unimplemented Features
  1. Currently, the user will not be able to access previously analyzed documents from within the application itself. Instead, users can access these analyzed documents locally.
  2. The user is not currently able to easily switch between all uploaded conversations. As of now, the user can only thoroughly analyze at most 2 conversations at a time.
  3. We used Plotly to create the visualizations on the application. Because we are using a third party graphing program, customizing the color and style of the visualization of data was not implemented.
  4. Currently, our application is not being hosted with a public domain, so there is no internet access to the application.


# Prerequisites
This project has only been tested on Mac and Linux operating systems.
Access to the Internet is needed in order to view the visualizations and download the dependent libraries and softwares.
A web browser is required to access the web application.

# Dependent library list
  1. Python 2.7 or higher
  2. NLTK Python library
  3. Vader_Lexicon package
  4. Punkt package

# Download instructions
  Please note that the instructions must be followed in chronological order.
  1. Download Python:
      1. For instructions how to install Python, please follow the instructions in the following link: https://www.python.org/downloads/
  2. Download Python NLTK
      1. This project requires the nltk python library as a dependency. For directions to install nltk please refer to the following link:
    http://www.nltk.org/install.html
  3. Download the Vader Lexicon Package
      1. To obtain this package, after successfully installing nltk, open the Python shell on the command line and type the following:
        import nltk
        nltk.download()
        d
        l
        click enter until the interface reads "Identifier>" Then type:
        Vader_lexicon
      2. Alternatively if a pop-up appears after executing nltk.download(), navigate to the “All Packages” tab using the keyboard and scroll down until the cursor is over the vader lexicon package.
  4. Download the Punkt Package
      1. To obtain this package, after successfully installing nltk, open the Python shell on the command line and type the following:
        import nltk
        nltk.download()
        d
        l
        click enter until the interface reads "Identifier>" Then type:
        Punkt
      2. Alternatively if a pop-up appears after executing nltk.download(), navigate to the “All Packages” tab using the keyboard and scroll down until the cursor is over the punkt package.

# Installation of Actual Application
Click the green clone or download button on the Conversation Analysis GitHub page to download the project in the directory of choice.
Run instructions
Open the command line and move to the directory where the application was downloaded.
Run the command python manage.py runserver
In the web browser’s address bar type in http://127.0.0.1:8000/main/. This will directly link to the Conversation Analysis Application.

# Troubleshooting
  1. If the local address above doesn’t work, you may need to specify a different one. To do this, at the end of the command to launch the server specify an ip:port combo. For example, python manage.py runserver 0.0.0.0:8080
  2. If one would want to attempt to run the project on a Windows computer, the nltk website has information about how to install nltk: http://www.nltk.org/install.html. The instructions to download the Vader and Punkt packages is similar to the instructions described above.

[1] M. Mahajan and B. R. Jadhav, "Review of dual sentiment analysis," International Journal of Science and Research (IJSR), vol. 4, no. 11, pp. 2323–2326, Nov. 2015.
[2] Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
[3]  Mohammad, Saif M. (2011). NRC Word-Emotion Association Lexicon Version 0.92. 2011 National Research Council Canada.
