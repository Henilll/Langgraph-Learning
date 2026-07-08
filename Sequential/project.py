import os
from pydantic import BaseModel
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from rich import print
load_dotenv()
# Lets create the state first

# llm
llm=ChatGroq(model='llama-3.3-70b-versatile',temperature=0.7)


class PipelineState(BaseModel):
    raw_input: str
    edited_text: str = ""
    script_text: str = ""
    final_text: str = ""


# Lets Create The Node

def editor_node(state:PipelineState) -> dict:
    """Stage 1: Cleans up grammar, removes typos, and refines the tone."""
    
    prompt=("You are an expert copyeditor.Clean up the following raw text."
             "Fox ant grammatical errors. spelling mistakes, and smooth out the transition flow"
             "While keeping the core message inact. Return only the edited text."

             f"Text:{state.raw_input}"
    )
    response=llm.invoke(prompt)
    
    return {"edited_text":response.content.strip()}

def scriptwriter_node(state: PipelineState) -> dict:
    """Stage 2: Formats The clean text into an engaging video scrip style."""
    print("\n---[Stage 2] Executing Scriptwriter Node ---")

    prompt=(
        "You are a charismatic YouTube content creator. Take this edited text and transform "
        "it into a highly engaging, punchy, conversational video script hook. Make it sound "
        "like a real person speaking passionately. Return only the script content.\n\n"
        f"Edited Text:\n{state.edited_text}"
    )

    response=llm.invoke(prompt)
    return {"script_text": response.content.strip()}

def translator_node(state: PipelineState) -> dict:
    """Stage 3: Translates the script into natural flowing Hinglish."""
    print("\n--- [Stage 3] Executing Hinglish Translator Node ---")
    
    prompt = (
        "You are an expert content localizer for the Indian market. Take the following script "
        "and convert it into natural, flowing 'Hinglish'. Do not simply translate it sentence-by-sentence "
        "or repeat information. Alternating comfortably between Hindi and English phrases just like "
        "an intellectual tech educator would speak naturally on a live stream. Keep the energy high! "
        "Return only the final Hinglish text.\n\n"
        f"Script:\n{state.script_text}"
    )
    
    response = llm.invoke(prompt)
    return {"final_text": response.content.strip()}

# now your state and nodes are ready and now it is time to create the graph
# and for creating the graph you have to connect this node and for that you have
# to use edges
# edges are very important to creat the workflows


from langgraph.graph import StateGraph, START , END

# Create the graph
graph= StateGraph(PipelineState)

# Add the nodes in our graph
 
graph.add_node("editor",editor_node)
graph.add_node("script_writer",scriptwriter_node)
graph.add_node("translator",translator_node)


# Add edges (Sequntial -  one after another)

graph.add_edge(START,"editor")
graph.add_edge("editor","script_writer")
graph.add_edge("script_writer","translator")
graph.add_edge("translator",END)


# Compile The Graph

app= graph.compile()

result=app.invoke({
    "raw_input": "AI agents are the future of tech. They can think, plan, and act on their own. LangGraph helps you build these agents with proper control and memory."
})

# Output
print("Your Result are: -\n\n")

print(result['final_text'])
