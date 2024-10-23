# Calculator Agent Example

This repository provides a sample implementation of a Calculator Agent built using LangChain and FastAPI. The purpose of this agent is to demonstrate how to build a modular, multi-thread safe agent that can evaluate mathematical expressions. The following sections will guide you through the code structure, its components, and the development practices used.

For development the agents backend can be built using any method or framework wanted by the developer. The only restriction is that the agent must be able to contacted and fully functional throught the endpoints provided in this example as well as the documentation.

For further clarification see the documentation or message the developers.

## Project Structure

- `CalculatorAgent.py`: Contains the core logic of the Calculator Agent, including the setup of the agent, definition of tools, and handling user queries.
- `CalculatorClient.py`: Implements the FastAPI application to expose the Calculator Agent functionalities via RESTful APIs.

## Quickstart Guide

### 1. Create a .env file

Within the .env format it as follows:

```bash
OPENAI_API_KEY = "<YOUR API KEY>"
```

### 2. Run the client via uvicorn

Run the client via uvicorn using the following command:

```bash
uvicorn CalculatorClient:app --reload
```

### 3. Access the clients endpoints via REST API

```bash
POST /activate
```

The activate endpoint will activate the agent for the current user

```
    Payload:
        {
            "user_id":"<USER_ID>"
        }
```

---

```bash
POST /execute
```

The execute endpoint will execute the agents core functionality and return the response from the agent to the core application

```
    Payload:
        {
            "input_text":"<INPUT_TEXT>"
            "user_id":"<USER_ID>"
        }
```

## CalculatorAgent.py

This file defines the calculator functionality and sets up the agent using LangChain's tools. It also handles user input and generates a response from the agent.

### Key Components

1. **Import Statements**

   - Various libraries and modules are imported, including `langgraph`, `langchain`, `logging`, and `dotenv`. These help set up the agent, manage tools, and handle logging.

2. **Logging Configuration**

   - Configures logging to store debug messages and errors in `calculator.log`. This ensures that issues can be easily traced and monitored.

   ```python
   logging.basicConfig(
       filename='calculator.log',
       level=logging.DEBUG,
       format='%(asctime)s - %(levelname)s - %(message)s'
   )
   ```

3. **Environment Variable Loading**

   - Uses `load_dotenv()` to load API keys and other sensitive information from environment variables, keeping the configuration secure.

   ```python
   load_dotenv()
   ```

4. **Initialize the Language Model**

   - The OpenAI language model is initialized globally, as it is thread-safe and can be reused across multiple requests.

   ```python
   llm = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'), model='gpt-4')
   ```

5. **Calculator Function**

   - Defines the core calculator logic to evaluate mathematical expressions using Python's `eval()`. Safety precautions limit the execution environment to prevent security risks.

   ```python
   def calculator(input_expression: str) -> str:
       try:
           result = eval(input_expression, {"__builtins__": None}, {})
           return str(result)
       except Exception as e:
           return f"Error: {str(e)}"
   ```

6. **Creating the Calculator Tool**

   - Wraps the calculator function into a LangChain `Tool` object, allowing it to be easily integrated into the agent workflow.

   ```python
   calculator_tool = Tool.from_function(calculator, name="Calculator", description="Answer a math question based on the given query.")
   ```

7. **Agent Setup**

   - Combines the language model and the calculator tool to create a `ReACT`-based agent using `create_react_agent`.

   ```python
   agent = create_react_agent(llm, tools=[calculator_tool])
   ```

8. **Processing User Input**
   - Provides a function `calculator_agent` that accepts user input, passes it to the agent, and retrieves the processed response. It includes error handling and logs relevant information.
   ```python
   def calculator_agent(user_input):
       ...
       return ai_response
   ```

## CalculatorClient.py

This file creates a FastAPI server to provide an interface for users to interact with the Calculator Agent via RESTful APIs.

### Key Components

1. **Import Statements**

   - Imports FastAPI, Pydantic models, and the calculator agent to set up the web service.

2. **FastAPI Initialization**

   - Initializes the FastAPI app, including metadata like the title, description, and version.

3. **Data Models**

   - Defines request and response models using Pydantic, ensuring the API data is well-structured.

   ```python
   class QueryRequest(BaseModel):
       user_id: str
       input_text: str

   class QueryResponse(BaseModel):
       response: str
   ```

4. **Endpoint: `/execute`**

   - Provides an endpoint that accepts a user query, processes it through the `calculator_agent`, and returns the result. Handles errors gracefully with appropriate HTTP status codes.

   ```python
   @app.post("/execute", response_model=QueryResponse)
   def query_agent(request: QueryRequest):
       ...
       return QueryResponse(response=response)
   ```

5. **Endpoint: `/activate`**
   - Demonstrates how to activate the agent for a specific user. In this example, it sends a message confirming that the agent is ready to handle requests.
   ```python
   @app.post("/activate")
   def activate(request: ActivateRequest):
       ...
       return {"message":f"Ready to handle traffic for User: {user_id}"}
   ```

## Development Notes

1. **Thread-Safety**

   - Ensure that functions and methods are thread-safe. The agent, as designed, is thread-safe, which is crucial for a multi-user environment.

2. **Logging and Monitoring**

   - Logging is implemented to capture debug information and errors. This practice helps in identifying and resolving issues promptly.

3. **Environment Variables**
   - Sensitive data (e.g., API keys) should be stored securely using environment variables, following best security practices.
