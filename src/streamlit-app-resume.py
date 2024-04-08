import streamlit as st
import os
import anthropic
import fitz
from pdf_processing.send_to_claude import send_text_to_claude_api
from pdf_processing.context_storing import send_text_to_claude_context
import whisper
import tempfile
from st_audiorec import st_audiorec
from gtts import gTTS
import base64

st.title("Interview Pro")

api_key = os.environ["ANTHROPIC_API_KEY"]
client = anthropic.Anthropic(api_key=api_key)

# Load the Whisper model
whisper_model = whisper.load_model("small")

system="You are an AI assistant that asks a question within 3 sentences to interview a candidate for the given job profile and previous responses. The initial emotion in the question should be neutral and make sure you make the candidate comfortable. Also, check the accuracy of the responses in the given context. Respond to candidates in second person as if you are talking directly to them. Move on to other parts of the resume after 2 questions on one aspect."
conversation=""

# Initialize session state for controlling UI display
if "submitted" not in st.session_state:
    st.session_state.submitted = False
    st.session_state.first_question=""
    st.session_state.context=""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "results" not in st.session_state:
    st.session_state.results = False

if st.sidebar.button("Interview Results"):
    st.session_state.results = not st.session_state.results

if not st.session_state.submitted and not st.session_state.results:
    # Load the PDF file
    resume = st.file_uploader("Upload your resume", type=["pdf"])
    user_content = st.text_input("Enter your job description")

    if st.sidebar.button("Submit"):
        if resume is not None and user_content:
            try:
                doc = fitz.open(stream=resume.read(), filetype="pdf")
                text = user_content
                for page in doc:
                    text += page.get_text() + "\n\n"
                st.sidebar.success("Reading resume")
                curr_context=send_text_to_claude_context(text, client=client)
                first_question=send_text_to_claude_api(curr_context.content[0].text, system=system, client=client)
                st.session_state.messages.append({"role": "assistant", "content": first_question.content[0].text})
                st.session_state.context+="Resume and job:"+curr_context.content[0].text+"\n question:"+first_question.content[0].text
                st.session_state.submitted = True
            except Exception as e:
                st.sidebar.error("Error reading resume")
        else:
            st.sidebar.error("Please upload a resume and enter a job description")

if st.session_state.submitted and not st.session_state.results:
    
    audio_data = st_audiorec() 
    if not st.session_state.get('first_audio_played', False):
        try:
            tts = gTTS(first_question.content[0].text, lang="en")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                # Convert MP3 file to Base64
                with open(fp.name, "rb") as mp3_file:
                    base64_audio = base64.b64encode(mp3_file.read()).decode('utf-8')
                audio_html = f'''
                <audio autoplay>
                <source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3" />
                </audio>
                '''
                st.markdown(audio_html, unsafe_allow_html=True)
                st.session_state['first_audio_played'] = True
        except Exception as e:
            st.error("Failed to generate speech: {}".format(e))

    # Write instructions on sidebar
    st.sidebar.markdown("Press start recording to begin your response and stop recording to end your response")
    for message in st.session_state.messages:
        if message["content"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
    if audio_data is not None and len(audio_data)>0:
        with tempfile.NamedTemporaryFile(delete=True, suffix='.wav', mode='wb') as tmpfile:
            tmpfile.write(audio_data)
            tmpfile.flush()
            try:
                transcript = whisper_model.transcribe(tmpfile.name)
                if transcript:
                    st.session_state.messages.append({"role": "user", "content": transcript['text']})
                    with st.chat_message("user"):
                        st.markdown(transcript['text'])
                        st.session_state.context+="\n Response: "+transcript["text"]
                    with st.chat_message("assistant"):
                        message_placeholder = st.empty()
                        full_response = ""
                        response = send_text_to_claude_api(st.session_state.context, system, client=client)
                        full_response+=response.content[0].text
                        try:
                            tts = gTTS(full_response, lang="en")
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                                tts.save(fp.name)
                                # Convert MP3 file to Base64
                                with open(fp.name, "rb") as mp3_file:
                                    base64_audio = base64.b64encode(mp3_file.read()).decode('utf-8')
                                audio_html = f'''
                                <audio autoplay>
                                <source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3" />
                                </audio>
                                '''
                                st.markdown(audio_html, unsafe_allow_html=True)
                                #st.audio(fp.read(), format="audio/mp3")
                            message_placeholder.markdown(full_response)
                            # Add assistant response to chat history
                            st.session_state.messages.append({"role": "assistant", "content": full_response})
                            st.session_state.context+="\n Question:"+full_response
                        except Exception as e:
                            st.error("Failed to generate speech: {}".format(e))
            except Exception as e:
                st.error("Failed to transcribe audio: {}".format(e))


if st.session_state.submitted and st.session_state.results:
    system="You are an AI assistant that gives a candidate feedback on their responses to interview questions with realistic ratings on scale of 10 for the overall interview. Be more conservative in your ratings."
    conversation=""
    for message in st.session_state.messages:
        if message["content"]:
            conversation+=f"{message['role']}={message['content']}\n"
    # Clear the messages after building conversation
    st.session_state.messages.clear()
    if conversation:
        results=send_text_to_claude_api(conversation, system, client=client)
        st.markdown(results.content[0].text)
    else:
        st.markdown("No conversation found")