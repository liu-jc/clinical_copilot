"""Gatekeeper Agent now orchestrates the Patient and Examination agents."""

from typing import Tuple

from data_models import CaseFile, AgentAction, GatekeeperResponse, ActionType
from config import Config
from patient_agent import PatientAgent
from examination_agent import ExaminationAgent


class GatekeeperAgent:
    """The Gatekeeper Agent routes requests to specialized sub-agents."""

    def __init__(self, config: Config):
        self.config = config
        self.patient_agent = PatientAgent(config)
        self.examination_agent = ExaminationAgent(config)
        self.model = (
            f"patient={self.patient_agent.model}, exam={self.examination_agent.model}"
        )

    def process_action(
        self, action: AgentAction, case_file: CaseFile
    ) -> GatekeeperResponse:
        """Process a question or test request using the appropriate sub-agent."""
        if action.action_type == ActionType.ASK_QUESTIONS:
            return self.patient_agent.answer_question(action.content, case_file)
        if action.action_type == ActionType.REQUEST_TESTS:
            return self.examination_agent.fetch_result(action.content, case_file)
        raise ValueError(f"Gatekeeper cannot process action type: {action.action_type}")

    def validate_request(self, action: AgentAction) -> Tuple[bool, str]:
        """Validate if a request is appropriate for the gatekeeper."""
        if action.action_type == ActionType.ASK_QUESTIONS:
            # Check for overly broad questions
            broad_indicators = [
                "tell me everything", "what's wrong", "what should I do",
                "give me all information", "summarize the case"
            ]
            
            question_lower = action.content.lower()
            for indicator in broad_indicators:
                if indicator in question_lower:
                    return False, "Please ask more specific questions about the patient's history or examination findings."
            
            return True, ""
        
        elif action.action_type == ActionType.REQUEST_TESTS:
            # Check for vague test requests
            vague_indicators = [
                "run blood work", "do some imaging", "order labs",
                "get tests", "run diagnostics"
            ]
            
            test_lower = action.content.lower()
            for indicator in vague_indicators:
                if indicator in test_lower:
                    return False, "Please specify the exact test you would like to order (e.g., 'Complete Blood Count', 'CT of the abdomen with contrast')."
            
            return True, ""
        
        return True, ""
