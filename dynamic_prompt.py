from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import streamlit as st
load_dotenv()

llm=HuggingFaceEndpoint(repo_id="Qwen/Qwen3-Coder-Next",task="text-generation")

model=ChatHuggingFace(llm=llm)

st.header('Research tool')

paper_input= st.selectbox("select name= ",["Attention is all you need",'BERT','GPT-3','Difussion model'])

style_input=st.selectbox("select explainatiob style",['Begginer friendly','Technical','Code-Oriented','Mathematical'])

length_input=st.selectbox("select explaination length",['Short (1-2 paragraphs)','Medium (3-4 paragraphs)','Long (detaqiled explaination)'])

template=PromptTemplate(
    template="""
    Please summarize the research paper titled "{paper_input}" with the following specifications:
Explanation Style: {style_input}
Explanation Length: {length_input}

1. Mathematical Details:
-Include relevant mathematical equations if present in the paper.
-Explain the mathematical concepts using simple, intuitive code snippets where applicable.

2. Analogies:

-Use relatable analogies to simplify complex ideas.
If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.
Ensure the summary is clear, accurate, and aligned with the provided style and length.""",input_variables=['paper_input', 'style_input','length_input']
)

prompt=template.invoke({
    'paper_input':paper_input,
    'style_input':style_input,
    'length_input':length_input
})

if st.button('Summarize'):
    result=model.invoke(prompt)
    st.write(result.content)



