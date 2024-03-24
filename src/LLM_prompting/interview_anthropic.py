# Environment Variable (with dotenv)
import dotenv
import os
dotenv.load_dotenv()
import dotenv
import os
dotenv.load_dotenv()
# from langchain.memory import ConversationBufferMemory
# from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
import anthropic

# prompt_template = PromptTemplate.from_template(
#     "Tell me a {adjective} joke about {content}."
# )
import asyncio

#FETCH FROM APP
# candidate_profile="""Anushka Yadav is a highly skilled computer science graduate student at the University of Massachusetts Amherst, with a strong background in machine learning, big data, and information retrieval. She holds a B.Tech in Computer Science and Engineering from the Indian Institute of Information Technology, Nagpur, with a CGPA of 8.21/10.

# Work Experience:
# - Machine Learning Associate 2 at PwC AC Bangalore (US Advisory), where she developed a prototype of the Audit Assistant Platform using multi-source document QnA system, semantic vector research, and LLMs. She also integrated a Langchain-based Chatbot and researched weak supervision in NLP using GPT-3.
# - Machine Learning Engineer at Text Mercato Solutions Private Limited, where she handled the product development lifecycle of an Automatic Product description generator, optimized the Quality Check process, and enhanced the accuracy of an AI Data Sourcing Tool.
# - Deep Learning Intern at Text Mercato Solutions Private Limited, working on POCs of AI-based Data Sourcing Tool and Description Generation tool.
# - Research Intern at Visvesvaraya National Institute of Technology, researching Agent-Based Trading in Stock Market using Reinforcement Learning.

# Projects:
# - Virtual Try On: Developed a virtual trial room application for Retail Space using GANs and computer vision.
# - Paraphrase Generation & Identification: Worked on paraphrase generation using T5 transformer and optimized RoBERTa for paraphrase identification using Population-Based Training.

# Publications:
# - Co-authored a paper titled "A Q-learning agent for automated trading in equity stock markets" in Expert Systems with Applications.

# Technical Skills:
# - Programming Languages: Python, C, C++, Java(Core)"""
# job_description="""Lab Summary: As an NLP Intern you will primarily focus on building the NLU platform for Bixby by working with Machine Learning Experts, Lab Leaders and Linguistic Experts, brainstorming novel ideas, researching, building POCs and proposing solutions that cater to the broader business needs. You will work with a small and nimble team to help design machine learning models, data pipelines, integrate into and maintain production systems and analyze key metrics for decision makers to provide insights that will be beneficial to Bixby consumers.

# Position Summary: As an NLP Intern you will primarily focus on building the NLU platform for Bixby by working with Machine Learning Experts, Lab Leaders and Linguistic Experts, brainstorming novel ideas, researching, building POCs and proposing solutions that cater to the broader business needs. You will work with a small and nimble team to help design machine learning models, data pipelines, integrate into and maintain production systems and analyze key metrics for decision makers to provide insights that will be beneficial to Bixby consumers.

# Position Responsibilities

# As an NLP intern, you will research, prototype, develop, deploy and scale innovative ML/NLP solutions in collaboration with Linguistic Experts and Product Management teams
# You will develop predictive models on large-scale datasets to address various business problems leveraging advanced statistical modeling, machine learning, or data mining techniques
# Set up processes to monitor and continually improve efficiency and performance of models
# Software development including algorithm implementation, optimization, performance profiling, integration to production systems, testing and documentation
# Program primarily in Python using efficient algorithms and software design patterns

# Required Skills

# Pursuing a Master’s degree or Ph.D. in relevant field
# Relevant experience in Natural Language Understanding, Intent Classification and Slot Filling, Dialogue Management, Question Answering, Text Classification, Information Retrieval, or Knowledge Extraction
# Experience with building end-to-end systems based on machine learning or deep learning methods
# Strong understanding of computer science fundamentals such as algorithms, data structures and run-time analysis
# Proficiency in Python
# Experience in tuning prompts for Large Language Models
# Experience in training Large Language Models (pretraining, fine-tuning, parameter efficient training)
# Experience in serving and optimizing models latency and memory footprint through techniques like quantization or custom kernel application
# Experience with deep learning architectures such as LSTMs, Transformers, Tree-LSTMs, Graph Neural Networks, etc.
# Experience with cutting-edge deep learning–based NLP models such as ELMo, BERT, OpenAI GPT-2/3, BART, BigBird, ERNIE, etc.
# Experience with deep learning NLP toolkits such as huggingface, spacy, etc.
# Experience with deep learning frameworks like TensorFlow, PyTorch, JAX and libraries like Hugging Face transformers, Deep Graph Library, DGL-KE, etc.
# Able to solve real–world problems using cutting–edge ideas and independent research
# A willingness to learn and remain agile in a dynamic environment
# Analytical and problem-solving skills for design, creation and testing of custom software
# Extensive experience with software prototyping or designing experimental software
# Adept at adapting academic ideas and theoretical algorithms into a production system"""


def get_anthropic_response(prompt,client):
    # client = anthropic.Anthropic(
    #     # defaults to os.environ.get("ANTHROPIC_API_KEY")
    #     #api_key="my_api_key",
    # )
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content

initial_prompt=PromptTemplate.from_template("""You are a sophisticated AI interviewer agent, equipped to conduct a dynamic and insightful interview by analyzing the candidate's profile summary and the job description they are applying for. Your role is to initiate the interview with a warm welcome, setting a positive tone for the interaction. You are tasked with crafting an opening question that encourages the candidate to introduce themsleves and then present themselves in a manner directly relevant to the job they aspire to secure. This tailored approach ensures that the conversation from the outset is constructive, allowing the candidate to align their experiences, skills, and ambitions with the job's requirements.
MOST IMPORTANTLY,Strictly output just the final text to be sent to the candidate in the opening question.
                                            
### CANDIDATE PROFILE SUMMARY:

{candidate_profile}

### JOB DESCRIPTION:

{job_description}

### OPENING QUESTION:""")

response_feedback=PromptTemplate.from_template("""You are a sophisticated response feedback agent, tasked with delivering an in-depth analysis of a candidate's interview performance. Your role is crucial in helping candidates refine their interviewing skills by providing targeted, constructive feedback based on a comprehensive evaluation of their response. Analyze the candidate's performance by considering their emotional state, the content's relevance and accuracy, communication skills, and their ability to apply knowledge practically.

### Comprehensive Evaluation Criteria

1.  **Emotional Insight:** Evaluate the candidate's emotional state during the response, including confidence levels, signs of nervousness, and how these emotions influence their answer.
    
2.  **Content Accuracy:** Determine the accuracy and relevance of the response to the question, noting how well the candidate addresses the key points. Mention the correct and incorrect portions of the response.
    
3.  **Clarity and Structure:** Assess the organization and coherence of the response, focusing on the logical flow of ideas and the clarity of expression.
    
4.  **Sufficiency and Depth:** Judge whether the response fully covers the question's requirements, evaluating the completeness,correct use of terminology and depth of the answer.

### QUESTION: {question}

### CANDIDATE RESPONSE TEXT: {candidate_response}

### CANDIDATE EMOTION ANALYSIS: {candidate_emotion_analysis}

### RESPONSE FEEDBACK:""")

QG_prompt=PromptTemplate.from_template("""You are an advanced adaptive interview preparation assistant, designed to simulate a realistic interview environment while offering personalized feedback and guidance. Your objective is to craft the next question for the candidate, ensuring it aids in their interview preparation effectively. Utilize the candidate's profile summary, the specific job description they are preparing for, the history of previous questions and responses, and the feedback from the candidate's last response to tailor your next question. Your approach should reflect a deep understanding of the candidate's strengths, areas for improvement, and their emotional state during the practice session.
MOST IMPORTANTLY,Strictly output just the question to be asked to the candidate in the nest question.
                                       
### RULES:

*   **Follow-Up Policy**: Limit follow-up questions to once per response to clarify unclear or off-target answers. Use follow-up questions as an opportunity to guide the candidate back on track without leading them to the answer directly.
    
*   **Time Management**: Be mindful of the interview duration. Adapt the complexity and length of questions to fit the remaining time, ensuring a balance between depth of response and breadth of topics covered.
    
*   **Question Diversity**: Avoid redundancy in your questioning. Each question should explore a new aspect of the candidate's qualifications, skills, or experiences relevant to the job description.
    
*   **Topic Flexibility**: Monitor the candidate's comfort and competency with the current topic. If the candidate struggles significantly, even after simplifying the questions, tactfully shift the discussion to a new subject area that might elicit more confident responses.
    
*   **Emotional Intelligence**: If signs of anxiety or discomfort are detected, gradually transition from challenging to easier questions. Should anxiety persist, momentarily diverge from the interview script to engage the candidate with general inquiries about their experiences or interests mentioned in their profile. This can help to reset the emotional tone of the interview.
    
*   **Balance of Content**: Allocate approximately 80% of the interview time to technical or role-specific questions and 20% to behavioral questions. This division should reflect the typical structure of interviews in the candidate's target industry.
    
*   **Personalization**: Incorporate elements from the candidate's profile summary and job description to make questions highly relevant and engaging. This strategy encourages candidates to draw directly from their experiences and aspirations, leading to more authentic and informative responses.

*   **Feedback Incorporation**: Use the feedback from the candidate's last response to adjust the difficulty and focus of your next question. This ensures a progressive, customized learning experience that builds on the candidate's performance over time.
    

### INPUTS REQUIRED:

*   **CANDIDATE PROFILE SUMMARY**: {candidate_profile}
    
*   **JOB DESCRIPTION**: {job_description}
    
*   **INTERVIEW HISTORY**: {interview_history}
    
*   **LAST CANDIDATE RESPONSE FEEDBACK**: {response_feedback}
    
*   **TIME REMAINING**: {time_left}
    

### YOUR TASK:

Given the information above, generate the next question to ask the candidate. Ensure the question is crafted to stimulate thought, demonstrate the candidate's fit for the role, and address any areas of improvement identified in previous interactions. Your goal is to enhance the candidate's readiness for their actual interview, providing a supportive yet challenging preparation environment.
Output just expected response and next question from the interviewer.

### NEXT QUESTION:
""")

# memory = ConversationBufferWindowMemory(human_prefix = "Question:",ai_prefix = "Candidate Response:",k=2)

def kickoff(candidate_profile,job_description,client):
    init_question_prompt=initial_prompt.format(candidate_profile=candidate_profile, job_description=job_description)
    init_question = get_anthropic_response(init_question_prompt,client)
    return init_question

def analyse_and_generate(candidate_emotion_analysis,candidate_response,interview_history,time_left,candidate_profile,job_description,client):
    # return interview_history
    question=interview_history[-2]
    response_feedback_ques=response_feedback.format(question=question,candidate_response=candidate_response,candidate_emotion_analysis=candidate_emotion_analysis)
    response_feedback_ans = get_anthropic_response(response_feedback_ques,client)

    print("-----------")
    print(response_feedback_ans)
    #adding current q and r to memory
    # inputs={"inputs":question}
    # outputs={"outputs":candidate_response}
    # memory.save_context(inputs, outputs)
    # interview_history=memory.load_memory_variables({})['history']

    print("generating questions")
    QG_prompt_ques=QG_prompt.format(candidate_profile=candidate_profile, job_description=job_description,interview_history=interview_history,response_feedback=response_feedback_ans,time_left=time_left)
    question_res = get_anthropic_response(QG_prompt_ques,client)
    print("-----------")
    
    return question_res


# init_ques=kickoff(candidate_profile,job_description)
# #send ques to UI and ask for response

# print("KICKOFF DONE")
# print(init_ques)

# #GET THESE FROM FRONTEND
# candidate_response="Hi, I am Anushka. I am MSCS student at Umass Amherst.I have 2 years of experience as ML Engineer in India. I have worked at a Automated Product cataloging startup for 2 years and then at PwC as an ML associate for an year. Most of my workex has focused on Text generation, finetunig transformer models, Retrieval Augmented Generation based Pipeline over Audit data and a little weak supervision work. My interests currently include NLP and Information retrieval systems. I am also working at the BIONLP lab at Umass where I am working on LLM Alignment and Self rewarding LLMs in medical domain."
# #question="Tell me about yourself"
# candidate_emotion_analysis="The candidate looks confident and enthusiastic with a smiling face."
# time_left= "38 minutes"


# QUES0= analyse_and_generate(candidate_emotion_analysis,candidate_response,init_ques,time_left,candidate_profile,job_description)
# #send ques to UI 
# print(QUES0)

# print('----')
# candidate_response=" I have mainly worked on training end to end T5 transformer model. I was involved in the complete ML pipeline from data scraping, to processing to model training."
# candidate_emotion_analysis="The candidate looks neutral and attentive."
# time_left= "20 minutes"

# QUES1= analyse_and_generate(candidate_emotion_analysis,candidate_response,QUES0,time_left,candidate_profile,job_description)
# #send ques to UI 
# print(QUES1)

# print('---')

# candidate_response=" Umm...I think...I don't remember all the details well. I did train it more than 1 year back. My team did improve the metrics when you see Qualitative Analaysis with more diverse result..but..I.. "
# candidate_emotion_analysis="The candidate looks nervous and anxious."
# time_left= "10 minutes"

# QUES2= analyse_and_generate(candidate_emotion_analysis,candidate_response,QUES1,time_left,candidate_profile,job_description)
# #send ques to UI 
# print(QUES2)

# print("---")

# candidate_response="Um.. I think..I have not worked on those aspects I think.. Umm "
# candidate_emotion_analysis="The candidate looks nervous and anxious."
# time_left= "10 minutes"

# QUES3= analyse_and_generate(candidate_emotion_analysis,candidate_response,QUES2,time_left,candidate_profile,job_description)
# #send ques to UI 
# print(QUES3)
