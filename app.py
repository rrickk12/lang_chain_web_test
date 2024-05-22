from flask import Flask, request, render_template_string
import warnings
from langchain.llms import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
# Ignore LangChainDeprecationWarning 
warnings.filterwarnings("ignore", category=UserWarning, module="langchain*")
warnings.filterwarnings("ignore")

# OLD
from langchain.llms import openai
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

# New
# from langchain_community.llms import OpenAi

# SECURE THIS KEY!
api_key= 'sk-proj-ZSqZy4cNNwC7xgeehAyxT3BlbkFJm6YeEld5B1KWjz6rDM2N'

llm = openai.OpenAI(
    openai_api_key=api_key
)

code_prompt = PromptTemplate(
    template = "escreva brevemente sobre {language} ",
    input_variables=['language','task']
)

code_chain = LLMChain(
    llm=llm,
    prompt=code_prompt
)

app = Flask(__name__)

# HTML template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>LangChain Prompt</title>
</head>
<body>
    <h1>Escolha um assunto</h1>
    <form method="post">
        <label for="language">Assunto:</label><br>
        <input type="text" id="language" name="language"><br><br>
        <input type="submit" value="Submit">
    </form>
    {% if result %}
        <h2>Result:</h2>
        <p>{{ result }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        language = request.form["language"]
        # Generate text based on user input
        results = code_chain.invoke({
            "language": language,
        })
        result = results
    return render_template_string(html_template, result=result)

if __name__ == "__main__":
    app.run(debug=True)