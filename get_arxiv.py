import arxiv
import os
from datetime import datetime
import sys


def create_paper_note(arxiv_url):
    print(f"Processing paper from URL: {arxiv_url}")

    # Extract paper ID from URL
    paper_id = arxiv_url.split("/")[-1]

    # Search for the paper
    print("Fetching paper details from arXiv...")
    search = arxiv.Search(id_list=[paper_id])
    paper = next(search.results())
    print(f"Found paper: {paper.title}")

    # Format authors (first author et al. if multiple)
    authors = paper.authors
    if len(authors) > 1:
        author_text = f"{authors[0].name.split()[-1]} et al."
    else:
        author_text = authors[0].name.split()[-1]

    # Get year
    year = paper.published.year

    # Format title
    title = f"{author_text} - {year} - {paper.title}"

    # Create markdown content
    content = f"""---
title: "{title}"
tags:
  - paper
---

## Links
- [PDF]({paper.pdf_url})
- [arXiv]({arxiv_url})

## Abstract

{paper.summary}

## notes

"""

    # Create filename
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-"))
    filename = f"content/papers/{safe_title}.md"
    print(f"Creating note at: {filename}")

    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Write file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully created paper note")

    return filename


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_arxiv.py <arxiv_url>")
        sys.exit(1)
    create_paper_note(sys.argv[1])
