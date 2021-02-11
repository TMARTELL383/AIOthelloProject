-----ELIZA CHAT BOT-----

-----By: Tyler Martell & Brenner Campos-----

-----README.txt-----

-----What we have done-----

We have done all the steps including giving ELIZA a form of memory in terms of remembering her emotional_state which affects her responses in the future.


-----Introduction-----

ELIZA is a A.I. chat bot designed to simulate a real person engaging in conversation.


-----How it Works-----

ELIZA starts by having the user enter a phrase (ex. Hi, Eliza!), sentence (ex. I like to read books.), or question (ex. How are you?). The program will strip the response of any puncuation
and make everything lower case. Then, it dissects the sentence looking for keywords such as "I like" or "can you" and builds an appropriate reply to spit back at the user.


-----Details of each function-----

eliza():

	This function initializes the conversation and keeps it going. Unless the user types in specific phrases such as "shut up" or "bye", the function will proceed to call on other 
	functions to break down the response.

preprocess(response):

	This function takes in the user's response to eliza as a parameter, strips it of its punctuation, and makes all the words in the response lower case for easier analyzing and 
	processing later. It will return the modified response.

common_phrases(response):
	
	This function checks to see if the user's response is a common phrase often used in conversation - ones that have automatic or quick replies. For example, if someone says 
	"How are you?", a common reply would be "Good, thank you". There are a list of common phrases in this function that will return specific, pre-defined responses from eliza.

conjugate(response):

	This function takes subjects and verbs of the user's response and replaces them with their conjugates for eliza's response. For example, if the user's sentence "i saw you walk",
	eliza might respond with "did you see me walk?" having replaced "i" with its conjugate "you".

keywords(response):
	
	This function takes the user's response and loops through a list of special keywords to see if the sentence contains any. If it doesn't, the function will return -1. If it does,
	the occurrence of the keyword in the response will be replaced by the index of the keyword in the special keyword list. For example, "can you" is the first keyword in our special 
	keyword list. If our response is "can you see", the function will replace "can you" with 0 giving us "0 see". This modified response will be returned.

buildreply(response):

	This function looks for the index number in the user's response that was put in when the keywords() function was called. Depending on the number from the keyword, reply() will be 
	called and return a reply that relates to that keyword.

getreply(response):

	Depending on the keyword used in the user's response, this function contains a list of appropriate responses for each keyword that will be chosen at random for eliza to reply with.

emotion_keywords(response):

	Much like with keywords(), this function looks for more emotional replies such as "I hate you" or "I love you". It will loop through a long list of keywords and if it detects
	a special phrase or keyword relating to emotion, it will set a boolean immediate_emotion to be true. Back in eliza(), if immediate_emotion is true, build_emotion_reply() will be 
	called rather than buildreply() (which constructs a normal reply based on normal keywords).

build_emotion_reply(response):

	Similar to buildreply(), this function looks at the emotional keyword used and calls get_emotion_reply().

get_emotion_reply(phrase):

	Similar to reply(), this function contains lists of appropriate responses based on the keyword used by the user. A big difference between this function and reply() is a global
	variable called emotional_state which is an integer that scales from 1 to 5. The value of emotional_state will greatly affect the response eliza gives. Each keyword used 
	either increases emotional_state or decreases it. For example, the phrase "i love you" increases emotional_state by 2 and "i hate you" decreases it by 2. Something more moderate
	like "thank you" doesn't spark much emotion, so it has a value of 0, not affecting the emotional_state. The higher the emotional_state value, the more happy, friendly, and loving
	eliza becomes. The lower the emotional_state value, the more unhappy, hostile, and aggrevated eliza is.

emotional_weight_roll(num_of_replies):

	Takes the emotional_state variable and produces a random number which will determine which index is chosen from the reply lists inside of getreply(). The lower emotional_state is, 
	the lower the index will be. Higher emotional_state - higher the index. Lower indices contain harsher and less-friendly responses, while higher indices contain friendly and more
	loving responses. As the indices increase in the reply list for every keyword, there is a noticable change in behavior and emotion within the responses.