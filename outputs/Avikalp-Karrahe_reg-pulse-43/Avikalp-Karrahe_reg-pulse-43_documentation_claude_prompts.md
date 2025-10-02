# Claude Desktop Prompts for Building RegPulse - Voice-First AI Compliance Monitoring

These prompts will help you **build and implement** the **RegPulse** project from scratch using Claude Desktop, based on the analyzed documentation. RegPulse is a sophisticated voice-first AI application that flags regulatory risk on sales calls in real-time and provides exact rule citations with audit-ready evidence.

## Project Information

- **GitHub URL:** https://github.com/Avikalp-Karrahe/reg-pulse-43
- **Primary Language:** TypeScript (85.9% - 110 files)
- **Project Type:** Web Frontend Application with AI Integration
- **File Count:** 128 files
- **Live Demo:** https://preview--reg-pulse-ai.lovable.app/
- **Complexity:** Complex
- **Reference Documentation:** Avikalp-Karrahe_reg-pulse-43_documentation.md

## Project Overview

**RegPulse** is a real-time regulatory risk detection system with audit-ready evidence capabilities. It's designed for financial services compliance, specifically targeting SEC, FINRA, and FTC regulations.

### Core Features
- **Voice-First AI:** Real-time analysis of sales calls for regulatory compliance
- **Risk Detection:** Instant flagging of potential regulatory violations
- **Audit-Ready Evidence:** Automatic generation of compliance documentation
- **Rule Citations:** Exact regulatory rule references with violations
- **Real-Time Monitoring:** Live compliance tracking during calls

### Technology Stack
- **Frontend:** React 18 + TypeScript + Vite
- **Styling:** Tailwind CSS + shadcn/ui components
- **Backend:** Supabase (Database + Auth + Edge Functions)
- **AI Integration:** Voice processing and compliance analysis
- **Build Tool:** Vite with TypeScript
- **Package Manager:** npm/bun
- **Deployment:** Lovable platform

---

## Prompt 1: Project Setup & Architecture Planning

```
You are a senior full-stack developer and AI integration specialist. I need you to help me build RegPulse, a voice-first AI compliance monitoring application for financial services.

**Project Context:**
- Primary Language: TypeScript
- Project Type: React Web Application with AI Integration
- Reference Repository: https://github.com/Avikalp-Karrahe/reg-pulse-43
- Live Demo: https://preview--reg-pulse-ai.lovable.app/
- Target Complexity: Complex (128 files)
- Core Purpose: Real-time regulatory risk detection with audit-ready evidence

**Technology Stack:**
- Frontend: React 18 + TypeScript + Vite
- Styling: Tailwind CSS + shadcn/ui
- Backend: Supabase (PostgreSQL + Auth + Edge Functions)
- Build Tool: Vite
- Package Manager: npm or bun

**Your Role:**
- Expert React/TypeScript developer with 10+ years experience
- AI integration specialist for voice processing
- Financial compliance software architect
- Supabase and modern web stack expert

**Task:**
Help me set up the foundational architecture for RegPulse:

1. **Project Initialization**
   ```bash
   # Create new Vite + React + TypeScript project
   npm create vite@latest reg-pulse-43 -- --template react-ts
   cd reg-pulse-43
   npm install
   
   # Install core dependencies
   npm install @supabase/supabase-js
   npm install @radix-ui/react-* lucide-react
   npm install tailwindcss postcss autoprefixer
   npm install class-variance-authority clsx tailwind-merge
   
   # Install development dependencies
   npm install -D @types/node eslint @typescript-eslint/eslint-plugin
   ```

2. **Configure Tailwind CSS + shadcn/ui**
   ```bash
   # Initialize Tailwind
   npx tailwindcss init -p
   
   # Setup shadcn/ui
   npx shadcn-ui@latest init
   
   # Install essential components
   npx shadcn-ui@latest add button card input label textarea
   npx shadcn-ui@latest add alert dialog sheet tabs
   npx shadcn-ui@latest add badge progress separator
   ```

3. **Project Structure Setup**
   Create this exact directory structure:
   ```
   src/
   ├── components/
   │   ├── ui/           # shadcn/ui components
   │   ├── compliance/   # Compliance-specific components
   │   ├── voice/        # Voice processing components
   │   └── dashboard/    # Dashboard components
   ├── hooks/            # Custom React hooks
   ├── lib/              # Utility functions
   ├── services/         # API and external services
   ├── types/            # TypeScript type definitions
   ├── pages/            # Page components
   └── integrations/     # Third-party integrations
   
   supabase/
   ├── functions/        # Edge functions
   └── migrations/       # Database migrations
   
   public/
   └── demo/            # Demo assets
   ```

4. **Configuration Files**
   Create these essential config files:
   
   **vite.config.ts:**
   ```typescript
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'
   import path from 'path'
   
   export default defineConfig({
     plugins: [react()],
     resolve: {
       alias: {
         "@": path.resolve(__dirname, "./src"),
       },
     },
   })
   ```
   
   **tailwind.config.ts:**
   ```typescript
   import type { Config } from "tailwindcss"
   
   const config = {
     darkMode: ["class"],
     content: [
       './pages/**/*.{ts,tsx}',
       './components/**/*.{ts,tsx}',
       './app/**/*.{ts,tsx}',
       './src/**/*.{ts,tsx}',
     ],
     theme: {
       extend: {
         colors: {
           border: "hsl(var(--border))",
           input: "hsl(var(--input))",
           ring: "hsl(var(--ring))",
           background: "hsl(var(--background))",
           foreground: "hsl(var(--foreground))",
           primary: {
             DEFAULT: "hsl(var(--primary))",
             foreground: "hsl(var(--primary-foreground))",
           },
           // Add compliance-specific colors
           compliance: {
             safe: "#10b981",
             warning: "#f59e0b", 
             danger: "#ef4444",
           }
         },
       },
     },
     plugins: [require("tailwindcss-animate")],
   } satisfies Config
   
   export default config
   ```

5. **Environment Setup**
   Create `.env.local`:
   ```env
   VITE_SUPABASE_URL=your_supabase_project_url
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
   VITE_AI_API_KEY=your_ai_service_api_key
   ```

**Output Requirements:**
- Fully configured Vite + React + TypeScript project
- Tailwind CSS + shadcn/ui integration
- Supabase client setup
- Proper project structure for compliance application
- Development environment ready for AI integration

**Quality Standards:**
- Follow React 18 best practices with hooks
- Use TypeScript strictly with proper typing
- Implement responsive design with Tailwind
- Ensure accessibility compliance
- Set up proper ESLint and Prettier configuration

Please provide the complete project setup with all configuration files and explain each step clearly.
```

---

## Prompt 2: Core Implementation & Feature Development

```
You are an expert Unknown developer and system implementer. Building on the project setup from the previous step, I need you to help me implement the core functionality.

**Previous Setup Context:**
[PASTE THE OUTPUT FROM PROMPT 1 HERE]

**Project Details:**
- Repository Reference: https://github.com/Avikalp-Karrahe/reg-pulse-43
- Technology Stack: Unknown, Unknown
- Target: Build a REST API application
- Core Features: REST API, Database integration, Web interface, Command-line interface, Testing framework, User interface

**Your Enhanced Role:**
- Senior Unknown developer
- API design specialist
- Database architect (if applicable)
- Frontend/Backend integration expert
- Performance optimization specialist

**Implementation Tasks:**

1. **Core Application Logic**
   - Implement main application entry points for a REST API application
   - Create core business logic modules
   - Set up routing and navigation (if applicable)
   - Implement data models and schemas

2. **Feature Implementation**
   - Build these specific features: REST API, Database integration, Web interface, Command-line interface, Testing framework, User interface
   - Create user interfaces for the core functionality
   - Implement API endpoints and services
   - Add data persistence and management

3. **Integration & Communication**
   - Set up inter-component communication
   - Implement external API integrations
   - Configure database connections
   - Add authentication and authorization

4. **Error Handling & Validation**
   - Implement comprehensive error handling
   - Add input validation and sanitization
   - Create logging and monitoring systems
   - Set up debugging and development tools

5. **Testing Implementation**
   - Write unit tests for core functionality
   - Create integration tests
   - Set up test automation
   - Implement code coverage reporting

**Code Quality Requirements:**
- Write clean, readable, and maintainable code
- Follow established coding standards
- Include comprehensive comments and documentation
- Implement proper error handling
- Use design patterns appropriately

**Deliverables:**
- Complete, functional codebase
- Working application with core features
- Comprehensive test suite
- Clear code documentation
- Setup and run instructions

**Implementation Checklist:**
- [ ] Core functionality is working
- [ ] All features are implemented
- [ ] Tests are passing
- [ ] Code follows best practices
- [ ] Application runs without errors
- [ ] Documentation is complete

Please provide complete, working code implementations that I can use to build a REST API application with these key features: REST API, Database integration, Web interface, Command-line interface, Testing framework, User interface.
```

---

## Prompt 3: Deployment, Optimization & Production Readiness

```
You are a DevOps engineer and production systems specialist. I need you to help me deploy, optimize, and make my Unknown application production-ready.

**Complete Implementation Context:**
[PASTE ALL PREVIOUS OUTPUTS HERE]

**Project Status:**
- Repository Reference: https://github.com/Avikalp-Karrahe/reg-pulse-43
- Technology: Unknown Unknown
- Current State: Functional a REST API application with core features
- Target: Production-ready deployment
- Features Implemented: REST API, Database integration, Web interface, Command-line interface, Testing framework, User interface

**Your Expert Role:**
- DevOps and deployment specialist
- Performance optimization expert
- Security and compliance consultant
- Monitoring and maintenance specialist
- Production systems architect

**Production Readiness Tasks:**

1. **Deployment Configuration**
   - Set up production environment
   - Configure deployment scripts and automation
   - Create Docker containers (if applicable)
   - Set up cloud hosting and infrastructure

2. **Performance Optimization**
   - Optimize application performance
   - Implement caching strategies
   - Configure load balancing (if needed)
   - Optimize database queries and connections

3. **Security Implementation**
   - Implement security best practices
   - Set up SSL/TLS certificates
   - Configure environment variables and secrets
   - Add security headers and protections

4. **Monitoring & Logging**
   - Set up application monitoring
   - Configure error tracking and alerting
   - Implement performance metrics
   - Create health check endpoints

5. **Documentation & Maintenance**
   - Create deployment documentation
   - Write operational runbooks
   - Set up backup and recovery procedures
   - Plan maintenance and update strategies

**Production Standards:**
- High availability and reliability
- Scalable architecture
- Comprehensive monitoring
- Security compliance
- Automated deployment processes

**Final Deliverables:**
- Production deployment configuration
- Monitoring and alerting setup
- Security implementation
- Operational documentation
- Maintenance procedures

**Production Checklist:**
- [ ] Application deploys successfully
- [ ] All security measures are in place
- [ ] Monitoring and logging are working
- [ ] Performance is optimized
- [ ] Backup and recovery are configured
- [ ] Documentation is complete
- [ ] Application is publicly accessible
- [ ] All production requirements are met

Please provide a complete production deployment solution that makes my a REST API application ready for real-world use, following industry best practices for reliability, security, and performance.
```

---

## Implementation Guide

### How to Use These Prompts:

1. **Sequential Development**: Follow prompts in order (Setup → Implementation → Deployment)
2. **Context Preservation**: Always include previous outputs in subsequent prompts
3. **Customization**: Adapt technical details to your specific requirements
4. **Iterative Refinement**: Ask for clarifications and improvements as needed

### Expected Outcomes:

- **Functional Application**: Complete, working a REST API application built with Unknown
- **Production Ready**: Deployed application ready for real users  
- **Best Practices**: Code following industry standards and conventions
- **Comprehensive Documentation**: Setup, usage, and maintenance guides
- **Key Features**: REST API, Database integration, Web interface, Command-line interface, Testing framework, User interface

### Development Tips:

- Start with the basic setup and gradually add complexity
- Test each component thoroughly before moving to the next step
- Ask for specific code examples and implementations
- Request explanations for any unclear concepts or decisions
- Adapt the suggestions to your specific use case and requirements

### Success Criteria:

- ✅ Project builds and runs without errors
- ✅ All core features are implemented and working
- ✅ Application is deployed and accessible
- ✅ Code quality meets professional standards
- ✅ Documentation enables others to understand and contribute

---

*Generated by PromptSwitch v2 for building a REST API application - 2025-10-01 18:08:31*
