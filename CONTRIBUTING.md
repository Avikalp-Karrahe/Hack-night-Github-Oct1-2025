# 🤝 Contributing to PromptSwitch

Thank you for your interest in contributing to PromptSwitch! We welcome contributions from the community and are excited to see what you'll bring to this AI-powered documentation generation project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Architecture](#project-architecture)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Voice Integration](#voice-integration)
- [Areas for Contribution](#areas-for-contribution)
- [Plugin Development](#plugin-development)

## 📜 Code of Conduct

By participating in this project, you agree to abide by our code of conduct:

- **Be respectful** and inclusive to all contributors
- **Be collaborative** and constructive in discussions
- **Be patient** with newcomers and provide helpful guidance
- **Focus on the issue**, not the person
- **Respect different perspectives** on AI and documentation approaches

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of Python, AI/ML concepts, and documentation generation
- Understanding of prompt engineering and AI agent architectures
- Familiarity with GitHub API and repository structures

### Optional Prerequisites for Voice Features

- Knowledge of speech recognition APIs (OpenAI Whisper, Google Speech-to-Text)
- Understanding of audio processing libraries (librosa, pydub)
- Experience with real-time audio streaming

### Development Setup

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/PromptSwitch.git
   cd PromptSwitch
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/Avikalp-Karrahe/PromptSwitch.git
   ```

4. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Set up environment**
   ```bash
   cp .env.example .env
   # Add your API keys to .env (OpenAI, Anthropic, etc.)
   ```

7. **Test installation**
   ```bash
   python main.py --help
   ```

## 🏗️ Project Architecture

### Core Components

```
PromptSwitch/
├── main.py                 # Main application entry point
├── agents/                 # AI agent modules
│   ├── cloner.py          # Repository cloning agent
│   ├── parser.py          # Repository parsing agent
│   ├── doc_planner.py     # Documentation planning agent
│   ├── section_filler.py  # Content generation agent
│   ├── formatter.py       # Document formatting agent
│   ├── test_generator.py  # Test generation agent
│   ├── review_agent.py    # Quality review agent
│   └── validator.py       # Output validation agent
├── plugins/               # Plugin system
│   ├── base_plugin.py     # Base plugin class
│   ├── plugin_manager.py  # Plugin management
│   └── builtin/          # Built-in plugins
├── prompts/              # Prompt templates
├── outputs/              # Generated documentation
└── voice/                # Voice integration (future)
    ├── speech_to_text.py # Speech recognition
    ├── audio_processor.py # Audio processing
    └── voice_prompts.py  # Voice-to-prompt conversion
```

### Agent Pipeline

1. **Repository Cloner**: Downloads and prepares repositories
2. **Repository Parser**: Analyzes structure, dependencies, and code
3. **Document Planner**: Creates intelligent documentation outlines
4. **Section Filler**: Generates content using prompt chaining
5. **Document Formatter**: Structures content into clean markdown
6. **Test Generator**: Creates relevant test cases
7. **Review Agent**: Performs quality assurance
8. **Output Validator**: Ensures output quality and completeness

## 🔄 Making Changes

### Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or for voice features:
   git checkout -b voice/speech-recognition-integration
   ```

2. **Make your changes**
   - Follow existing code patterns and architecture
   - Add comprehensive docstrings and comments
   - Consider AI agent interactions and prompt flows
   - Test with multiple repository types

3. **Test your changes**
   ```bash
   # Run linting
   flake8 .
   
   # Run type checking
   mypy .
   
   # Test with sample repositories
   python main.py https://github.com/octocat/Hello-World
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat(agents): add enhanced repository analysis"
   ```

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature (agent, plugin, voice integration)
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `voice`: Voice-related features
- `prompt`: Prompt engineering improvements

**Scopes:**
- `agents`: AI agent modifications
- `plugins`: Plugin system changes
- `prompts`: Prompt template updates
- `voice`: Voice integration features
- `core`: Core application logic
- `config`: Configuration changes

**Examples:**
```
feat(agents): add support for Rust project analysis
fix(plugins): resolve plugin loading race condition
voice(core): implement speech-to-text integration
prompt(templates): enhance code documentation prompts
```

## 🔀 Pull Request Process

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Use our PR template
   - Provide clear description of AI agent changes
   - Include example outputs or prompt improvements
   - Link related issues
   - Add screenshots for UI changes

4. **Review Process**
   - Code review by maintainers
   - AI agent testing with various repositories
   - Prompt quality assessment
   - Address feedback and iterate
   - Approval and merge

### Pull Request Template

```markdown
## 📝 Description
Brief description of changes and AI improvements

## 🔗 Related Issues
Fixes #123

## 🤖 AI Agent Changes
- [ ] New agent functionality
- [ ] Prompt improvements
- [ ] Plugin enhancements
- [ ] Voice integration features

## 🧪 Testing
- [ ] Tested with Python repositories
- [ ] Tested with JavaScript repositories
- [ ] Tested with multi-language repositories
- [ ] Voice features tested (if applicable)
- [ ] Plugin system tested
- [ ] Output quality verified

## 📊 Performance Impact
- [ ] No significant performance degradation
- [ ] Memory usage within acceptable limits
- [ ] API rate limits respected

## 📸 Screenshots/Examples
(Generated documentation examples, voice integration demos)

## ✅ Checklist
- [ ] Code follows project conventions
- [ ] Docstrings added/updated
- [ ] Prompt templates validated
- [ ] Self-review completed
- [ ] Documentation updated
```

## 💻 Coding Standards

### Python Code Style

- Follow PEP 8 style guidelines
- Use type hints for all functions and methods
- Write comprehensive docstrings
- Use meaningful variable and function names
- Keep functions focused and modular

```python
# Good
from typing import Dict, List, Optional, Any
from pathlib import Path

class RepositoryAnalyzer:
    """Analyzes repository structure and generates insights."""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.supported_languages = ['python', 'javascript', 'java']
    
    def analyze_dependencies(self, repo_path: Path) -> Dict[str, List[str]]:
        """Extract and categorize project dependencies.
        
        Args:
            repo_path: Path to the repository root
            
        Returns:
            Dictionary mapping dependency types to lists of packages
        """
        dependencies = {}
        # Implementation here
        return dependencies

# Avoid
def analyze(path):  # Missing types and docstring
    deps = {}  # Unclear variable name
    return deps
```

### AI Agent Development

- Each agent should inherit from a base agent class
- Implement proper error handling and fallbacks
- Use structured logging for debugging
- Design agents to be stateless when possible

```python
from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

class BaseAgent(ABC):
    """Base class for all PromptSwitch agents."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.logger = logging.getLogger(f"promptswitch.{name}")
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results."""
        pass
    
    def handle_error(self, error: Exception, context: str) -> Dict[str, Any]:
        """Handle errors gracefully with fallback content."""
        self.logger.error(f"Error in {context}: {error}")
        return {"error": str(error), "fallback_used": True}
```

### Prompt Engineering

- Use clear, specific instructions in prompts
- Include examples and context
- Design prompts for consistency and quality
- Test prompts with various repository types

```python
# Good prompt template
SYSTEM_PROMPT = """
You are a Senior Technical Writer and Software Architect.
Analyze the provided repository and generate comprehensive documentation.

Context:
- Repository: {repo_name}
- Primary Language: {primary_language}
- Project Type: {project_type}

Requirements:
1. Write clear, professional documentation
2. Include practical examples
3. Focus on developer experience
4. Maintain consistent tone and structure

Output Format: Structured Markdown with proper headings
"""
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] **Core Functionality**: All agents work as expected
- [ ] **Repository Types**: Test with Python, JavaScript, Java, Go projects
- [ ] **Error Handling**: Graceful failure with meaningful messages
- [ ] **Output Quality**: Generated documentation is accurate and useful
- [ ] **Performance**: Reasonable processing times for various repo sizes
- [ ] **Plugin System**: Plugins load and execute correctly
- [ ] **Voice Features**: Speech recognition and processing work (if implemented)

### Testing Commands

```bash
# Lint code
flake8 . --max-line-length=88 --extend-ignore=E203,W503

# Type checking
mypy . --ignore-missing-imports

# Run with test repository
python main.py https://github.com/octocat/Hello-World --output-name test_run

# Test plugin system
python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); pm.discover_plugins()"

# Test voice features (when implemented)
python -m voice.speech_to_text --test-audio sample.wav
```

### Integration Testing

```bash
# Test with various repository types
./test_repositories.sh

# Test plugin compatibility
./test_plugins.sh

# Performance benchmarking
./benchmark_agents.sh
```

## 🎤 Voice Integration

### Overview

PromptSwitch is expanding to support voice-to-prompts functionality, allowing users to:
- Speak repository analysis requests
- Generate documentation through voice commands
- Create custom prompts via speech input
- Control the documentation generation process hands-free

### Voice Architecture

```python
# voice/speech_to_text.py
class SpeechToTextProcessor:
    """Converts speech input to text for prompt generation."""
    
    def __init__(self, provider: str = "openai_whisper"):
        self.provider = provider
        self.supported_formats = ['.wav', '.mp3', '.m4a', '.flac']
    
    def transcribe_audio(self, audio_file: Path) -> str:
        """Transcribe audio file to text."""
        pass
    
    def process_real_time(self, audio_stream) -> str:
        """Process real-time audio stream."""
        pass

# voice/voice_prompts.py
class VoicePromptGenerator:
    """Converts voice commands to structured prompts."""
    
    def parse_voice_command(self, transcribed_text: str) -> Dict[str, Any]:
        """Parse voice command into structured prompt."""
        pass
```

### Voice Command Examples

```
# Repository Analysis
"Analyze the React repository at github.com/facebook/react and focus on the component architecture"

# Custom Documentation
"Generate API documentation for the Python project in my current directory, include usage examples"

# Plugin Control
"Enable the notion publisher plugin and generate documentation for the machine learning project"

# Voice Prompts
"Create a prompt for documenting microservices architecture with emphasis on deployment strategies"
```

### Voice Integration Guidelines

1. **Audio Processing**
   - Support multiple audio formats (WAV, MP3, M4A, FLAC)
   - Implement noise reduction and audio enhancement
   - Handle various microphone qualities and environments

2. **Speech Recognition**
   - Use robust STT services (OpenAI Whisper, Google Speech-to-Text)
   - Implement fallback mechanisms for recognition failures
   - Support multiple languages and accents

3. **Command Parsing**
   - Design natural language command parsing
   - Handle ambiguous or incomplete voice commands
   - Provide voice feedback for confirmation

4. **Integration Points**
   - Voice input for repository URLs and paths
   - Spoken configuration of documentation preferences
   - Voice control of the agent pipeline
   - Audio feedback for process status

### Voice Development Setup

```bash
# Install voice dependencies
pip install openai-whisper speechrecognition pydub librosa

# For real-time processing
pip install pyaudio sounddevice

# Test voice setup
python -m voice.test_setup
```

## 🎯 Areas for Contribution

### 🌟 High Priority

- **Voice Integration**: Speech-to-text and voice command processing
- **Agent Improvements**: Enhanced repository analysis and content generation
- **Prompt Engineering**: Better prompts for specific project types
- **Performance Optimization**: Faster processing and reduced API calls
- **Error Handling**: More robust error recovery and user feedback

### 🔧 Feature Additions

- **Multi-language Support**: Documentation generation in different languages
- **Custom Templates**: User-defined documentation templates
- **Advanced Analytics**: Repository complexity analysis and insights
- **Integration APIs**: REST API for programmatic access
- **Voice Commands**: Natural language control of documentation generation
- **Real-time Collaboration**: Multi-user documentation editing

### 🤖 AI/ML Enhancements

- **Model Fine-tuning**: Custom models for specific documentation styles
- **Context Learning**: Improved AI learning from past documentation
- **Prompt Optimization**: Automated prompt improvement based on output quality
- **Semantic Analysis**: Better understanding of code relationships
- **Voice Processing**: Advanced speech recognition and natural language understanding

### 🎨 User Experience

- **CLI Improvements**: Better command-line interface and progress indicators
- **Web Interface**: Browser-based documentation generation
- **Voice Interface**: Hands-free operation and audio feedback
- **Configuration UI**: Graphical configuration management
- **Output Customization**: Flexible output formatting and styling

### 📚 Documentation & Examples

- **Agent Development Guide**: Comprehensive guide for creating new agents
- **Plugin Tutorial**: Step-by-step plugin development tutorial
- **Voice Integration Guide**: Documentation for voice feature development
- **Prompt Engineering Best Practices**: Guidelines for effective prompt design
- **Video Tutorials**: Getting started and advanced usage guides

## 🔌 Plugin Development

### Creating a Plugin

1. **Inherit from BasePlugin**
   ```python
   from plugins.base_plugin import BasePlugin
   
   class MyCustomPlugin(BasePlugin):
       name = "my_custom_plugin"
       version = "1.0.0"
       description = "Custom functionality for PromptSwitch"
       author = "Your Name"
       
       def execute(self, hook: str, data: Dict[str, Any]) -> Dict[str, Any]:
           # Plugin logic here
           return data
   ```

2. **Register Plugin Hooks**
   ```python
   hooks = [
       "pre_clone",
       "post_parse", 
       "pre_generate",
       "post_format",
       "pre_review"
   ]
   ```

3. **Test Your Plugin**
   ```bash
   python -m plugins.test_plugin my_custom_plugin
   ```

### Voice Plugin Example

```python
class VoiceControlPlugin(BasePlugin):
    """Plugin for voice-controlled documentation generation."""
    
    name = "voice_control"
    version = "1.0.0"
    description = "Voice command integration for PromptSwitch"
    
    def __init__(self):
        super().__init__()
        self.voice_processor = VoiceProcessor()
    
    def execute(self, hook: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if hook == "pre_generate":
            # Listen for voice commands to modify generation parameters
            voice_input = self.voice_processor.listen_for_command()
            if voice_input:
                data.update(self.parse_voice_preferences(voice_input))
        
        return data
```

## 🆘 Need Help?

- 💬 **Discussions**: [GitHub Discussions](https://github.com/Avikalp-Karrahe/PromptSwitch/discussions)
- 🐛 **Issues**: [Report bugs](https://github.com/Avikalp-Karrahe/PromptSwitch/issues)
- 📧 **Email**: [akarrahe@ucdavis.edu](mailto:akarrahe@ucdavis.edu)
- 🎤 **Voice Features**: Tag issues with `voice-integration` for voice-related questions
- 🤖 **AI/Prompts**: Tag issues with `ai-enhancement` for AI and prompt engineering questions

## 🏆 Recognition

Contributors will be:
- Added to our contributors list
- Mentioned in release notes for their specific contributions
- Featured on our website for significant contributions
- Credited in generated documentation (for prompt/template contributions)
- Recognized in voice feature announcements (for voice integration work)

## 📋 Contribution Checklist

Before submitting your contribution:

- [ ] Code follows Python style guidelines (PEP 8)
- [ ] All functions have type hints and docstrings
- [ ] Changes are tested with multiple repository types
- [ ] Voice features are tested with various audio inputs (if applicable)
- [ ] Plugin compatibility is verified
- [ ] Documentation is updated
- [ ] Commit messages follow conventional format
- [ ] PR template is completed
- [ ] No sensitive information (API keys) in code

---

**Thank you for making PromptSwitch better! 🚀**

*Together, we're building the future of AI-powered documentation generation and voice-controlled development workflows.*