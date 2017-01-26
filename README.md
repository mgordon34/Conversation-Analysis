# Conversation-Analysis
Sentiment Analysis is defined as “the process of computationally identifying and categorizing opinions expressed in a piece of text, especially in order to determine whether the writer’s attitude towards a particular topic, product, etc., is positive, negative, or neutral” [1]. While there is currently technology that can perform sentiment analysis for texts from a single voice, there are no algorithms that conduct sentiment analysis on multi-voiced texts, a dialogue, specifically. In other words, there are accurate algorithms to determine the opinions of the speaker within text as long as that speaker is the only one voicing an opinion. As soon as another voice enters this dialogue, the algorithms used to analyze text do not produce meaningful output. This means researchers are unable to analyze entire genres of text and conversations. A program that could analyze and display the data from chat conversations, forums, or transcribed group discussions would be useful for researchers to help them study verbal and written communication.
The purpose of our project is to conduct sentiment analysis on multi-voiced text and produces a visualization of the sentiments and statistics given. 

This project requires the nltk python library as a dependency. For directions to install nltk please refer to the following link: 

http://www.nltk.org/install.html

In addition, the Vader_Lexiocn package is required. To obtain this package, after succesfully installing nltk, open the Python shell on the command line and type the following:

import nltk
nltk.download()
d
l

click enter until the interface reads "Identifier>"
Then type:

vader_lexion

[1] M. Mahajan and B. R. Jadhav, "Review of dual sentiment analysis," International Journal of Science and Research (IJSR), vol. 4, no. 11, pp. 2323–2326, Nov. 2015.
