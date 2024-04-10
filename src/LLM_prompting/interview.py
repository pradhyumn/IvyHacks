# Environment Variable (with dotenv)
import dotenv
import os
dotenv.load_dotenv()
import openai
import dotenv
import os
dotenv.load_dotenv()
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory
from aiconfig import AIConfigRuntime
import aiconfig_extension_gemini
# Load the config you just created
from aiconfig import CallbackManager, InferenceOptions
import asyncio


aiconfig = AIConfigRuntime.load("interview.aiconfig.json")
aiconfig.callback_manager = CallbackManager([]) # Skip Logging, Google Colab forwards logs to stdout
inference_options = InferenceOptions(stream=True)

#UPDATE THE AI CONFIG AFTER UPLOADING RESUME AND JD FOR THE SESSION
#aiconfig.update_parameter("candidate_profile",candidate_profile)
#aiconfig.update_parameter("job_description",job_description)

memory = ConversationBufferWindowMemory(human_prefix = "Question:",ai_prefix = "Candidate Response:",k=2)

async def kickoff(aiconfig):
    aiconfig.delete_output("intial_prompt")
    await aiconfig.run("intial_prompt")
    init_question = aiconfig.get_output_text("intial_prompt")
    return init_question

async def analyse_and_generate(aiconfig,candidate_emotion_analysis,candidate_response,question,time_left):
    aiconfig.delete_output("response_feedback")
    a=aiconfig.get_parameters("response_feedback")
    await aiconfig.run("response_feedback", params={"candidate_response": candidate_response,"candidate_emotion_analysis":candidate_emotion_analysis})
    response_feedback = aiconfig.get_output_text("response_feedback")
    #print("-----------")
    #print(response_feedback)
    #adding current q and r to memory
    inputs={"inputs":question}
    outputs={"outputs":candidate_response}
    memory.save_context(inputs, outputs)
    interview_history=memory.load_memory_variables({})['history']
    print("generating questions")
    aiconfig.delete_output("QG_prompt")
    await aiconfig.run("QG_prompt", params={'interview_history': interview_history,"time_left":time_left})
    question_res = aiconfig.get_output_text("QG_prompt")
    print("-----------")
    
    return question_res


# Async entry point for the script
async def main():
    init_ques = await kickoff(aiconfig)
    print("KICKOFF DONE")
    print(init_ques)

    candidate_response = "Hi, I am Anushka. I am MSCS student at Umass Amherst. I have 2 years of experience as ML Engineer in India. I have worked at a Automated Product cataloging startup for 2 years and then at PwC as an ML associate for an year. Most of my workex has focused on Text generation, finetuning transformer models, Retrieval Augmented Generation based Pipeline over Audit data and a little weak supervision work. My interests currently include NLP and Information retrieval systems. I am also working at the BIONLP lab at Umass where I am working on LLM Alignment and Self rewarding LLMs in medical domain."
    candidate_emotion_analysis = "The candidate looks confident and enthusiastic with a smiling face."
    time_left = "38 minutes"

    ques0 = await analyse_and_generate(aiconfig, candidate_emotion_analysis, candidate_response, init_ques, time_left)
    print(ques0)

    print("----")
    candidate_response=" I have mainly worked on training end to end T5 transformer model. I was involved in the complete ML pipeline from data scraping, to processing to model training."
    candidate_emotion_analysis="The candidate looks neutral and attentive."
    time_left= "20 minutes"
    ques1 = await analyse_and_generate(aiconfig, candidate_emotion_analysis, candidate_response, ques0, time_left)
    print(ques1)

    print("----")
    candidate_response=" Umm...I think...I don't remember all the details well. I did train it more than 1 year back. My team did improve the metrics when you see Qualitative Analaysis with more diverse result..but..I.. "
    candidate_emotion_analysis="The candidate looks nervous and anxious."
    time_left= "10 minutes"
    ques2 = await analyse_and_generate(aiconfig, candidate_emotion_analysis, candidate_response, ques1, time_left)
    print(ques2)

    print("----")
    candidate_response="Um.. I think..I have not worked on those aspects I think.. Umm "
    candidate_emotion_analysis="The candidate looks nervous and anxious."
    time_left= "5 minutes"
    ques3 = await analyse_and_generate(aiconfig, candidate_emotion_analysis, candidate_response, ques2, time_left)
    print(ques3)




# Run the main function
if __name__ == "__main__":
    asyncio.run(main())