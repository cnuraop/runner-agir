import json
from tools.gmail_tool import GmailTool
from tools.google_docs_tool import GoogleDocsTool
from tools.wordpress_tool import WordPressTool
from tools.research_tool import ResearchTool
from utils.google_logger import GoogleLogger  # You create this to log in Docs

class LifeAutomationAgent:
    def __init__(self):
        self.gmail = GmailTool()
        self.docs = GoogleDocsTool()
        self.wp = WordPressTool()
        self.research = ResearchTool()
        self.logger = GoogleLogger()

    def load_tasks(self, path='todo.json'):
        with open(path, 'r') as file:
            return json.load(file)

    def confirm(self, message):
        print(f"[CONFIRMATION NEEDED] {message}")
        user_input = input("Type 'yes' to confirm: ")
        return user_input.strip().lower() == 'yes'

    def handle_task(self, task):
        desc = task['task']
        print(f"Handling: {desc}")

        if "email" in desc.lower():
            if self.confirm(f"Do you want to send this email: '{desc}'?"):
                response = self.gmail.send_email_from_task(desc)
                self.logger.log_task(task['id'], desc, response)
        elif "research" in desc.lower():
            if self.confirm(f"Do you want to perform research: '{desc}'?"):
                data = self.research.research_from_task(desc)
                doc_url = self.docs.save_research_to_doc(desc, data)
                self.logger.log_task(task['id'], desc, f"Saved to {doc_url}")
        elif "blog" in desc.lower() or "wordpress" in desc.lower():
            if self.confirm(f"Do you want to publish this blog: '{desc}'?"):
                post_url = self.wp.post_blog_from_task(desc)
                self.logger.log_task(task['id'], desc, f"Published: {post_url}")
        else:
            self.logger.log_task(task['id'], desc, "Task type not recognized.")

    def run(self):
        tasks = self.load_tasks()
        for task in tasks:
            self.handle_task(task)
