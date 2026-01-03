# Configuration Contract: Docusaurus Book Setup

## Overview
This contract defines the required configuration structure for the Docusaurus-based book project, including site configuration and chapter metadata requirements.

## Site Configuration Schema

### docusaurus.config.js
The main configuration file must include these required fields:

```javascript
module.exports = {
  // Required fields
  title: 'string',                    // Name of the site
  tagline: 'string',                  // Brief description
  url: 'string',                      // URL of the site
  baseUrl: 'string',                  // Base URL
  onBrokenLinks: 'string',            // 'throw', 'warn', or 'ignore'
  onBrokenMarkdownLinks: 'string',    // 'warn' or 'ignore'
  favicon: 'string',                  // Path to favicon

  // Organization information
  organizationName: 'string',         // GitHub username/organization
  projectName: 'string',              // GitHub repository name

  // Deployment configuration
  deploymentBranch: 'string',         // Branch for deployment (usually 'gh-pages')

  // Themes and presets
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: 'string',      // Path to sidebar config
          editUrl: 'string',          // URL for edit links (optional)
        },
        theme: {
          customCss: 'string',        // Path to custom CSS
        },
      },
    ],
  ],

  // Theme configuration
  themeConfig: {
    navbar: {
      title: 'string',                // Navbar title
      logo: {
        alt: 'string',                // Alt text for logo
        src: 'string',                // Path to logo
      },
      items: [                        // Navigation items
        {
          type: 'string',             // 'doc', 'docsVersionDropdown', 'search', etc.
          docId: 'string',            // Document ID (for doc type)
          position: 'string',         // 'left' or 'right'
          label: 'string',            // Display label
        }
      ],
    },
    footer: {
      style: 'string',                // 'dark' or 'light'
      links: [                        // Footer links
        {
          title: 'string',
          items: [
            {
              label: 'string',
              to: 'string',           // Path or URL
            }
          ],
        }
      ],
      copyright: 'string',            // Copyright text
    },
  },
};
```

## Chapter Frontmatter Schema

### Required Fields for Each Chapter
Each chapter Markdown file in the `/docs` directory must include these frontmatter fields:

```yaml
---
title: "string"                    # Chapter title for the page
sidebar_label: "string"            # Label to show in sidebar
slug: "string"                     # Custom URL path for the page (optional)
description: "string"              # SEO description of the chapter
---
```

### Optional Fields for Each Chapter
```yaml
---
# Additional metadata that can be included
tags: ["string", ...]              # Array of tags for the chapter
authors: ["string", ...]           # Array of author names
last_update: "YYYY-MM-DD"          # Date of last update
image: "string"                    # Path to featured image (for social sharing)
keywords: ["string", ...]          # SEO keywords
---
```

## Sidebar Configuration Schema

### sidebars.js
The sidebar configuration must follow this structure:

```javascript
module.exports = {
  docs: [
    {
      type: 'category',
      label: 'string',                // Main category label (e.g., "AI/Spec-Driven Book")
      collapsed: boolean,             // Whether the category is collapsed by default
      items: [
        'string',                    // Document IDs (e.g., 'chapter-01-introduction-to-ai')
        // ... more document IDs
      ],
    },
    // ... additional categories if needed
  ],
};
```

## Content Validation Rules

### Markdown Structure Requirements
1. Each chapter must have a top-level heading (H1) that matches or relates to the frontmatter title
2. Subsequent headings must follow proper hierarchy (H2, H3, etc.)
3. Code blocks must specify language: ` ```javascript ` or ` ```markdown `
4. All relative links must point to existing files within the documentation

### Content Requirements
1. Each chapter must follow the 5-part structure: Title, Introduction, 2-4 main sections, Simple example, Summary
2. Content must be appropriate for students and beginners
3. All technical claims must be verifiable
4. Examples must be simple and clear

## Build Process Contract

### Required Build Steps
1. `npm install` - Install all dependencies
2. `npm run build` - Build the static site
3. Verify successful build with no errors
4. Test locally with `npm run serve`

### Expected Output
- Static HTML files in the `build/` directory
- All links resolve correctly
- All assets are properly referenced
- Site is accessible at configured base URL

## Deployment Contract

### GitHub Pages Deployment
1. The `build/` directory contents must be deployed to the `gh-pages` branch
2. Site must be accessible at the configured URL
3. All navigation must function correctly
4. Search functionality must work properly