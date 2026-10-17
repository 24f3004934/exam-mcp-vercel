# Exam MCP Server

A single-tool Streamable HTTP MCP server for the exam grader.

## PyCharm local setup

1. Open this extracted folder as a project in PyCharm.
2. In PyCharm Terminal, run `python -m pip install -r requirements.txt`.
3. Run `python main.py`.
4. MCP endpoint: `http://127.0.0.1:9000/mcp`.

## GitHub and Vercel

Push the project to a GitHub repository, then import it in Vercel.
The deployed MCP endpoint should be `https://YOUR-DOMAIN.vercel.app/mcp`.

## Grading behavior

The sole MCP tool is `solve_challenge`, with no required arguments. Each invocation reads the `X-Exam-Challenge` HTTP header and returns the first 16 lowercase hex characters of SHA-256 of `<challenge>:24f3004934@ds.study.iitm.ac.in`.

Test the deployed endpoint with an MCP client before submitting.
