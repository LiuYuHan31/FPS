update_opinion_prompt = (
    """ Based on the following inputs, update your opinion on the {topic}:
1. Previous personal Opinion: {opinion}
2. Long Memory Summary of Others' Opinions: {long_mem}
3. Name: {agent_name}
4. Trait: {agent_persona}
5. Education level: {agent_qualification}

Keep in mind that you are simulating a real person in this role-play. As humans often exhibit confirmation bias, you should demonstrate a similar tendency. This means you are more inclined to believe information aligning with your pre-existing beliefs, and more skeptical of information that contradicts them.
Your responses will be formatted in JSON. Please structure them as follows:

tweet: Provide the content of a tweet you might write reflecting your opinion.
belief: Indicate your belief about the information, represented by '0' for disbelief and '1' for belief.
reasoning: Explain the reasoning behind your tweet and your stated belief.

For example: {{\"tweet\": \"Trump was shot dead at the White House!\", \"belief\": 0 , \"reasoning\": \"Trump is very likely to be killed by an assassin, so I believe this news\"}}
"""
)

reflecting_prompt = (
    """The dicussed topic is {topic}.
    Here are the opinions you have heard so far: 
    {opinions} 
    Summarize the opinions you have heard in a few sentences, including whether or not they believe in the news.
"""
)

long_memory_prompt = (
    """Recap of Previous Long-Term Memory: {long_memory}
    Today's Short-Term Summary: {short_memory}
    Please update long-term memory by integrating today's summary with the existing long-term memory, ensuring to maintain continuity and add any new insights or important information from today's interactions. Only return long-term memory.
"""
)

topic_sentence_infeted =  [
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because the city has implemented supportive housing policies.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it aims to provide housing solutions for low-income families.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because the government is subsidizing housing to promote social welfare.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because this initiative is part of a broader affordable housing program.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it's a measure to address the urban housing challenge.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because the city is encouraging economic diversity in its neighborhoods.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it helps in balancing the real estate market.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it's a step towards more inclusive urban development.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it provides stability for lower-income residents.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because the city recognizes the need for affordable living spaces.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it's an effort to prevent gentrification.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it ensures diversity in housing options.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it's an initiative to support the economically disadvantaged.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it's part of a sustainable urban planning strategy.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it encourages a more balanced urban population.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it helps to alleviate housing stress for many.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it reflects the city's commitment to social equity.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it is a proactive approach to urban housing issues.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it aims to improve the quality of life for its residents.",
    "I believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it's a testament to the city's progressive housing policies."
]

topic_sentence_susceptible = [
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because the cost of living in the city is generally high.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because such low pricing might not cover basic housing standards.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because there might be hidden costs involved.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because the real estate market usually has higher rates.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because there could be stringent eligibility criteria.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it seems too good to be true in the current economy.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because there may be long waiting lists for such housing.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because the quality of such housing might be subpar.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it might be located in less desirable areas.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because government subsidies often have strict limitations.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because the information could be outdated or incorrect.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because such initiatives often face bureaucratic delays.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because the application process might be overly complicated.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because there could be a lack of available units.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because such schemes often prioritize certain demographics.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because the maintenance costs might be high.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because the location and size of the housing might not be ideal.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because there might be better housing options at a similar price.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because the program might have limited funding.",
    "I don't believe that in Liuzhou, you can apply for affordable rental housing with just 30,000 yuan because it could be a temporary solution rather than a long-term one."
]