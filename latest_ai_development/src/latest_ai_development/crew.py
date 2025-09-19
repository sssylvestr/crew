import json
from typing import Dict, Any, List
from pathlib import Path
import datetime
import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from crewai import LLM

# Add this LLM configuration
gpt5_llm = LLM(
    model="azure/gpt-4o",  # Azure model format
    api_base="https://openai-nc-east-us-2.openai.azure.com",  # Your Azure endpoint
    api_key="6e72266c1ada4d32b94787854eed8ea1",  # Your Azure API key
    api_version="2025-03-01-preview",  # API version for GPT-5
    drop_params=True,
    additional_drop_params=["stop"]
)

@CrewBase
class ReviewCommitteeCrew:
    """Review Committee Crew to simulate a private equity investment review meeting using hierarchical process."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    def __init__(self, investment_memo_path: str = None):
        """Initialize the Review Committee Crew with a path to an investment memo JSON file."""
        # Default to None and allow the memo to be passed later
        self.investment_memo = None
        self.knowledge_source = None
        self.log_file = "agent_phrases.txt"
        
        if investment_memo_path:
            self.load_investment_memo(investment_memo_path)

    

    @before_kickoff
    def _clear_log(self, inputs):
        open(self.log_file, "w", encoding="utf-8").close()
        return inputs

    
    def load_investment_memo(self, path: str):
        """Load the investment memo from a JSON file."""
        memo_path = Path(path)
        if not memo_path.exists():
            raise FileNotFoundError(f"Investment memo file not found at {memo_path}")
        
        # Load the JSON data for internal use
        with open(memo_path, "r", encoding="utf-8") as f:
            self.investment_memo = json.load(f)
        
        # Get the raw file content as a string
        with open(memo_path, "r", encoding="utf-8") as f:
            raw_content = f.read()
        
        # Use StringKnowledgeSource with the raw string content
        self.knowledge_source = StringKnowledgeSource(
            content=raw_content,
            chunk_size=4000,  # Adjust based on your needs
            chunk_overlap=200  # Adjust based on your needs
        )
        
        return self.investment_memo

    @agent
    def an_agent(self) -> Agent:
        conf     = self.agents_config['an_agent']
        role_str = conf['role']
        a = Agent(config=conf, verbose=True, allow_delegation=False, llm=gpt5_llm)
        def _log_my_steps(step_output):
            text = (getattr(step_output, "output", None) or getattr(step_output, "text", "")).strip()
            if text:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"{role_str}: {text}\n")
        a.step_callback = _log_my_steps
        return a

    @agent
    def cf_agent(self) -> Agent:
        conf     = self.agents_config['cf_agent']
        role_str = conf['role']
        a = Agent(config=conf, verbose=True, allow_delegation=False, llm=gpt5_llm)
        def _log_my_steps(step_output):
            text = (getattr(step_output, "output", None) or getattr(step_output, "text", "")).strip()
            if text:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"{role_str}: {text}\n")
        a.step_callback = _log_my_steps
        return a

    @agent
    def fn_agent(self) -> Agent:
        conf     = self.agents_config['fn_agent']
        role_str = conf['role']
        a = Agent(config=conf, verbose=True, allow_delegation=False, llm=gpt5_llm)
        def _log_my_steps(step_output):
            text = (getattr(step_output, "output", None) or getattr(step_output, "text", "")).strip()
            if text:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"{role_str}: {text}\n")
        a.step_callback = _log_my_steps
        return a

    @agent
    def km_agent(self) -> Agent:
        conf     = self.agents_config['km_agent']
        role_str = conf['role']
        a = Agent(config=conf, verbose=True, allow_delegation=False, llm=gpt5_llm)
        def _log_my_steps(step_output):
            text = (getattr(step_output, "output", None) or getattr(step_output, "text", "")).strip()
            if text:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"{role_str}: {text}\n")
        a.step_callback = _log_my_steps
        return a

    @agent
    def rf_agent(self) -> Agent:
        conf     = self.agents_config['rf_agent']
        role_str = conf['role']
        a = Agent(config=conf, verbose=True, allow_delegation=False, llm=gpt5_llm)
        def _log_my_steps(step_output):
            text = (getattr(step_output, "output", None) or getattr(step_output, "text", "")).strip()
            if text:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"{role_str}: {text}\n")
        a.step_callback = _log_my_steps
        return a

    @agent
    def rs_agent(self) -> Agent:
        conf     = self.agents_config['rs_agent']
        role_str = conf['role']
        a = Agent(config=conf, verbose=True, allow_delegation=False, llm=gpt5_llm)
        def _log_my_steps(step_output):
            text = (getattr(step_output, "output", None) or getattr(step_output, "text", "")).strip()
            if text:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"{role_str}: {text}\n")
        a.step_callback = _log_my_steps
        return a

    @agent
    def manager_agent(self) -> Agent:
        conf     = self.agents_config['manager_agent']
        role_str = conf['role']
        a = Agent(config=conf, verbose=True, allow_delegation=True, llm=gpt5_llm)
        def _log_my_steps(step_output):
            text = (getattr(step_output, "output", None) or getattr(step_output, "text", "")).strip()
            if text:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"{role_str}: {text}\n")
        a.step_callback = _log_my_steps
        return a




    # @agent
    # def kt_agent(self) -> Agent:
    #     """KT - Strategic RC member"""
    #     return Agent(
    #         config=self.agents_config['kt_agent'],
    #         verbose=True,
    #         allow_delegation=False,
    #     )

    @agent
    def manager_agent(self) -> Agent:
        """Moderator who facilitates the RC meeting"""
        a = Agent(
            config=self.agents_config['manager_agent'],
            verbose=True,
            allow_delegation=True, llm=gpt5_llm
            )
        
        def _log_my_steps(step_output):
            # step_output is the AgentFinish
            text = getattr(step_output, "output", "") or getattr(step_output, "text", "")
            text = text.strip()
            if not text:
                return
            role = a.config.get("role", "KT")
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{role}: {text}\n")

        a.step_callback = _log_my_steps
        return a

    @task
    def conduct_review_meeting(self) -> Task:
        """Task for moderator to manage the entire meeting with delegation"""
        return Task(
            config=self.tasks_config['conduct_review_meeting']
        )

    @crew
    def crew(self) -> Crew:
        """Define the Review Committee Crew structure and process flow"""
        manager = self.manager_agent()
        manager.allow_delegation = True 

        crew_args = {
            "agents": [
                self.an_agent(),
                self.cf_agent(),
                self.fn_agent(),
                self.km_agent(),
                self.rf_agent(),
                self.rs_agent(),
                # self.kt_agent(),
            ],
            "tasks": [
                self.conduct_review_meeting()
            ],
            # "planning": False,
            # "planning_llm": gpt5_llm,
            "output_log_file": True,
            "process": Process.hierarchical,
            "manager_agent": manager,
            "max_iterations": 200,
            "verbose": True,
            "memory": True,
            "llm": gpt5_llm,
            "embedder": {
                "provider": "azure",
                "config": {
                    "model": "text-embedding-ada-002",
                    "api_key": "6e72266c1ada4d32b94787854eed8ea1",
                    "api_base": "https://OpenAI-NC-East-US-2.openai.azure.com",
                    "api_version": "2023-05-15"
                }
            }
        }
        
        if self.knowledge_source:
            crew_args["knowledge_sources"] = [self.knowledge_source]
        
        return Crew(**crew_args)

    def kickoff(self, investment_memo_path: str = None):
        """Run the Review Committee simulation and optionally save the output."""
        if investment_memo_path:
            self.load_investment_memo(investment_memo_path)
            
        if not self.investment_memo:
            raise ValueError("No investment memo provided. Please provide an investment memo path.")
            
        result = self.crew().kickoff()

        
        return result