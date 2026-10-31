from tkinter import *
from tkinter import (ttk, messagebox)
from transformers import pipeline
import os


class AItask:
    MODEL = "microsoft/Phi-4-mini-instruct"
    #MODEL = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

    def run_chat_model(self, context: list, max_num_token: int) -> str:
        pipe = pipeline(task="text-generation", model=AItask.MODEL, tokenizer=AItask.MODEL, dtype="auto", device_map="auto")
        response = pipe(context, max_new_tokens=max_num_token)
        return response[0]["generated_text"][-1]["content"]

    def __call__(self, query: str, tokens_out: int) -> str:
        context = [
            {"role": "system", "content": "You are a helpful science assistant."},
            {"role": "user", "content": query}
        ]
        return self.run_chat_model(context, tokens_out)


class AIExperiment(Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        
        self.taskCaptions = ["AI shall answer a question", "AI shall summarize a article"]

        self.title("AI Experiment")
        self.resizable(0, 0)

        frame_ques = LabelFrame(self, text="Input", relief="groove")
        frame_ques.grid(row=0, column=0, padx=10, pady=10)

        lbl_exp = Label(frame_ques, text="Examples:", justify="left", anchor="w")
        lbl_exp.grid(row=0, column=0)

        self.cb_task = ttk.Combobox(frame_ques)
        self.cb_task["values"] = self.taskCaptions
        self.cb_task.current(0)
        self.cb_task.grid(row=0, column=1)

        btn_predef = Button(frame_ques, text="Set", command=self.click_example)
        btn_predef.grid(row=0, column=2)

        self.txt_ques = Text(frame_ques, height=10, wrap=WORD)
        self.txt_ques.grid(row=1, column=0, columnspan=3)

        frame_answ = LabelFrame(self, text="Output", relief="groove")
        frame_answ.grid(row=1, column=0, padx=10, pady=10)

        self.txt_answ = Text(frame_answ, height=10, wrap=WORD)
        self.txt_answ.grid(row=0, column=0)

        btn_resp = Button(self, text="Get response", command=self.click_response)
        btn_resp.grid(row=0, column=1)

    def click_example(self):
        article = "Summarize the following text:\n" + """ New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.
        A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband.
        Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared "I do" five more times, sometimes only within two weeks of each other.
        In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her "first and only" marriage.
        Barrientos, now 39, is facing two criminal counts of "offering a false instrument for filing in the first degree," referring to her false statements on the
        2010 marriage license application, according to court documents.
        Prosecutors said the marriages were part of an immigration scam.
        On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further.
        After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective
        Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002.
        All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say.
        Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages.
        Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted.
        The case was referred to the Bronx District Attorney\'s Office by Immigration and Customs Enforcement and the Department of Homeland Security\'s
        Investigation Division. Seven of the men are from so-called "red-flagged" countries, including Egypt, Turkey, Georgia, Pakistan and Mali.
        Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force.
        If convicted, Barrientos faces up to four years in prison.  Her next court appearance is scheduled for May 18."""

        question = "Hey, can you explain gravity to me?"

        self.txt_ques.delete('1.0', END)
        self.txt_answ.delete('1.0', END)
        if self.cb_task.get() == self.taskCaptions[0]:
            self.txt_ques.insert(END, question + "\n")
        elif self.cb_task.get() == self.taskCaptions[1]:
            self.txt_ques.insert(END, article + "\n")

    def click_response(self):
        num_tokens = -1
        if self.cb_task.get() == self.taskCaptions[0]:
            num_tokens = 512
        elif self.cb_task.get() == self.taskCaptions[1]:
            num_tokens = 130

        tAI = AItask()
        answ = tAI(self.txt_ques.get("1.0", "end-1c"), num_tokens)

        self.txt_answ.delete('1.0', END)
        self.txt_answ.insert(END, answ + "\n")


if __name__ == "__main__":
    try:
        from HF_token import HF_TOKEN
        os.environ["HF_TOKEN"] = HF_TOKEN
    except:
        messagebox.showinfo("Error", "Please provide Access Token for HuggingFace.")

    app = AIExperiment()
    app.mainloop()
