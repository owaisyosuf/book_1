# Quickstart Guide: AI/Spec-Driven Book Creation

## Overview
This guide provides instructions for setting up and working with the AI-assisted book creation project using Docusaurus.

## Prerequisites
- Node.js (version 18 or higher)
- Git
- A GitHub account (for deployment)
- Claude access (for AI-assisted writing)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Verify Docusaurus Installation
```bash
npm run start
```
This should start a local development server at `http://localhost:3000`

## Creating Book Content

### 1. Chapter Structure
Each chapter should follow this structure in the `/docs` directory:
```
docs/
├── chapter-01-introduction-to-ai.md
├── chapter-02-spec-driven-development.md
├── ...
└── chapter-10-deployment.md
```

### 2. Chapter Template
Create new chapters using this template:

```markdown
---
title: "Your Chapter Title"
sidebar_label: "Chapter X: Your Title"
slug: /chapter-x-title
---

# Chapter Title

## Introduction
[1-2 paragraphs introducing the topic and what the reader will learn]

## Main Section 1
[Content for the first main section]

## Main Section 2
[Content for the second main section]

## Simple Example
[Include a practical example - code, concept, or demonstration]

## Summary
[Recap the key points covered in the chapter]
```

### 3. Using AI for Content Creation
1. Define your chapter outline based on the specification
2. Use Claude to generate content for each section
3. Verify technical accuracy against official documentation
4. Ensure language remains beginner-friendly
5. Review and refine the content

## Building and Previewing

### Local Development
```bash
npm run start
```
This starts a local server with hot reloading.

### Build Static Site
```bash
npm run build
```
This creates a static build in the `build/` directory.

### Serve Build Locally
```bash
npm run serve
```
This serves the built site locally for testing.

## Navigation Configuration

### Sidebar Setup
Update `sidebar.js` to include your new chapters:

```javascript
module.exports = {
  docs: [
    {
      type: 'category',
      label: 'AI/Spec-Driven Book',
      items: [
        'chapter-01-introduction-to-ai',
        'chapter-02-spec-driven-development',
        // Add more chapters here
      ],
    },
  ],
};
```

## Deployment

### GitHub Pages
1. Ensure your repository is connected to GitHub Pages
2. Build the site: `npm run build`
3. Deploy using GitHub Actions or manually push to the `gh-pages` branch

### Configuration
Update `docusaurus.config.js` with your site details:
- Site title
- Tagline
- URL
- Base URL
- GitHub repository information

## Quality Guidelines

### Writing for Beginners
- Use simple, clear language
- Define technical terms before using them
- Provide concrete examples
- Break complex concepts into digestible parts
- Include visual aids where helpful

### Technical Accuracy
- Verify all code examples
- Cross-reference official documentation
- Test examples in practice when possible
- Have a review process for technical claims

## File Structure Reference
```
my-book/
├── docs/                 # Chapter content
│   ├── chapter-01.md
│   ├── chapter-02.md
│   └── ...
├── src/                  # Custom components
│   ├── components/
│   ├── pages/
│   └── theme/
├── static/               # Static assets
├── docusaurus.config.js  # Site configuration
├── sidebars.js          # Navigation structure
├── package.json         # Dependencies
└── README.md           # Project overview
```

## Troubleshooting

### Build Issues
- Check Markdown syntax
- Verify all file paths are correct
- Ensure frontmatter is properly formatted

### Navigation Issues
- Confirm sidebar configuration matches file names
- Check that slugs don't conflict
- Verify all navigation links are valid

### Content Issues
- Review for beginner-appropriateness
- Check technical accuracy
- Ensure examples are clear and functional