# LeadGen

A Python application for lead generation with a multi-step questioning process using Pydantic AI and Groq LLM.

## Overview

LeadGen is an industry-level Python application that helps businesses create detailed Ideal Customer Profiles (ICPs) through a structured questioning process. The application uses advanced AI capabilities from Pydantic AI and Groq LLM to generate personalized questions and extract valuable insights from user responses.

### Process Flow

1. **Default Questions Stage**: Ask the user 5 default questions to gather basic information about their business and target customers.
2. **Personalized Questions Stage**: Generate 10 personalized questions based on the initial answers using Pydantic AI and Groq LLM.
3. **Keyword Generation Stage**: Generate relevant keywords for lead generation based on all questions and answers.
4. **ICP Generation Stage**: Create a comprehensive Ideal Customer Profile based on all collected data.

## Installation

### Prerequisites

- Python 3.8 or higher
- Groq API key (get one from [console.groq.com/keys](https://console.groq.com/keys))

### Setup

1. Clone the repository:

```bash
git clone https://github.com/
cd leadgen
```

2. Install the package:

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
```

Edit the `.env` file and add your Groq API key.

## Usage

### Running the Application

To run the full lead generation pipeline:

```bash
python main.py
```

This will guide you through the entire process, from answering default questions to generating an Ideal Customer Profile.

### Using as a Library

You can also use LeadGen as a library in your own Python code:

```python
from leadgen.pipeline.lead_gen_pipeline import LeadGenPipeline

# Initialize the pipeline
pipeline = LeadGenPipeline()

# Run the default questions stage
default_questions = pipeline.run_default_questions_stage()
# ... get answers from user ...
pipeline.process_default_answers(answers)

# Run the personalized questions stage
personalized_questions = pipeline.run_personalized_questions_stage()
# ... get answers from user ...
pipeline.process_personalized_answers(answers)

# Generate keywords
keywords = pipeline.run_keyword_generation_stage()

# Generate ICP
icp = pipeline.run_icp_generation_stage()

# Save the session
session_file = pipeline.save_session()
```

## Project Structure

```
leadgen/
├── config/                  # Configuration files
│   ├── config.yaml          # Main configuration
│   ├── params.yaml          # Application parameters
│   ├── prompts.yaml         # System prompts for agents
│   └── schema.yaml          # Data schema definitions
├── src/
│   └── leadgen/             # Main package
│       ├── agents/          # AI agents for different stages
│       ├── config/          # Configuration loading
│       ├── constants/       # Application constants
│       ├── entity/          # Data models
│       ├── models/          # Model definitions
│       ├── pipeline/        # Pipeline orchestration
│       ├── services/        # Services (e.g., LLM service)
│       └── utils/           # Utility functions
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore file
├── main.py                  # Main entry point
├── README.md                # This file
├── requirements.txt         # Dependencies
└── setup.py                 # Package setup
```

## Configuration

The application uses YAML files for configuration:

- `config.yaml`: Main configuration settings
- `params.yaml`: Application parameters, including default questions
- `prompts.yaml`: System prompts for different agents
- `schema.yaml`: Data schema definitions

## Development

### Adding New Features

1. Create a new module in the appropriate directory
2. Update the pipeline to include the new feature
3. Update configuration files as needed

### Running Tests

```bash
pytest
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.