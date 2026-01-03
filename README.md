# AI/Spec-Driven Book Creation

This project creates a technical book using AI-assisted, specification-driven development. The book is built with Docusaurus and deployed to GitHub Pages.

## Overview

This repository contains a 10-chapter technical book on AI-assisted, specification-driven development. The book is written with AI assistance and published as a static website using Docusaurus.

## Features

- 10 comprehensive chapters covering AI and spec-driven development
- Beginner-friendly content designed for students
- Docusaurus-based static site generation
- GitHub Pages deployment ready

## Prerequisites

- Node.js (version 18 or higher)
- Git
- A GitHub account (for deployment)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run start
   ```

This will start a local development server at `http://localhost:3000`.

## Project Structure

```
docs/                    # Chapter content
├── chapter-01.md        # Chapter 1 content
├── chapter-02.md        # Chapter 2 content
└── ...
src/                   # Custom components
├── components/        # Custom Docusaurus components
├── pages/             # Custom pages if needed
└── theme/             # Custom theme overrides
static/                # Static assets (images, etc.)
docusaurus.config.js   # Docusaurus configuration
package.json          # Project dependencies
sidebar.js            # Navigation configuration
```

## Contributing

For contributions to the book content, please follow the 5-part chapter structure:
- Title
- Introduction (1-2 paragraphs)
- 2-4 main sections with content
- Simple example (code or concept)
- Summary (recap of key points)

## License

This project is licensed under the MIT License.