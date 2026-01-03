# Data Model: AI/Spec-Driven Book Creation

## Overview
This document describes the data model for the 10-chapter technical book project. Since this is primarily a content-focused project with Markdown files, the "data model" refers to the structure and metadata of the content files.

## Core Entities

### Book
- **Name**: The complete collection of chapters
- **Description**: A technical book on AI-assisted, specification-driven development
- **Relationships**: Contains 10 chapters in a specific sequence
- **Attributes**:
  - Title: "AI/Spec-Driven Book Creation"
  - Author: To be determined during content creation
  - Publication date: To be set when published
  - Version: Track revisions if needed

### Chapter
- **Name**: Individual content unit within the book
- **Description**: A focused section covering a specific topic in the book
- **Relationships**: Belongs to one Book, may reference other Chapters
- **Attributes**:
  - Chapter number: Sequential identifier (1-10)
  - Title: Descriptive name of the chapter
  - Slug: URL-friendly identifier for web routing
  - Description: Brief summary of chapter content
  - Status: Draft, Review, Published
  - Created date: When chapter was created
  - Modified date: When chapter was last updated
  - Dependencies: Other chapters this chapter builds upon

### Content Section
- **Name**: Subdivision within a chapter
- **Description**: Organized part of a chapter with specific focus
- **Relationships**: Belongs to one Chapter
- **Attributes**:
  - Section number: Hierarchical identifier
  - Title: Descriptive name of the section
  - Content: The actual text content
  - Type: Introduction, Concept, Example, Summary, etc.

### Example
- **Name**: Practical demonstration within a chapter
- **Description**: Code or concept example to illustrate key points
- **Relationships**: Belongs to one Chapter
- **Attributes**:
  - Title: Brief description of the example
  - Code/Content: The actual example
  - Language: For code examples (javascript, python, etc.)
  - Difficulty: Beginner, Intermediate (all should be beginner-friendly)
  - Purpose: What concept this example demonstrates

## Validation Rules

### Chapter Validation
- Each chapter MUST have a title
- Each chapter MUST follow the 5-part structure (Title, Intro, 2-4 sections, Example, Summary)
- Each chapter MUST be in Markdown format compatible with Docusaurus
- Content MUST use simple language appropriate for students and beginners
- All technical claims MUST be verifiable against official documentation

### Content Structure Validation
- All chapters MUST be stored in the `/docs` directory
- File names MUST follow the pattern `chapter-{number}-{topic}.md`
- Each Markdown file MUST include appropriate frontmatter for Docusaurus
- Navigation MUST be properly configured in sidebar

## State Transitions

### Chapter States
- Draft → Review: When initial content is complete and ready for review
- Review → Published: When content passes quality checks
- Published → Review: When updates are needed
- Review → Draft: When major changes are required

## Relationships

### Book-Chapter Relationship
- One Book contains many Chapters (10 total)
- Chapters have a specific sequence within the Book
- Navigation follows the sequential order

### Chapter-Section Relationship
- One Chapter contains many Sections (2-4 minimum)
- Sections are organized hierarchically within the Chapter
- Sections support the main topic of the Chapter

### Chapter-Example Relationship
- One Chapter may contain many Examples
- Examples illustrate concepts described in the Chapter
- Examples should be simple and beginner-friendly