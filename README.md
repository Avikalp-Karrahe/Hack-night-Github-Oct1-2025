# PromptSwitch 🤖📚

> An AI-powered agent that reads GitHub repositories and generates comprehensive, structured project documentation using prompt chaining and meta-prompting techniques.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🎯 Overview

PromptSwitch Agent is an intelligent documentation generator that analyzes GitHub repositories and creates clean, structured `project_doc.md` files. It leverages advanced AI techniques including:

- **Prompt Chaining**: Sequential AI prompts for comprehensive analysis
- **Meta-Prompting**: Self-improving prompt strategies
- **Context Integration**: Uses prior AI knowledge from `Learn_AI/` directory
- **Modular Architecture**: Separate agents for cloning, parsing, planning, and formatting

## ✨ Key Features

- 🔍 **Smart Repository Analysis**: Automatically detects project type, complexity, and structure
- 📝 **Comprehensive Documentation**: Generates sections for overview, installation, usage, API docs, and more
- 🔗 **Prompt Chaining**: Uses sequential AI prompts for detailed, contextual content
- 🧠 **Self-Learning**: Incorporates AI engineering best practices from knowledge base
- 📊 **Multiple Formats**: Outputs markdown with optional PDF/HTML conversion
- 🛠 **Modular Design**: Clean separation of concerns with dedicated agents
- 🎯 **Claude Prompts Generation**: Creates tailored Claude Desktop prompts for project recreation
- 🔄 **Local & Remote Support**: Works with both GitHub URLs and local directories

## 🏗 Architecture

```
PromptSwitch/
├── main.py                    # Main orchestrator
├── agents/                    # Modular agent components
│   ├── repo_cloner.py        # Repository cloning with GitPython
│   ├── parser.py             # Structure and content analysis
│   ├── doc_planner.py        # Outline generation using meta-prompting
│   ├── section_filler.py     # Content generation via prompt chaining
│   ├── formatter.py          # Document formatting and conversion
│   ├── test_generator.py     # Automated test generation
│   └── review_agent.py       # Quality review and validation
├── prompts/                   # AI prompt templates
│   ├── meta_prompt.txt       # Core behavior and guidelines
│   ├── outline_prompt.txt    # Structure generation prompt
│   ├── section_prompt.txt    # Section-specific content prompt
│   └── system_prompt.txt     # System-level instructions
├── outputs/                   # Generated documentation
│   ├── {project}_documentation.md        # Main documentation
│   ├── {project}_documentation.pdf       # PDF version
│   └── {project}_claude_prompts.md       # Claude Desktop prompts
├── Learn_AI/                  # AI knowledge base
│   └── guide-to-ai-assisted-engineering.pdf
└── Project Docs/              # Project planning and architecture
    ├── 01_plan.md            # Design blueprint
    ├── 02_architecture.mmd   # System diagram
    └── 03_docs.md            # Behavior guide
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git installed on your system
- API keys for AI services (OpenAI/Anthropic)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Avikalp-Karrahe/PromptSwitch.git
   cd PromptSwitch
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.public .env
   # Edit .env with your API keys and preferences
   ```

### Basic Usage

#### Analyze a GitHub Repository
```bash
python main.py https://github.com/username/repository
```

#### Analyze a Local Directory
```bash
python main.py /path/to/local/project
```

#### Advanced Options
```bash
# Custom output directory
python main.py https://github.com/username/repo --output ./custom_output

# Skip tests and review
python main.py https://github.com/username/repo --no-tests --no-review

# Custom prompts directory
python main.py https://github.com/username/repo --prompts-dir ./custom_prompts
```

## 📋 Configuration

### Environment Variables

Copy `.env.public` to `.env` and configure:

```bash
# AI Service Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# PromptSwitch Settings
PROMPTSWITCH_OUTPUT_DIR=./outputs
PROMPTSWITCH_TEMP_DIR=./temp
PROMPTSWITCH_LOG_LEVEL=INFO
PROMPTSWITCH_MAX_RETRIES=3

# Documentation Settings
PROMPTSWITCH_INCLUDE_TOC=true
PROMPTSWITCH_DEFAULT_FORMAT=markdown
PROMPTSWITCH_WORD_LIMIT=10000
```

## 🔧 Advanced Usage

### Programmatic API

```python
from main import PromptSwitchAgent

# Initialize agent
agent = PromptSwitchAgent(output_dir="./outputs")

# Process repository
result = agent.process_repository("https://github.com/username/repo")

# Access generated files
print(f"Documentation: {result['documentation_path']}")
print(f"Claude Prompts: {result['prompts_path']}")
print(f"PDF Version: {result['pdf_path']}")
```

### Custom Prompts

Create custom prompt templates in the `prompts/` directory:

- `meta_prompt.txt`: Core agent behavior
- `outline_prompt.txt`: Documentation structure
- `section_prompt.txt`: Content generation
- `system_prompt.txt`: System instructions

## 📊 Output Files

PromptSwitch generates comprehensive documentation including:

### 📄 Main Documentation
- **Project Overview**: Summary, goals, and key features
- **Technology Stack**: Languages, frameworks, and tools
- **Installation Guide**: Step-by-step setup instructions
- **Usage Examples**: Code samples and tutorials
- **API Documentation**: Detailed API reference
- **Architecture**: System design and components
- **Contributing**: Guidelines for contributors
- **Troubleshooting**: Common issues and solutions

### 🎯 Claude Desktop Prompts
- **Prompt 1**: Project Setup & Architecture Planning
- **Prompt 2**: Core Implementation & Features
- **Prompt 3**: Testing, Deployment & Optimization

### 📋 Additional Outputs
- **PDF Documentation**: Professional formatted version
- **Test Files**: Automated test generation
- **Quality Review**: Comprehensive analysis report
- **Regeneration Blocks**: Improvement suggestions

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_parser.py

# Run with coverage
python -m pytest --cov=agents
```

### Generate Tests
```bash
# Generate tests for a repository
python main.py https://github.com/username/repo --generate-tests
```

## 🔍 Quality Assurance

PromptSwitch includes built-in quality assurance:

- **Automated Testing**: Generates comprehensive test suites
- **Code Review**: AI-powered code quality analysis
- **Documentation Review**: Content quality validation
- **Performance Metrics**: Generation time and accuracy tracking

## 🛠 Development

### Project Structure

- `agents/`: Core processing modules
- `prompts/`: AI prompt templates
- `outputs/`: Generated documentation
- `tests/`: Test suites
- `Learn_AI/`: Knowledge base
- `Project Docs/`: Project documentation

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `python -m pytest`
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting: `black .`
- Add type hints where appropriate
- Write comprehensive docstrings

## 📈 Performance

### Benchmarks

- **Small Projects** (< 50 files): ~2-3 minutes
- **Medium Projects** (50-200 files): ~5-8 minutes
- **Large Projects** (200+ files): ~10-15 minutes

### Optimization Tips

- Use `PROMPTSWITCH_SHALLOW_CLONE=true` for faster cloning
- Set `PROMPTSWITCH_MAX_FILES_TO_ANALYZE` to limit scope
- Enable caching with `PROMPTSWITCH_ENABLE_CACHE=true`

## 🔧 Troubleshooting

### Common Issues

**API Rate Limits**
```bash
# Increase retry delay
PROMPTSWITCH_RETRY_DELAY=5
PROMPTSWITCH_MAX_RETRIES=5
```

**Memory Issues**
```bash
# Reduce file analysis limit
PROMPTSWITCH_MAX_FILES_TO_ANALYZE=100
PROMPTSWITCH_MAX_FILE_SIZE=524288  # 512KB
```

**Timeout Errors**
```bash
# Increase timeout
PROMPTSWITCH_TIMEOUT=600  # 10 minutes
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

Need help? Here's how to get support:

- 🐛 **Issues**: [GitHub Issues](https://github.com/Avikalp-Karrahe/PromptSwitch/issues)
- 📧 **Email**: akarrahe@ucdavis.edu
- 💼 **LinkedIn**: [Connect with Avikalp](https://www.linkedin.com/in/avikalp/)
- 🔗 **GitHub**: [Follow for updates](https://github.com/Avikalp-Karrahe)

## 🙏 Acknowledgments

- Built with advanced AI engineering principles
- Inspired by modern documentation best practices
- Powered by OpenAI and Anthropic AI models
- Designed for developer experience (DX) optimization

## 🚀 What's Next?

- 🔄 **Real-time Updates**: Live documentation synchronization
- 🌐 **Web Interface**: Browser-based documentation generation
- 🔌 **Plugin System**: Extensible architecture for custom processors
- 📱 **Mobile App**: On-the-go documentation generation
- 🤖 **Advanced AI**: GPT-4 and Claude-3 integration

---

**Created by [Avikalp Karrahe](https://github.com/Avikalp-Karrahe)** | **Connect on [LinkedIn](https://www.linkedin.com/in/avikalp/)**

*Generated with ❤️ by PromptSwitch Agent*