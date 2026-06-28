from tkinter import *
from tkinter import (ttk, messagebox)
#from transformers import BertTokenizer, BertModel, AutoModel
from transformers import pipeline
import os
from HF_token import HF_TOKEN


def chat(question: str) -> str:
    MODEL = "microsoft/Phi-4-mini-instruct" #"HuggingFaceTB/SmolLM2-1.7B-Instruct"

    chat = [
        {"role": "system", "content": "You are a helpful science assistant."},
        {"role": "user",   "content": question}
    ]
    pipe = pipeline(task="text-generation", model=MODEL, tokenizer=MODEL, dtype="auto", device_map="auto")
    response = pipe(chat, max_new_tokens=512)
    return response[0]["generated_text"][-1]["content"]

def summarize(article: str) -> str:
    MODEL = "microsoft/Phi-4-mini-instruct"

    summarizer = pipeline(model=MODEL)
    return summarizer(article, max_length=130, min_length=30, do_sample=False)


class AItask:
    ANSWER = 0
    SUMMARIZE = 1
    NUM_TASKS = 2

class AIExperiment(Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        
        self.allTasks = [""] * AItask.NUM_TASKS
        self.allTasks[AItask.ANSWER] = "AI shall answer a question"
        self.allTasks[AItask.SUMMARIZE] = "AI shall summarize a article"
        self.currTask = -1

        self.title("AI Experiment")
        self.resizable(0, 0)

        self.cb_task = ttk.Combobox(self)
        self.cb_task["values"] = self.allTasks
        self.cb_task.current(0)
        self.cb_task.grid(row=0, column=0, sticky="we")

        lbs_ques = Label(self, text="Input:", justify="left", anchor="w")
        lbs_ques.grid(row=1, column=0, sticky=W)

        self.txt_ques = Text(self, height=10, wrap=WORD)
        self.txt_ques.grid(row=2, column=0)

        lbl_answ = Label(self, text="Output:", justify="left", anchor="w")
        lbl_answ.grid(row=3, column=0, sticky=W)

        self.txt_answ = Text(self, height=10, wrap=WORD)
        self.txt_answ.grid(row=4, column=0)

        btn_task = Button(self, text="Select task", command=self.click_task)
        btn_task.grid(row=0, column=1)

        btn = Button(self, text="Go further", command=self.click_action)
        btn.grid(row=2, column=1)

    def click_task(self):
        article = """ New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.
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

        self.currTask = self.allTasks.index(self.cb_task.get())
        self.txt_ques.delete('1.0', END)
        self.txt_answ.delete('1.0', END)
        if self.currTask == AItask.ANSWER:
            self.txt_ques.insert(END, question + "\n")
        if self.currTask == AItask.SUMMARIZE:
            self.txt_ques.insert(END, article + "\n")

    def click_action(self):
        if self.currTask < 0:
            messagebox.showinfo("Error", "You must select the task first.")
            return
        if self.currTask == AItask.ANSWER:
            answ = chat(self.txt_ques.get("1.0", "end-1c"))
            self.txt_answ.insert(END, answ + "\n")
        if self.currTask == AItask.SUMMARIZE:
            answ = summarize(self.txt_ques.get("1.0", "end-1c"))
            self.txt_answ.insert(END, answ + "\n")


if __name__ == "__main__":
    os.environ["HF_TOKEN"] = HF_TOKEN

    app = AIExperiment()
    app.mainloop()
