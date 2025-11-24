# **LATS Implementation without External Web Search Tools**

# 1. Setting Up the Environment"""

from __future__ import annotations
import getpass
import os
import json
import math
from collections import deque
from typing import Optional, Literal
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph, START
#from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers.openai_tools import (
    JsonOutputToolsParser,
    PydanticToolsParser,
)

#from langchain_community.chat_models import ChatOpenAI
#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import chain as as_runnable
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.runnables import RunnableConfig
# from IPython.display import Image, display, Markdown
from collections import defaultdict
import streamlit as st
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
llm = ChatOpenAI(model="gpt-4o", openai_api_key=OPENAI_API_KEY) #enter open-Ai key here

"""# 2. Class Declarations of Node, Tree State and Reflection"""

class Node:
    def __init__(
        self,
        messages: list[BaseMessage],
        reflection: Reflection,
        parent: Optional[Node] = None,
    ):
        self.messages = messages
        self.parent = parent
        self.children = []
        self.value = 0
        self.visits = 0
        self.reflection = reflection
        self.depth = parent.depth + 1 if parent is not None else 1
        self._is_solved = reflection.found_solution if reflection else False
        if self._is_solved:
            self._mark_tree_as_solved()
        self.backpropagate(reflection.normalized_score)
        print(f"Created node : {self}")

    def __repr__(self) -> str:
        return (
            f"<Node value={self.value:.2f}, visits={self.visits},"
            f" Response={self.messages[-1].content[:50] if self.messages else 'No messages'}...,"
            f" Reflection={self.reflection.reflections[:50] if self.reflection else 'No reflection'}...,"
            f" is_solved={self._is_solved}, depth={self.depth}>"
        )

    @property
    def is_solved(self):
        return self._is_solved

    @property
    def is_terminal(self):
        return not self.children

    @property
    def best_child(self):
        if not self.children:
            return None
        all_nodes = self._get_all_children()
        return max(all_nodes, key=lambda child: child.upper_confidence_bound())

    @property
    def best_child_score(self):
        if not self.children:
            return None
        return max(self.children, key=lambda child: int(child.is_solved) * child.value)

    @property
    def height(self) -> int:
        if self.children:
            return 1 + max([child.height for child in self.children])
        return 1

    def upper_confidence_bound(self, exploration_weight=1.0):
        if self.parent is None:
            raise ValueError("Cannot obtain UCT from root node")
        if self.visits == 0:
            return float('inf')
        average_reward = self.value / self.visits
        exploration_term = math.sqrt(math.log(self.parent.visits) / self.visits)
        return average_reward + exploration_weight * exploration_term

    def backpropagate(self, reward: float):
        node = self
        while node:
            node.visits += 1
            node.value = (node.value * (node.visits - 1) + reward) / node.visits
            node = node.parent

    def get_messages(self, include_reflections: bool = True):
        if include_reflections:
            return self.messages + [self.reflection.as_message()]
        return self.messages

    def get_trajectory(self, include_reflections: bool = True) -> list[BaseMessage]:
        messages = []
        node = self
        while node:
            messages.extend(
                node.get_messages(include_reflections=include_reflections)[::-1]
            )
            node = node.parent
        return messages[::-1]

    def _get_all_children(self):
        all_nodes = []
        nodes = deque([self])
        while nodes:
            node = nodes.popleft()
            all_nodes.extend(node.children)
            nodes.extend(node.children)
        return all_nodes

    def get_best_solution(self):
        all_nodes = [self] + self._get_all_children()
        best_node = max(
            all_nodes,
            key=lambda node: int(node.is_terminal and node.is_solved) * node.value,
        )
        return best_node

    def _mark_tree_as_solved(self):
        parent = self.parent
        while parent:
            parent._is_solved = True
            parent = parent.parent
#--------------------------------------

class Reflection(BaseModel):
    reflections: str = Field(
        description="The critique and reflections agent based on the Dialectical Behaviour Therapy (DBT) component or element skills specialist"
    )
    score: int = Field(
        description="""Think step by step
            You have some criteria: Now below I set criteria: 
                    1 Is it Impact_on_well_being.
                    2 Is it User_Goal_Achievement.
                    3 Is it usefull for User_Satisfaction
                    4 Is it usefull for Feedback_Quality

            # Now, You have to generate reward by following rules. Before reward generation you need to consider conversation context:
                - You have to generate reward for all criteria within 1 to 5.
                - You have to highly critical.
                - Reward value should be consider DBT component effectiveness to address patient mental states.
                - Reward value should be consider DBT component effectiveness to address patient emotions, symptoms, and patient current situation.
                - Reward value consider patient's Immediate and long-term therapeutic goal by following DBT component in given patient context.
                - Reward value consider emotional, psychological, and physical well-being by following DBT component in given patient context.
                - Reward value consider patient's current and long-term satisfaction by following DBT component in given patient context.
                - Reward value consider 'Clarity and Specificity' by following DBT component in given patient context.
             
                The reward variable are:
                    Impact_on_well_being_reward
                    User_Goal_Achievement_reward
                    User_Satisfaction_reward
                    Feedback_Quality_reward
                    
            # Now, You have to generate probability by following rules. Before reward generation you need to consider conversation context:
                - you must generate a probability between 0.0 and 1.0 for the above criterion and for the given conversation context. 
                - If the patient has stress or depression, you will give high weight to impact on well-being. If the patient needs to achieve a specific goal, you will give high weight to goal achievement criteria. You will adjust the probability for 'User_Satisfaction_probability' and 'feedback_quality_probability' based on DBT componend effectiveness for given conversation context.
                - Propability values should consider both immediate emotional relief and long-term therapeutic benefits by that following DBT component.
                - You have to generate propability by considering following DBT component reliability, effectiveness to address patient current mental state situation is in the given context.

                The probability variable are:
                    Impact_on_well_being_probability
                    User_Goal_Achievement_probability
                    User_Satisfaction_probability
                    Feedback_Quality_probability
            
            # Now, You have to generate weight by following rules. Before reward generation you need to consider conversation context:
                - Weight should be consider following criteria which are personalized: 1) Impact on wellbeing of patient, 2)  Goal Achivement of patient 3) Patient satisfaction  4) Feedback Quality for patient by following criteria in the given <Context><Context> XML tag.
                - Weight should be consider patient personal Emotional Stability Improvement, Coping Strategy  for situation, shift positive emotion by folllowing DBT component for the given conversation context.
                - Weight should be consider priority-based on patient needs for well-being in given conte
                
                The probability variable are:
                    Impact_on_well_being_weight
                    User_Goal_Achievement_weight
                    User_Satisfaction_weight
                    Feedback_Quality_weight

            After that, you need to calculate the score by using below score formula and you have to give the score in integer value:
            Score  = Impact_on_well_being_probability * (Impact_on_well_being_reward * Impact_on_well_being_weight)  + User_Goal_Achievement_probability * (User_Goal_Achievement_reward * User_Goal_Achievement_weight) + User_Satisfaction_probability *  (User_Satisfaction_reward * User_Satisfaction_weight) + Feedback_Quality_probability * (Feedback_Quality_reward * Feedback_Quality_weight)

            You can Learn From the below Example to calculation. Below Example is Learning for you.

            Example: Impact_on_well_being_reward = 4, User_Goal_Achievement_reward = 5, User_Satisfaction_reward = 4, Feedback_Quality_reward = 3
                     Impact_on_well_being_probability = 0.3, User_Goal_Achievement_probability =0.3, User_Satisfaction_probability = 0.2, Feedback_Quality_probability = 0.2
                     Impact_on_well_being_weight = 0.2, User_Goal_Achievement_weight =0.2, User_Satisfaction_weight = 0.1, Feedback_Quality_weight = 0.1
            
            Score = 0.3 * (4 * 0.2) + 0.3 * (5 * 0.2) + 0.2 * (4 * 0.1) + 0.2 * (3 * 0.1)
                  = 0.3 * 0.8 + 0.3 * 1.0 + 0.2 * 0.4 + 0.2 * 0.3
                  = 0.24 + 0.3 + 0.08 + 0.06
                  = 0.68
                  I repeat, you have to give the answer in integer value
                  """,
        ge=0,
        le=10,
    )

    found_solution: bool = Field(
        description="Whether this DBT component or element is perfect for the patient or user's next to response generation?"
        )

    def as_message(self):
        return HumanMessage(
            content=f"Reasoning: {self.reflections}\nScore: {self.score}"
        )

    @property
    def normalized_score(self) -> float:
        return self.score / 1.0

#-------------------------------
class TreeState(TypedDict):
    root: Node
    input: str

"""# 3. Reflection"""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a mental health therapist critic. Be soft critical in response. Users always ask which DBT element is needed for the next response generation based on user input",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="candidate"),
    ]
)

reflection_llm_chain = (
    prompt
    | llm.bind_tools(tools=[Reflection], tool_choice="Reflection").with_config(
        run_name="Reflection"
    )
    | PydanticToolsParser(tools=[Reflection])
)
@as_runnable
def reflection_chain(inputs) -> Reflection:
    tool_choices = reflection_llm_chain.invoke(inputs)
    reflection = tool_choices[0]
    if not isinstance(inputs["candidate"][-1], AIMessage):
        reflection.found_solution = False
    print(f"Generated reflection: {reflection} \n")
    return reflection

"""# 4. Initial Response with Reflection"""

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a Simulation Mental Health Therapist and DBT Component Specialist: Firstly, try to understand 'Previous conversation history' context and 'Patient last Utterarcne' intent.
             Now You have four DBT elements: 'Emotion Regulation', 'Interpersonal Effectiveness', 'Mindfulness' and 'Distress Tolerance'.
             You have to select which element is best for the next response generation based on your therapist's skill, Previous conversation history context and Patient's last Utterarcne.

             You have to return only the element name, The format is below:
             [element_name]
            """,
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="messages", optional=True),
    ]
)

initial_answer_chain = prompt_template | llm.with_config(run_name="GenerateInitialCandidate")

parser = JsonOutputToolsParser(return_id=True)

def generate_initial_response(state: TreeState) -> dict:
    print("Generating initial response")
    res = initial_answer_chain.invoke({"input": state["input"]})
    output_messages = [res]
    content = res.content
    #display(Markdown(content))
    # print(f"Initial response: {res.content[:100]}...")
    reflection = reflection_chain.invoke(
        {"input": state["input"], "candidate": output_messages}
    )
    # print(f"\nInitial reflection: {reflection} \n ")
    root = Node(output_messages, reflection=reflection)
    print(f"Initial root node created: {root}")
    return {
        **state,
        "root": root,
    }

"""# 5. Tree Expansion"""

def generate_candidates(messages: ChatPromptValue, config: RunnableConfig):
    n = config["configurable"].get("N", 8)
    print(f"Generating {n} candidates")
    chat_result = llm.generate(
        [messages.to_messages()],
        n=n,
        callbacks=config["callbacks"],
        run_name="GenerateCandidates"
    )
    return [gen.message for gen in chat_result.generations[0]]

expansion_chain = prompt_template | generate_candidates

def expand(state: TreeState, config: RunnableConfig) -> dict:
    print("Expanding tree \n")
    root = state["root"]
    best_candidate: Node = root.best_child if root.children else root
    print(f"Best candidate for expansion : {best_candidate} \n")
    messages = best_candidate.get_trajectory()

    new_candidates = expansion_chain.invoke(
        {"input": state["input"], "messages": messages}, config
    )
    print(f"Generated {len(new_candidates)} new candidates \n")

    output_messages = [[candidate] for candidate in new_candidates]

    reflections = reflection_chain.batch(
        [{"input": state["input"], "candidate": msges} for msges in output_messages],
        config,
    )

    child_nodes = [
        Node(cand, parent=best_candidate, reflection=reflection)
        for cand, reflection in zip(output_messages, reflections)
    ]
    best_candidate.children.extend(child_nodes)
    print(f"\n Added {len(child_nodes)} child nodes to the tree \n")

    return state


def should_loop(state: TreeState) -> Literal["expand", "__end__"]:
    root = state["root"]
    print(f"Checking if should loop again. Root height: {root.height}, Solution Found: {root.is_solved} \n")
    if root.is_solved:
        print("Root is solved. Ending search. \n")
        return END
    if root.height >= 3:
        print("Max height reached. Ending search. \n ")
        return END
    print("Continuing to expand. \n")
    return "expand"

"""# 6. Build Graph"""

builder = StateGraph(TreeState)
builder.add_node("start", generate_initial_response)
builder.add_node("expand", expand)
builder.add_edge(START, "start")

builder.add_conditional_edges(
    "start",
    should_loop,
)
builder.add_conditional_edges(
    "expand",
    should_loop,
)

graph = builder.compile()

"""# 7. Tree Search for best answer"""

def print_tree(node, level=0):
    print("  " * level + str(node))
    for child in node.children:
        print_tree(child, level + 1)

def run_tree_search(question):
    # print(f"Starting tree search for question")
    last_step = None
    for step in graph.stream({"input": question}):
        last_step = step
        step_name, step_state = next(iter(step.items()))
        #print(f"Step: {step_name}")
        #print(f"Tree height: {step_state['root'].height}")
        #print("--------------------------------------------------------")

    if "expand" in last_step:
        solution_node = last_step["expand"]["root"].get_best_solution()
        best_trajectory = solution_node.get_trajectory(include_reflections=False)
        print("Best solution found:")
        # print(best_trajectory[-1].content)
        content = best_trajectory[-1].content
        # display(Markdown(content))

        if content is None:
          return "No Element Found"
        else:
          return content

    elif "start" in last_step:
        solution_node = last_step["start"]["root"].get_best_solution()
        best_trajectory = solution_node.get_trajectory(include_reflections=False)
        print("Best solution found:")
        # print(best_trajectory[-1].content)
        content = best_trajectory[-1].content
        # display(Markdown(content))

        if content is None:
          return "No Element Found"
        else:
          return content
    else:
        print("Tree expansion ended \n ")
        solution_node = last_step["expand"]["root"].get_best_solution()
        best_trajectory = solution_node.get_trajectory(include_reflections=False)
        print("Best solution found:")
        # print(best_trajectory[-1].content)
        content = best_trajectory[-1].content
        # display(Markdown(content))

        if content is None:
          return "No Element Found"
        else:
          return content

    # print("Final tree structure:")
    # print_tree(last_step["start"]["root"] if "start" in last_step else last_step["expand"]["root"])


    # print("Final tree structure:")
    # print_tree(last_step["start"]["root"] if "start" in last_step else last_step["expand"]["root"])

#Question: Try to understand the below conversation history and the last message of the Patient. Which DBT element is best for the next response generation based on Your mental health therapist's skill and DBT Skills?
    ##

def testMCTS(question):
    response_val = run_tree_search(question)
    return response_val
