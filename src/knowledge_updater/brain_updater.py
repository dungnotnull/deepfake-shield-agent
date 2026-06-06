from datetime import datetime
from typing import List, Dict

class BrainUpdater:
    """
    Maintains the SECOND-KNOWLEDGE-BRAIN.md file.
    Transforms raw research summaries into a structured knowledge base.
    """
    def __init__(self, brain_path: str = "SECOND-KNOWLEDGE-BRAIN.md"):
        self.brain_path = brain_path

    def update_knowledge(self, findings: List[Dict]):
        """
        Appends findings to the markdown file in the project's required format.
        """
        if not findings: return
        
        now = datetime.now().strftime("%Y-%m-%d")
        with open(self.brain_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n### Update {now} (Auto-Discovery)\n")
            f.write("**Papers processed:** " + str(len(findings)) + "\n\n")
            
            for i, paper in enumerate(findings):
                f.write(f"#### {paper['title']}\n")
                f.write(f"- **Source:** {paper['url']}\n")
                f.write(f"- **Key Finding:** {paper['summary']}\n")
                f.write("- **Actionable:** [ ] Evaluate model, [ ] Update Prompt\n\n")
        
        print(f"Successfully updated {self.brain_path} with {len(findings)} papers.")

if __name__ == "__main__":
    updater = BrainUpdater()
    updater.update_knowledge([{"title": "New Paper", "summary": "Cool stuff", "url": "arxiv.org/123"}])
