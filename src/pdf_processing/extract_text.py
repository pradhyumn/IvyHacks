import fitz
 
class ExtractText:
    # def __init__(self):
    #     self.job_description = ""
    #     self.resume = ""

    def extract_text_from_pdf(self,buffer):
        with fitz.open(stream=buffer, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text

    def send_text_to_claude_api(self,text, client):
        message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        system="Summarize the following resume making sure all the technical details are covered and concise",
        messages=[{"role": "user", "content": text}]
        )
        return message

