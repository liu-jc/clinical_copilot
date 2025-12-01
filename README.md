# Clinical Copilot: A Multi-Turn Diagnosis Demo for Human–AI Collaboration

**Clinical Copilot** is an interactive demonstration system that simulates real-world multi-turn diagnostic encounters between an attending physician and an AI resident doctor. The system implements a collaboration protocol where clinicians can accept, modify, or reject AI-generated suggestions for questions, test orders, and diagnoses, creating a realistic environment for studying human–AI collaboration in clinical decision-making.

## Motivation

A prevailing paradigm in medical AI operates on a "one-shot" model. These systems are designed to ingest a complete snapshot of a patient's data—including all history, lab results, and findings gathered upfront—and output a diagnosis.

However, real-world diagnosis is not a single calculation but an iterative process of inquiry. Physicians sequentially ask questions and order tests to build their understanding. This natural workflow of clinical inquiry has been largely ignored by existing AI tools, creating a need for systems that support, rather than bypass, this process.

**Clinical Copilot** addresses this gap by orchestrating multi-turn diagnostic encounters that mirror how diagnosis happens in real clinical practice.

## Overview

In our system, the user plays the role of a senior physician, while an LLM assistant acts as an **AI Resident Doctor**. The AI can suggest what question to ask or which test to order next. Crucially, the user remains in full control: they can accept, edit, or completely ignore the AI's suggestions before taking an action.

While our underlying dataset for each demonstration case contains the complete patient record, we do not expose this information all at once. Instead, we employ two specialized LLM-powered agents to simulate information gathering:

- **Patient Agent**: Answers questions proposed by the doctor as the real patient would, using everyday language and avoiding medical jargon
- **Examination Agent**: Provides test results ordered by the doctor, formatted like clinical reports

Both agents take the complete patient file as input but are constrained to synthesize and deliver only the relevant piece of information requested, thereby enforcing an iterative diagnostic workflow.

The system also includes:
- **Cost Estimator**: Provides real-time feedback on resource utilization
- **Judge Agent**: Evaluates diagnostic accuracy against ground truth using a 5-point scoring rubric

## Target Audience

**Clinical Copilot** is designed for diverse audiences:

- **Medical students and residents**: Seeking a hands-on tool to practice diagnostic skills
- **Medical educators**: Can integrate it into curricula for case-based learning
- **HCI and clinical informatics researchers**: Experimental platform for studying human-AI teaming
- **AI developers**: Design pattern for building more responsible and collaborative clinical support tools

## Features

- **Multi-Turn Interaction**: Turn-based diagnostic encounters with realistic clinical flow
- **Human-AI Collaboration**: AI suggests next steps; human maintains full control
- **Specialized Agents**: Patient Agent for conversational responses, Examination Agent for objective data
- **Cost Awareness**: Tracks test costs using CPT codes and provides real-time feedback
- **Automated Evaluation**: Judge agent scores diagnostic accuracy with detailed rationale
- **Interactive Demo**: Streamlit-based UI for hands-on exploration
- **Open Source**: Available for deployment in both research and educational settings

## Installation

1. Clone or download the Clinical Copilot repository:
   ```bash
   git clone <repository-url>
   cd SDBench
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API credentials:
   
   For OpenAI:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```
   
   For OpenRouter (default):
   ```bash
   export OPENROUTER_API_KEY="your_api_key_here"
   export SDBENCH_API_PROVIDER="openrouter"
   ```
   
   Or create a `.env` file with:
   ```
   OPENAI_API_KEY=your_api_key_here
   # OR
   OPENROUTER_API_KEY=your_api_key_here
   SDBENCH_API_PROVIDER=openrouter
   ```

## Quick Start

### Run the Interactive Demo

The main demo provides a full interactive experience:

```bash
streamlit run clinical_rounds_ui.py
```

This launches the **Clinical Copilot** interface where you can:
1. Select a patient case
2. Draft questions, test orders, or diagnoses yourself or let the AI Resident Doctor suggest them
3. Receive responses from the Patient Agent (for questions) or Examination Agent (for tests)
4. Build your diagnostic reasoning iteratively
5. Submit your final diagnosis for evaluation by the Judge Agent

### Run Automated Benchmark

For automated evaluation of diagnostic agents:

```bash
python main.py quick    # Quick test
python main.py single   # Single case demo
python main.py full     # Full benchmark
```

## System Architecture

### Core Components

#### Patient Agent
- Simulates patient responses in natural, first-person language
- Avoids medical jargon to mimic real patient communication
- Grounded in the complete case file but only reveals requested information
- Uses LLM to synthesize conversational answers from case data

#### Examination Agent
- Acts as a clinical information system for objective data
- Returns lab results, imaging findings, and physical exam results
- Formats output like formal clinical reports
- Extracts only the specific data points requested

#### AI Resident Doctor
- Suggests next clinical actions (questions, tests, or diagnoses)
- Provides draft suggestions that users can accept, modify, or reject
- Modular design allows easy replacement with different LLM models or agent architectures

#### Cost Estimator
- Maps test requests to CPT codes using language models
- Uses 2023 CMS pricing data for cost calculation
- Tracks both physician visit costs ($300 per visit) and test costs
- Provides real-time feedback on resource utilization

#### Judge Agent
- Evaluates final diagnoses using a 5-point Likert scale:
  - 5: Perfect/Clinically superior
  - 4: Mostly correct (minor incompleteness)
  - 3: Partially correct (major error)
  - 2: Largely incorrect
  - 1: Completely incorrect
- Provides detailed rationale for scoring decisions

### Workflow

The system operates on a turn-based workflow:

1. **Initialization**: User selects a case from the dataset. The UI presents only the initial abstract (chief concern).
2. **Action Formulation**: User selects an action type (ask question, request test, or diagnose) and chooses whether to draft it themselves or let the AI Resident Doctor suggest it.
3. **AI Suggestion (Optional)**: If requested, the AI Resident Doctor receives the encounter transcript and proposes a draft suggestion.
4. **Action Submission**: User finalizes and submits their action.
5. **Backend Processing**: 
   - Questions → **Patient Agent**
   - Test orders → **Examination Agent** (plus Cost Estimator)
   - Diagnoses → Logged for final evaluation
6. **State Update**: System updates with the new action and response. UI refreshes to show the new turn in the clinical timeline.
7. **Finalization**: User triggers evaluation. The **Judge Agent** compares the final diagnosis against ground truth and returns a score with rationale.

## Usage Examples

### Interactive Demo Session

```python
# Launch the Streamlit demo
streamlit run clinical_rounds_ui.py
```

The interface guides you through:
- Selecting a patient case
- Reviewing the initial presentation
- Planning each step (ask question, order test, or diagnose)
- Choosing to draft yourself or get AI assistance
- Viewing responses from Patient/Examination agents
- Tracking costs in real-time
- Finalizing and receiving judge evaluation

### Custom Diagnostic Agent

For automated evaluation, implement a custom diagnostic agent:

```python
from sdbench import DiagnosticAgent
from data_models import AgentAction, ActionType

class MyCustomAgent(DiagnosticAgent):
    def __init__(self):
        super().__init__("MyCustomAgent")
    
    def get_next_action(self, case_abstract: str, encounter_history: List[AgentAction]) -> AgentAction:
        # Implement your diagnostic logic here
        # Use encounter_history to build context
        if len(encounter_history) < 5:
            return AgentAction(
                action_type=ActionType.ASK_QUESTIONS,
                content="How have you been feeling lately?"
            )
        else:
            return AgentAction(
                action_type=ActionType.DIAGNOSE,
                content="Based on available information, the diagnosis is..."
            )
    
    def reset(self):
        # Reset agent state for new case
        pass
```

## Data Models

The system uses Pydantic models for type safety and validation:

- `CaseFile`: Complete case information including abstract, full text, and ground truth diagnosis
- `AgentAction`: Actions taken (questions, test requests, or diagnoses)
- `GatekeeperResponse`: Responses from Patient or Examination agents with source attribution
- `DiagnosticEncounter`: Complete encounter with all interactions
- `BenchmarkResult`: Evaluation results and metrics

## Configuration

Key configuration options in `config.py`:

- `API_PROVIDER`: Choose 'openai' or 'openrouter' (default: 'openrouter')
- `PHYSICIAN_VISIT_COST`: Cost per physician visit (default: $300)
- `CORRECT_DIAGNOSIS_THRESHOLD`: Minimum score for correct diagnosis (default: 4)
- `GATEKEEPER_MODEL`: Model for gatekeeper sub-agents (default: "openai/gpt-4o-mini")
- `JUDGE_MODEL`: Model for judge agent (default: "openai/gpt-4o-mini")
- `PATIENT_AGENT_MODEL`: Model for patient agent (inherits from GATEKEEPER_MODEL if not set)
- `EXAMINATION_AGENT_MODEL`: Model for examination agent (inherits from GATEKEEPER_MODEL if not set)

## File Structure

```
SDBench/
├── clinical_rounds_ui.py    # Main interactive demo (Streamlit)
├── patient_agent.py          # Patient Agent implementation
├── examination_agent.py      # Examination Agent implementation
├── gatekeeper_agent.py       # Gatekeeper orchestrator
├── cost_estimator.py         # Cost estimation module
├── judge_agent.py            # Judge agent implementation
├── config.py                 # Configuration settings
├── data_models.py            # Pydantic data models
├── data_loader.py            # Dataset loading utilities
├── sdbench.py               # Core SDBench class for automated runs
├── evaluation_protocol.py   # Evaluation metrics and reporting
├── synthetic_cases.py       # Synthetic test cases
├── example_agents.py        # Example diagnostic agents
├── main.py                  # CLI interface for automated runs
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Evaluation

The system can be evaluated through:

1. **Interactive Human Sessions**: Users work through cases in the Streamlit demo, with judge scores tracked for each encounter
2. **Automated Agent Evaluation**: Diagnostic agents can be run programmatically across case sets, with accuracy and cost metrics computed
3. **Human-AI Collaboration Studies**: Researchers can study how different collaboration patterns affect diagnostic outcomes

### Metrics

- **Diagnostic Accuracy**: Percentage of cases with judge score ≥ 4
- **Average Cumulative Cost**: Mean total cost across all cases
- **Turn Efficiency**: Average number of turns needed to reach diagnosis
- **Cost-Accuracy Trade-off**: Visualization of performance across different strategies

## Contributing

We welcome contributions! Clinical Copilot is designed to be extensible:

- Add new diagnostic agents for automated evaluation
- Extend the Patient or Examination agents with additional capabilities
- Integrate with external medical knowledge bases
- Enhance the UI with additional visualization features
- Add new evaluation metrics or study protocols

To contribute:

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open-source and available for research and educational purposes.

## Citation

If you use Clinical Copilot in your research, please cite:

```
@article{clinicalcopilot2025,
  title={Clinical Copilot: A Multi-Turn Diagnosis Demo for Human–AI Collaboration},
  author={[Authors]},
  journal={[Journal]},
  year={2025}
}
```

## Support

For questions, issues, or collaboration inquiries, please open an issue on the repository or contact the development team.

## Acknowledgments

Clinical Copilot builds upon the SDBench framework and is designed to support research on sequential diagnosis, human-AI collaboration, and clinical decision-making systems.
