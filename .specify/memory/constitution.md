<!--
Sync Impact Report:
- Version change: [CONSTITUTION_VERSION] -> 1.0.0
- List of modified principles (old title -> new title if renamed):
  - [PRINCIPLE_1_NAME] -> I. Specification-First
  - [PRINCIPLE_2_NAME] -> II. Educational Clarity
  - [PRINCIPLE_3_NAME] -> III. Accuracy & Verifiability
  - [PRINCIPLE_4_NAME] -> IV. Style Consistency
  - [PRINCIPLE_5_NAME] -> V. Docusaurus Compatibility
- Added sections:
  - Book Structure & Outline
  - Writing & Formatting Rules
- Removed sections: None
- Templates requiring updates (✅ updated / ⚠ pending):
  - .specify/templates/plan-template.md (✅ updated)
  - .specify/templates/spec-template.md (✅ updated)
  - .specify/templates/tasks-template.md (✅ updated)
- Follow-up TODOs: Ensure Docusaurus is initialized in the repository.
-->

# AI/Spec-Driven Book Creation Constitution

## Core Principles

### I. Specification-First
All chapters and major content sections MUST be defined in a formal specification BEFORE any content is written. Changes to the book structure require an update to the specification first.

### II. Educational Clarity
Content MUST be written for beginners and students. Simple explanations, analogies, and step-by-step guides are preferred over dense technical jargon. Non-negotiable: All technical terms must be introduced before use.

### III. Accuracy & Verifiability
No false or unverifiable claims. AI-generated technical content MUST be verified against official documentation or tested in a live environment. If a claim cannot be verified, it must be omitted or framed as an observation.

### IV. Style Consistency
The book MUST maintain a consistent voice and tone across all 10 chapters. Each chapter must follow the mandated structure: Clear title, Short introduction, Main concepts in sections, Simple examples, and a Summary.

### V. Docusaurus Compatibility
All output MUST be valid Markdown compatible with Docusaurus. Files MUST be placed in the `/docs` directory and adhere to Docusaurus sidebar configurations.

## Book Structure & Outline

### Chapter Mandate
Each of the 10 chapters MUST include:
- **Title**: Clear and descriptive
- **Introduction**: 1-2 paragraphs setting the context
- **Main Concepts**: Organized into logical sections with subheadings
- **Examples**: Simple, runnable, or illustrative examples
- **Summary**: Recaps key takeaways at the end

### Chapter Outline
1. Introduction to AI-Native Development
2. What is Spec-Driven Development?
3. Understanding Specifications
4. AI Tools in Software Development
5. Using Claude for Writing Code & Docs
6. Introduction to Docusaurus
7. Building a Book with Docusaurus
8. Integrating AI Content into Docusaurus
9. Version Control with GitHub
10. Deploying to GitHub Pages

## Writing & Formatting Rules

### Markdown & Docusaurus
- Use Docusaurus-standard Markdown (MDX support where needed).
- Headings MUST follow hierarchical structure (H1 for title, H2 for sections, H3 for sub-sections).
- Code blocks MUST specify the language (e.g., ```javascript) and use proper indentation.

### Content Constraints
- Keep language simple and educational.
- Avoid advanced research papers or academic style.
- Do not introduce dependencies on paid tools unless explicitly specified in the feature plan.
- Eliminate unnecessary complexity in both explanations and examples.

## Governance

### Amendment Procedure
This constitution is the authoritative source for the book's development. Amendments require a version bump and a Sync Impact Report. Changes to core principles require a MAJOR version bump.

### Versioning Policy
- **MAJOR**: Fundamental change to book purpose or core writing principles.
- **MINOR**: New chapters, significant structural changes, or new mandatory sections.
- **PATCH**: Wording clarifications, typo fixes, or minor formatting updates.

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
