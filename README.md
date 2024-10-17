## RAG-Care-Mental-Wellness-Assistant

### Table of Contents
- [Problem Description](#problem-description)
- [Solution Overview](#solution-overview)
- [Technology Stack](#technology-stack)
- [Knowledge Base](#knowledge-base)
- [Ground Truth Generation and Evaluation](#ground-truth-generation-and-evaluation)
- [Ingestion Pipeline](#ingestion-pipeline)
- [Retrieval Evaluation](#retrieval-evaluation)
- [User query rewriting ](#user-query-rewriting )
- [RAG Evaluation](#rag-evaluation)
- [Containerization](#containerization)
- [FlaskAPI](#flaskapi)
- [User Data Collection and Monitoring](#user-data-collection-and-monitoring)
- [CICD Pipeline](#cicd-pipeline)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Potential Enhancements](#potential-enhancements)
- [Acknowledgement](#acknowledgement)

## Problem Description
Traditional methods of retrieving mental health information can be time-consuming and inefficient. This project tackles the complexity of navigating mental health resources, ensuring swift, tailored, and reliable responses to users' queries.

## Solution Overview
- The **RAG-Care-Mental-Wellness-Assistant** project develops a conversational AI system providing accessible mental wellness support, focusing on depression-related issues. 
- Leveraging Retrieval-Augmented Generation (RAG) technology and powered by Large Language Models (LLMs), specifically LLaMA3:8b Gemma2:2b,OpenAI3.5 Turbo and OpenAI4o,  this assistant enables users to interact with trusted mental health resources effectively, while capturing user feedback for continuous improvement.

![image](https://deepgram.com/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F96965%2F1698862153-image4.png&w=1200&q=75) 
Imagecredits :deepgram.com

<h5> Goals </h5>
- Provide Conversational interface mental wellness support by integrating with trusted mental health resources<br/>
- Offer accurate and trustworthy information via RAG technology<br/>
- Foster empathetic and engaging user interactions and Continuously improve through user feedback and model updates<br/>

### Technology Stack
- **Python**: Core programming language.
- **Hugging Face Transformers**: For language model integration.
- **LLaMA Models (LLaMA3:8b & Gemma2:2b)**: For ground truth query generation and evaluation.
- **LLaMA Models (Gemma2 & OpenAI3.5Turbo and OpenAI4o)**: For RAG Flow evaluation and response generation in Flask
- **Pydantic**: Data modeling and validation.
- **Pandas**: Data manipulation and analysis.
- **ElasticSearch**: Vectorstore
- **Flask**: Web application framework.
- **MySQL**: Data storage of user interaction
- **Grafana**: Dashboard
- **Docker**: For containerization and environment management.
- **CI/CD**: Unit/Integration test, GitHub Actions, and CD via AWS.
- **LLM Framework** :Langchain
---

## Section 1: Dataset and Ground Truth Generation  <br/>
(Notebook is in the folder `/notebooks/step0_data_preparation.ipynb`)  <br/>
[Data Preparation Notebook: Step 0](https://github.com/padmapria/RAG-Care-Mental-Wellness-Assistant/blob/master/notebooks/step0_data_preparation.ipynb)
 
### Knowledge Base
- **Counsel Chat Dataset**: A comprehensive dataset of mental health-related conversations.
- **Source**: Utilizes the [Counsel Chat Dataset](https://huggingface.co/datasets/nbertagnolli/counsel-chat) from Hugging Face.
- **Focus**: Data related to **depression**.
- **Processing**: Only questions with depression as the topic and titles longer than 20 characters are included.

### Ground Truth Generation and Evaluation
- **LLaMA3** and **Gemma2 models** are utilized for generating high-quality ground truth data, ensuring that the response is accurate and relevant to mental wellness queries on depression.
- Ground truth data is evaluated before testing with RAG. **LLaMA3** evaluates the quality of queries generated by **Gemma2**, and vice versa, to ensure robustness and relavence of the query.
![ground truth](images/ground_truth.jpg)
---

## Section 2: RAG Flow and Evaluation   <br/>
(Notebook in the folder `/notebooks/step1_data_preparation.ipynb`) <br/>
[RAG Test Notebook: Step 1](https://github.com/padmapria/RAG-Care-Mental-Wellness-Assistant/blob/master/notebooks/step1_rag_test.ipynb)

**RAG Pipeline** <br/>
![RAG Flow](images/rag_pipeline.jpg)
Imagecredits :https://medium.com/@drjulija/what-is-retrieval-augmented-generation-rag-938e4f6e03d1

### Ingestion Pipeline
- Integrates the Counsel Chat Dataset knowledge base and **LLaMA3:8b, OpenAI API, Gemma2:2b models** LLM models
- Utilizes a semi-automated Jupyter Notebook **Jupyter Notebook (step0)** for data ingestion and preparation.

### Indexing and Storing the data
 **VectorStore**: The project employs **Elasticsearch** as a VectorStore, indexing mental health data for rapid question-answer pair retrieval via vector similarity searches.
 
### Retrieval Evaluation
The system evaluates retrieval performance using:
- Text Search: `minsearch_search` 
- Vector Search: `question_answer_vector_knn` 
- Hybrid Search(vector + text search): `question_answer_vector_knn_combined` 

<b> Evaluation Metrics </b>
- **Hit Rate**: Measures the proportion of relevant documents retrieved.
- **Mean Reciprocal Rank (MRR)**: Assesses the ranking quality of retrieved documents.

### User query rewriting 
This project employs advanced query rewriting capabilities with OpenAI 3.5 Turbo API  to enhance user experience.<br/>
<br/>
<b>How it Works </b><br/>
- User Input: User submits a query.<br/>
- Query Rewriting: OpenAI 3.5 Turbo API rewrites the query.<br/>
- Optimized Query: The rewritten query is sent to the RAG model.<br/>
  <br/>
<b>Benefits</b><br/>
- Improved query accuracy<br/>
- Enhanced search results<br/>
- Better user experience<br/>
- Increased relevance of mental health resources<br/>
  
### RAG Evaluation
- The RAG flow is evaluated using **Gemma2** and **OpenAI4o** as LLM judges for:
![Evaluation](images/rag_evaluation.jpg)
Imagecredits :(https://cobusgreyling.medium.com/steps-in-evaluating-retrieval-augmented-generation-rag-pipelines-7d4b393e62b3) <br/>
- Evaluation criteria:
    - Relvevence of LLM generated answer against true answer
    - Relvevence of LLM generated answer against the question
 ![RAG Flow](images/RAG_flow.jpg)
---

## Section 3: Interface  <br/>
### Containerization
- The entire system is containerized using **Docker** and managed via **docker-compose** to ensure ease of deployment.
- The **docker-compose.yml** file is present in the root directory of the project. It defines services for:
  - **ElasticSearch**: For indexing and searching the mental health-related data.
    - The **vectorstore index** are created during the container initialization.
  - **Grafana**: For monitoring and analytics, with a pre-configured dashboard.
    - The **Grafana JSON** file is automatically uploaded during container initialization for immediate use.
  - **Python**: For running the Flask application and RAG logic.
  - **MySQL**: For user interaction data management.
     - The **SQL Tables** are created during the container initialization.
    
        ![docker](images/docker_containers.jpg)
  <br/>
- The Docker setup also includes **unit and integration tests** to ensure the functionality and stability of the system:
  - **Unit tests**: For verifying individual components of the system.
  - **Integration tests**: For testing the interaction between different components (e.g., Flask, ElasticSearch, etc.).
  - Tests are automatically triggered during the CI/CD pipeline.
   
---
### FlaskAPI
*(Source code in the folder `/services/app`)*  
[app](https://github.com/padmapria/RAG-Care-Mental-Wellness-Assistant/blob/master/services/app)
- A web application built with **Flask**.
- The application provides the following functionalities:
  - **Query Processing**: Accepts user queries and rewrites them to optimize search results.
  - **Vector Store Search**: Searches the vector store to retrieve relevant answers.
  - **LLM Integration**: Utilizes two Large Language Models (LLMs):
    - **Generator LLM**: Retrieves answers from the vector store.
    - **Evaluator LLM**: Calculates the effectiveness of the retrieved answer and provides relevance explanations using OpenAI LLM.
      - Endpoint: `http://localhost:5000/ask`
         <br/>
        ![ask](images/ask.jpg)
  - **Feedback Processing**: Accepts feedback for every query.
      - Endpoint: `http://localhost:5000/feedback`
         <br/>
        ![feedback](images/feedback.jpg)
  - **Listing Recent Questions**: Shows the last 5 questions from the user.
      - Endpoint: `http://localhost:5000/recent_questions`
         <br/>
    ![recent_questions](images/recent_questions.jpg)
---

### User Data Collection and Monitoring
*(Init.sql configuration is located in the folder `/services/app/mysql`)*  
[mysql](https://github.com/padmapria/RAG-Care-Mental-Wellness-Assistant/blob/master/services/mysql) 
- **User Feedback Collection**: Tracks user interaction and feedback with MySQL.
    - MySQL Access: `http://localhost:3306`
      <br/>
- **Monitoring Dashboard**: Provides insights into system performance and user activity.
  - *(Dashboard.json configuration is located in the folder `/services/app/grafana`)*
  - [grafana](https://github.com/padmapria/RAG-Care-Mental-Wellness-Assistant/blob/master/services/grafana) 
- The application also integrates **Grafana**, a monitoring and visualization tool. Grafana allows users to track performance metrics of the RAG model and the underlying infrastructure, ensuring that the application operates efficiently.
  - Grafana dashboard can be accessed from:
    - `http://localhost:3000`
       <br/>
    ![Dashboard](images/grafana.jpg)
---

## Section 4: Testing and Cloud Deployment  <br/>
- **Testing**: Unit and integration test cases are located in the `/services/app/tests` [tests](https://github.com/padmapria/RAG-Care-Mental-Wellness-Assistant/blob/master/services/app/tests) directory. These tests ensure the functionality and reliability of the application.

#### GitHub Actions Workflow
The following GitHub Actions workflow is defined in the `.github/workflows/ci-cd.yml` file: [GitHub Actions Workflow: CI/CD Pipeline](https://github.com/padmapria/RAG-Care-Mental-Wellness-Assistant/blob/master/.github/workflows/rag_care_ci_cd.yml)
- Every GitHub push triggers the CI/CD pipeline.

### CICD Pipeline

Our project utilizes a robust CI/CD pipeline to ensure continuous integration and deployment. This process is managed using **GitHub Actions** and is triggered by every push to the `master` branch as well as pull requests targeting the `master` branch.

![CI/CD](images/cicd.jpg)
##### Steps

1. **Triggering the Pipeline**: 
   - The CI/CD pipeline is initiated on every push or pull request to the `master` branch to ensure that all changes are validated before merging.

2. **Checkout Code**: 
   - The pipeline checks out the latest code from the repository, allowing access to the current version for the workflow.

3. **Set Up Python Environment**: 
   - A Python environment is set up using the specified version (e.g., `3.8`) to ensure compatibility with the project.

4. **Install Dependencies**: 
   - All required Python packages are installed using the `requirements.txt` file, ensuring that the necessary dependencies are available for the application.

5. **Run Tests**: 
   - The pipeline runs unit and integration tests located in the `/services/app/tests` directory. This validates the functionality and reliability of the application.

6. **Change Directory Back to Root**: 
   - The workflow changes back to the root directory to prepare for subsequent Docker operations.

7. **Uninstall Requirements**: 
   - Dependencies are uninstalled to maintain a clean environment, preventing conflicts in future builds.

8. **Start Docker Services**: 
   - The pipeline starts the Docker services defined in the `docker-compose.yml` file, which includes the application, MySQL, ElasticSearch, and Grafana.

9. **Check Services Status**: 
   - The workflow checks if the services are up and running. It waits for a maximum of 10 attempts (with a 5-second interval) to confirm the services are operational.

10. **Tear Down Docker Services**: 
    - After the tests are completed, the workflow tears down the Docker services to free up resources.

11. **Log in to AWS ECR**: 
    - The pipeline logs into Amazon Elastic Container Registry (ECR) using AWS CLI, allowing the subsequent push of the Docker image.

12. **Build Docker Image**: 
    - A Docker image for the application is built, containing the latest code and dependencies.

13. **Tag and Push Docker Image to ECR**: 
    - The newly built Docker image is tagged with the ECR registry URL and pushed to ECR for deployment.

14. **Deploy to AWS ECS**: 
    - Finally, the updated application is deployed to AWS Elastic Container Service (ECS), ensuring the latest version is running in the cloud.

This automated CI/CD pipeline enhances the reliability and speed of our development process by continuously integrating and deploying code changes. <br/>
<br/>
**Note:** Continuous Deployment (CD) Testing Pending <br/>
The Continuous Integration (CI) part of this workflow has been successfully implemented and tested. However, thorough testing of the Continuous Deployment (CD) section is still pending to ensure reliable performance.<br/>

![CI/CD](images/cicd_complete.jpg)
---

## Setup Instructions
**LLM Setup**:  <br/>
**Note:** OpenAI immediately revokes the API key once it detects that the key has been exposed publicly. Therefore, do not expose your API key.<br/>
Generate your OpenAI API key here: [Click Here](https://platform.openai.com/account/api-keys)

**Note:** Download the LLaMA 3 model (8B) and gemma2:2b from the ollama website and Install the OLLAMA server by following the instructions <br/>
https://ollama.com/blog/llama3 <br/>
https://ollama.com/blog/gemma2 <br/>

<b> Starting the ollama: </b> <br/>
Start the OLLAMA server by running the command 'ollama serve' in your terminal <br/>
By default ollama server runs in the port (11434)<br/>

<b> Steps to run the project: </b> <br/>
1. Clone this git repository from command prompt<br/>
git clone https://github.com/padmapria/RAG-Care-Mental-Wellness-Assistant.git    
cd RAG-Care-Mental-Wellness-Assistant  

2. Create a `.env` file and  Store the key as follows, in both the 'app' folder and in the notebooks folder.     
OPENAI_API_KEY=YOUR_API_KEY_HERE<br/>

3. Use Anaconda to create a conda environment and install the requirements.txt by running the following command
```
pip install -r requirements.txt
```
4. Run **Jupyter Notebook (notebooks folder)** for data ingestion and processing, RAG evaluation

5. Install Docker Desktop and use the below command to start the end-to-end Flask-based RAG application
```
docker compose up -d
```
6. Verify the status of docker container, Check if the container is up and running
   ![docker](images/docker_containers.jpg)
   
### Usage
1.Accessing the Flask API Application
 -  Open Postman and navigate to [http://localhost:5000](http://localhost:5000)
2. Input mental wellness-related queries.
3. Receive personalized guidance and support from trusted mental health resources.
   - Sample JSON for testing: [Sample Json to test Flask App](https://github.com/padmapria/RAG-Care-Mental-Wellness-Assistant/blob/master/RAG_Mental_wellness_RestAPI_sample.postman_collection.json)
4.  Monitoring with Grafana <br/>
    Access the Grafana dashboard via browser from: <br/>
    - `http://localhost:3000`
    - Username: admin
    - Password: admin
5. Database Access <br/>
     MySQLDB can be accessed via MySQLWorkbench or dbeaver with the following credentials <br/>
    - db: rag_db
    - host: localhost
    - port :3306
    - Username: root
    - Password: root_pass
      
---
### Potential Enhancements
- Standardized Prompts: Standardize prompts in the workflow to enhance consistency and clarity. (sometimes llama3 gives json output for some inputs)
- Model Ensemble: Combine model outputs for improved performance.
- Continuous Deployment (CD) Testing: Conduct thorough testing of the CD section in the GitHub workflow to ensure reliable performance.
- Logging and Exception Handling: Integrate comprehensive logging throughout the codebase and Improve exception handling to enhance code reliability and stability.
---

### Acknowledgement
I would like to extend my gratitude to the following individuals and organizations for their valuable resources and contributions:
- Alexey Grigorev's expertise and community resources for informative guidance. https://alexeygrigorev.com/
- OpenAI, Meta AI, and Google for providing access to their LLM models and APIs (OpenAI API, LLaMA3, and Gemma2)..

---
