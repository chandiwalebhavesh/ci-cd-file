from github import Github
import openai

# Your GitHub Personal Access Token or GitHub OAuth token
# Generate a token with appropriate permissions: repo, workflow
# For security reasons, it's better to use environment variables to store the token
ACCESS_TOKEN = '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'

# Repository owner and name
repo_owner = 'your_github_username'
repo_name = 'your_repo_name'

# Define the prompt to generate the YAML file
prompt = """Give me a yaml  code for GitHub Actions workflow used for deploying a web application to
 AWS App Runner service in different environments (development, staging, and production). 
 Here's a breakdown of its main components:

1. Events Triggering Deployment: The workflow is triggered by `push` events to the `newui_master` branch 
and `pull_request` events targeting the same branch.
2. Environment Variables: Several environment variables are defined, such as `AWS_REGION`, `ECR_REPOSITORY`, 
and the names of different App Runner services for development, staging, and production.
3. Permissions: The workflow sets permissions to read the repository's contents.
4. Jobs: The workflow has three jobs: `DeployDev`, `DeployPreProd`, and `DeployProd`. Each job represents
 a deployment to a different environment.
5. Steps: Each job consists of multiple steps to perform the deployment:
 a. Checkout: Checks out the repository code.
 b. Configure AWS credentials: Configures AWS credentials using secrets stored in the GitHub repository.
 c. Login to Amazon ECR: Authenticates Docker with the Amazon Elastic Container Registry (ECR).
 d. Build, tag, and push image to Amazon ECR: Builds a Docker container, tags it with the current commit SHA, 
 and pushes it to the ECR repository.
 e. Deploy to App Runner: Deploys the Docker image to the AWS App Runner service using the specified 
 configuration.
 f. App Runner output: Displays the output or status of the App Runner deployment.
6. Conditionals: Some steps are conditional based on the `if` statements. For example, the `DeployDev` 
job runs only when the event is a pull request, and the `DeployPreProd` job runs only when the branch is 
`newui_master`.

"""

def create_or_update_workflow_file(repo, file_path, content):
    try:
        # Check if the workflow file already exists
        existing_file = repo.get_contents(file_path)

        # Update the existing file with the new content
        repo.update_file(file_path, "Updating workflow file",
                 content, existing_file.sha)
        print(f"Workflow file '{file_path}' updated successfully!")
    except Exception as e:
        # If the file does not exist, create a new one
        repo.create_file(file_path, "Creating workflow file", content)
        print(f"Workflow file '{file_path}' created successfully!")

def main():
    # Connect to the GitHub API using the access token
    g = Github(ACCESS_TOKEN)

    # Get the repository
    repo = g.get_repo(f"{repo_owner}/{repo_name}")

    # File path where the workflow will be created or updated
    workflow_file_path = '.github/workflows/main.yml'

    # Request the model to generate the YAML file
    openai.api_key = 'your-openai-api-key'
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1000,
        n=1,
        stop=None,
        echo=True
    )

    # Extract the generated YAML from the response
    yaml_file = response.choices[0].text.strip()

    # Call the function to create or update the workflow file
    create_or_update_workflow_file(repo, workflow_file_path, yaml_file)

if __name__ == "__main__":
    main()
