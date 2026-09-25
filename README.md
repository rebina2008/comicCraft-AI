# ComicCraft - AI Comic Story Creator

ComicCraft is a FastAPI-based web application that creates
personalized five-panel comic stories.

## Features

- Story prompt input
- Main character selection
- Setting selection
- Story tone selection
- Art style selection
- Gemini Flash outline generation
- Gemini Pro narration and dialogue generation
- Hugging Face Stable Diffusion image generation
- Comic preview
- PDF export
- JSON API endpoint

## Project Architecture

User Input
    |
    v
FastAPI Backend
    |
    v
Gemini Flash
    |
    v
Five-Panel Outline
    |
    v
Gemini Pro
    |
    v
Narration and Dialogue
    |
    v
Stable Diffusion
    |
    v
Comic Images
    |
    v
Layout Builder
    |
    v
PDF Export
    |
    v
Comic Preview and Download

## Installation

Create a virtual environment:

```bash
python -m venv env