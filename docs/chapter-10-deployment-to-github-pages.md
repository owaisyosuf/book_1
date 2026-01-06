---
title: "Chapter 10: Deployment to GitHub Pages"
sidebar_label: "Chapter 10: Deployment to GitHub Pages"
slug: /chapter-10-deployment-to-github-pages
---

# Chapter 10: Deployment to GitHub Pages

## Introduction
Deploying your Docusaurus site to GitHub Pages provides a free, reliable platform for sharing your documentation or book with the world. GitHub Pages integrates seamlessly with GitHub repositories, making it an excellent choice for open-source projects and documentation sites. In this chapter, we'll explore how to set up GitHub Pages for your Docusaurus site, configure deployment settings, and establish continuous deployment workflows that automatically update your site when you make changes.

## Setting Up GitHub Pages
Setting up GitHub Pages for your Docusaurus site involves several key steps that ensure your documentation is properly published and accessible. First, you need to configure your Docusaurus project with the correct settings for GitHub Pages deployment.

In your `docusaurus.config.js` file, you need to specify the correct `organizationName`, `projectName`, and `baseUrl` settings. The `organizationName` should match your GitHub username or organization name, while `projectName` should match your repository name. If your site will be hosted at `https://your-username.github.io/your-repo-name`, then `projectName` should be `your-repo-name`.

The `baseUrl` setting is crucial for proper routing. If you're deploying to a subdirectory (which is typical for GitHub Pages), this should match the repository name. For example, if your repository is `my-docs`, the `baseUrl` should be `/my-docs/`.

You'll also need to configure the `url` setting to match your GitHub Pages URL. For user/organization pages, this would be `https://your-username.github.io`, while for project pages it would include the repository name.

GitHub Pages offers two deployment options: deploying from the main branch or from a dedicated `gh-pages` branch. For Docusaurus sites, using a dedicated `gh-pages` branch is typically recommended, as it keeps your source code and built files separate.

## Deployment Configuration
Proper deployment configuration ensures your Docusaurus site works correctly on GitHub Pages. The `deploymentBranch` setting in your Docusaurus configuration should specify which branch GitHub Pages will use to serve your site.

When deploying to GitHub Pages, you may need to configure your site's assets to use relative paths rather than absolute paths. This ensures that your site works correctly when accessed from different URL structures.

Docusaurus provides a built-in deployment command: `npm run deploy`. This command builds your site and pushes the built files to the specified deployment branch. Before running this command, ensure you have the correct settings in your configuration file.

You can also configure custom domains for your GitHub Pages site by adding a `CNAME` file to your repository. This allows you to use your own domain instead of the default GitHub Pages URL.

Consider setting up SSL/TLS for your GitHub Pages site to ensure secure connections. GitHub automatically provides SSL certificates for GitHub Pages sites, making this process straightforward.

## Continuous Deployment Workflows
Continuous deployment workflows automate the process of updating your GitHub Pages site whenever you make changes to your documentation. GitHub Actions provides an excellent platform for setting up these workflows.

You can create a workflow that automatically runs `npm run build` and `npm run deploy` whenever changes are pushed to your main branch. This ensures your published site always reflects the latest version of your documentation.

A typical GitHub Actions workflow for Docusaurus deployment might include steps for:
- Checking out your repository
- Setting up Node.js environment
- Installing dependencies
- Building your Docusaurus site
- Deploying the built site to GitHub Pages

You can also configure the workflow to run on a schedule, ensuring your site is regularly updated even if there are no code changes. This can be useful for sites that pull in external content or need regular maintenance.

Consider adding checks to your workflow to ensure builds pass before deploying. This might include linting, spell-checking, or link validation to catch issues before they affect your published site.

For more complex documentation projects, you might set up different workflows for different types of changes, such as immediate deployment for minor fixes and manual approval for major content changes.

## Simple Example
Here's a simple example of setting up deployment for a Docusaurus site to GitHub Pages:

1. Configure your `docusaurus.config.js`:
```javascript
const config = {
  // ... other config
  url: 'https://your-username.github.io',
  baseUrl: '/your-repository-name/',
  organizationName: 'your-username',
  projectName: 'your-repository-name',
  deploymentBranch: 'gh-pages',
  // ... rest of config
};
```

2. Create a GitHub Actions workflow file at `.github/workflows/deploy.yml`:
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    name: Deploy to GitHub Pages
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: npm

      - name: Install dependencies
        run: npm ci
      - name: Build website
        run: npm run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

3. Run the deployment manually for the first time:
```bash
npm run deploy
```

This setup will automatically deploy your site whenever changes are pushed to the main branch, ensuring your documentation is always up-to-date.

## Summary
In this final chapter, we've explored how to deploy your Docusaurus site to GitHub Pages, covering setup procedures, configuration options, and continuous deployment workflows. GitHub Pages provides an excellent platform for publishing documentation, offering reliability, speed, and seamless integration with GitHub repositories. By following the deployment practices outlined in this chapter, you can ensure your documentation is accessible to your audience and automatically updated as you make improvements. This completes our comprehensive guide to creating AI/Spec-Driven documentation with Docusaurus, from initial setup through deployment and maintenance.