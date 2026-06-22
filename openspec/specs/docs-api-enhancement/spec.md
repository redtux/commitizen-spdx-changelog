<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# docs-api-enhancement Specification

## Purpose

Enhance the API reference with introductory context, usage examples, and
mkdocstrings documentation for all overridden methods.

## Requirements

### Requirement: API reference includes usage context

The API reference SHALL include introductory prose explaining what the
SPDXMarkdown formatter does, how it relates to commitizen's built-in Markdown
format, and when a user would use it.

#### Scenario: User reads the API reference intro

- **WHEN** a user opens the API reference page
- **THEN** they see introductory text before the mkdocstrings block
- **THEN** the text explains the class purpose and relationship to commitizen's
    Markdown format

### Requirement: API reference includes usage example

The API reference SHALL include at least one code example showing how to use the
SPDXMarkdown formatter programmatically or via configuration.

#### Scenario: Usage example is displayed

- **WHEN** a user scrolls to the usage example section
- **THEN** they see a code block with a practical example
- **THEN** the example demonstrates configuration or invocation

### Requirement: API reference documents all public API

The API reference SHALL document the SPDXMarkdown class entry point using
mkdocstrings `:::` syntax, covering all overridden methods.

#### Scenario: Public API is documented

- **WHEN** a user views the API reference
- **THEN** the mkdocstrings block renders documentation for the class
- **THEN** all overridden methods (get_metadata, get_latest_full_release) are
    included
