# Conceptual Code: Coordinator using LLM Transfer
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
from .prompts import ROOT_AGENT_INSTRUCTION, ROOT_AGENT_DESCRIPTION, CREDIT_CARD_AGENT_INSTRUCTION, CREDIT_CARD_AGENT_DESCRIPTION
from .tools  import get_basic_account_information, get_user_transactions, get_credit_card_details, get_credit_card_late_fee_waive_off

load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

dispute_agent = LlmAgent(
    name="DisputeAgent",
    model=LiteLlm(model="openai/gpt-4.1"),
    tools=[],
    instruction="You are a Dispute Help Agent. Handle queries related to transaction disputes, unauthorized charges, or billing errors.",
    description="Handles user queries about transaction disputes and billing errors.",
)

credit_card_agent = LlmAgent(
    name="CreditCardAgent",
    model=LiteLlm(model="openai/gpt-4.1"),
    instruction=CREDIT_CARD_AGENT_INSTRUCTION,
    description=CREDIT_CARD_AGENT_DESCRIPTION,
    tools=[get_credit_card_details, get_credit_card_late_fee_waive_off]
)

loan_agent = LlmAgent(
    name="LoanAgent",
    model=LiteLlm(model="openai/gpt-4.1"),
    tools=[],
    instruction="You are a Loan Help Agent. Handle queries regarding loan applications, interest rates, repayment options, or loan status.",
    description="Handles user queries about loans and repayment options.",
)

account_agent = LlmAgent(
    name="AccountAgent",
    model=LiteLlm(model="openai/gpt-4.1"),
    tools=[],
    instruction="You are an Account Help Agent. Handle queries about account management, balance inquiries, password resets, or account security.",
    description="Handles user queries about account management and security.",
)

root_agent = LlmAgent(
    name="MainAIAssistant",
    model=LiteLlm(model="openai/gpt-4.1"),
    tools=[],
    instruction=ROOT_AGENT_INSTRUCTION,
    description=ROOT_AGENT_DESCRIPTION,
    sub_agents=[
        dispute_agent,
        credit_card_agent,
        loan_agent,
        account_agent,
    ],
)