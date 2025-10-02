# GitBlueprint 🚀

**The AI-Powered Repository Documentation Platform**

## 👥 Contributors

- **Amy Zhuang** - [LinkedIn](https://www.linkedin.com/in/amy-zhuang/) - Collaborator

---

## 🎯 Product Overview

**GitBlueprint** transforms GitHub repositories into comprehensive documentation and Claude Desktop prompts. Built for developers and teams who need to understand and replicate codebases efficiently.

### 💡 Why GitBlueprint?

- **Automated Documentation**: Generate comprehensive docs from any repository
- **Fast Onboarding**: Help teams understand codebases quickly  
- **AI Replication**: Create Claude prompts that recreate project structures
- **Production Ready**: Built for teams and organizations

## 🌟 Key Features

### 🎯 Core Functionality
- **Intelligent Repository Analysis**: Deep analysis of GitHub repositories using advanced AI models
- **Multi-Modal Documentation**: Generates comprehensive documentation in multiple formats
- **Claude Prompt Generation**: Creates production-ready Claude Desktop prompts for repository replication
- **Meta-Prompting Strategy**: Uses sophisticated prompt chaining for enhanced output quality

### 🖥️ Web Interface (GitBlueprint-Inspired)
- **Modern UI**: Clean, responsive interface inspired by GitBlueprint design patterns
- **Real-Time Processing**: Live status updates and progress tracking
- **Theme Toggle**: Dark/light mode support for better user experience
- **Mobile-Friendly**: Responsive design that works across all devices
- **Live Analytics**: Real-time insights into processing status and results

### 🤖 Advanced AI Integration
- **Weaviate Vector Search**: Enhanced semantic analysis and pattern recognition
- **Opik Observability**: Comprehensive LLM monitoring and performance tracking
- **Multi-Agent Architecture**: Specialized agents for different processing tasks
- **Enhanced Claude Generator**: Advanced prompt generation with executable instructions

## 🏗️ Architecture

GitBlueprint follows a modular, agent-based architecture:

```
GitBlueprint/
├── backend/                   # Python backend
│   ├── agents/               # Core AI agents
│   │   ├── repo_cloner.py    # Repository cloning and setup
│   │   ├── doc_planner.py    # Documentation structure planning
│   │   ├── section_filler.py # Content generation for sections
│   │   ├── enhanced_claude_generator.py # Claude prompt creation
│   │   ├── weaviate_analyzer.py # Vector search and analysis
│   │   ├── formatter.py      # Output formatting
│   │   ├── parser.py         # Code parsing and analysis
│   │   ├── review_agent.py   # Quality assurance
│   │   └── test_generator.py # Test case generation
│   ├── prompts/              # AI prompts and templates
│   ├── ui/                   # Legacy web interface
│   ├── main.py              # CLI entry point
│   ├── api_server.py        # REST API server
│   └── requirements.txt     # Python dependencies
├── src/                      # Modern React frontend
│   ├── components/          # UI components
│   ├── pages/              # Application pages
│   └── lib/                # Utilities and helpers
└── public/                  # Static assets
```

### 🤖 Core Agents

1. **RepoCloner**: Handles GitHub repository cloning and initial setup
2. **DocPlanner**: Creates structured documentation outlines
3. **SectionFiller**: Generates content for each documentation section
4. **EnhancedClaudeGenerator**: Creates executable Claude Desktop prompts
5. **EnhancedWeaviateAnalyzer**: Performs semantic analysis and pattern recognition
6. **Formatter**: Handles output formatting and file generation
7. **Parser**: Analyzes code structure and dependencies
8. **ReviewAgent**: Ensures quality and completeness
9. **TestGenerator**: Creates comprehensive test suites
10. **PDFConverter**: Converts documentation to PDF format

## 🚀 Quick Start

### Web Interface (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Avikalp-Karrahe/gitblueprint-agent-forge-67146.git
   cd gitblueprint-agent-forge-67146
   ```

2. **Install frontend dependencies**:
   ```bash
   npm install
   ```

3. **Install backend dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Start the development servers**:
   ```bash
   # Frontend (in root directory)
   npm run dev
   
   # Backend API (in backend directory)
   python api_server.py
   ```

5. **Open your browser** to `http://localhost:5173`

### CLI Usage

1. **Set up environment**:
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Run GitBlueprint**:
   ```bash
   python main.py --repo-url https://github.com/username/repository
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GITHUB_TOKEN=your_github_token_here

# Optional - Weaviate Integration
WEAVIATE_URL=your_weaviate_cluster_url
WEAVIATE_API_KEY=your_weaviate_api_key

# Optional - Opik Observability
OPIK_API_KEY=your_opik_api_key
OPIK_PROJECT_NAME=gitblueprint
OPIK_WORKSPACE=your_workspace_name
```

### Advanced Configuration

- **Custom Prompts**: Modify files in `backend/prompts/` directory
- **Agent Behavior**: Configure individual agents in `backend/agents/`
- **Output Formats**: Customize formatting in `backend/agents/formatter.py`
- **UI Themes**: Modify styles in `src/` directory

## 📁 Output Files

GitBlueprint generates several types of outputs:

- **📄 Documentation Files**: Comprehensive markdown documentation
- **🤖 Claude Prompts**: Ready-to-use Claude Desktop prompts
- **📊 Analysis Reports**: Detailed repository analysis
- **🧪 Test Suites**: Generated test cases and scenarios
- **📋 Project Summaries**: Executive summaries and overviews
- **🔄 Regeneration Blocks**: Modular prompt components for updates

## 🧪 Testing

Run the test suite:

```bash
cd backend
python -m pytest tests/ -v
```

## 🎬 Live Demo

Experience GitBlueprint in action:
- **Web Interface**: Modern React-based UI with real-time processing
- **CLI Tool**: Command-line interface for automated workflows
- **API Integration**: RESTful API for custom integrations

## 🛠️ Development

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.8+
- **Git**
- **Anthropic API Key**
- **GitHub Token**

### Setup

1. **Fork and clone** the repository
2. **Install dependencies** (frontend and backend)
3. **Configure environment** variables
4. **Start development** servers
5. **Make changes** and test
6. **Submit pull requests**

### Code Style

- **Frontend**: ESLint + Prettier configuration
- **Backend**: Black formatter + flake8 linting
- **Commits**: Conventional commit messages

## 🐳 Docker Deployment

### Build and Run

```bash
# Build the image
docker build -t gitblueprint .

# Run the container
docker run -p 3000:3000 -p 8000:8000 gitblueprint
```

### Docker Compose

```yaml
version: '3.8'
services:
  gitblueprint:
    build: .
    ports:
      - "3000:3000"
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
```

## ☁️ Cloud Deployment

GitBlueprint can be deployed on various cloud platforms:

- **Vercel**: Frontend deployment with serverless functions
- **Railway**: Full-stack deployment with automatic scaling
- **AWS**: EC2, ECS, or Lambda deployment options
- **Google Cloud**: App Engine or Cloud Run deployment
- **Azure**: Container Instances or App Service deployment

## 🔧 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure all required API keys are set in `.env`
2. **Rate Limiting**: Implement delays between API calls if needed
3. **Memory Issues**: Use streaming for large repositories
4. **Network Timeouts**: Configure appropriate timeout values

### Debug Mode

Enable debug logging:

```bash
export DEBUG=true
python main.py --repo-url https://github.com/username/repository --verbose
```

## 🗺️ Roadmap

### Upcoming Features

- **🔌 Plugin System**: Extensible architecture for custom agents
- **📊 Analytics Dashboard**: Advanced metrics and insights
- **🔄 Incremental Updates**: Smart diff-based documentation updates
- **🌐 Multi-Language Support**: Support for more programming languages
- **🤝 Team Collaboration**: Shared workspaces and collaborative editing
- **📱 Mobile App**: Native mobile applications for iOS and Android

### Performance Improvements

- **⚡ Caching Layer**: Redis-based caching for faster processing
- **🔄 Background Jobs**: Asynchronous processing with job queues
- **📈 Scalability**: Horizontal scaling and load balancing
- **🎯 Smart Routing**: Intelligent request routing and optimization

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- Inspired by GitBlueprint's elegant design patterns
- Built with modern AI technologies and best practices
- Community-driven development and continuous improvement

---

**Made with ❤️ by the GitBlueprint Team**

🔗 **Repository**: [https://github.com/Avikalp-Karrahe/gitblueprint-agent-forge-67146](https://github.com/Avikalp-Karrahe/gitblueprint-agent-forge-67146)
