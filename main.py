
import hashlib
import re

import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.lowlevel.server import request_ctx
from mcp.server.transport_security import TransportSecuritySettings

EMAIL = "24f3004934@ds.study.iitm.ac.in"

# Allow requests from Vercel and local development
security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=[
        "exam-mcp-vercel.vercel.app",
        "exam-mcp-vercel.vercel.app:*",
        "localhost:*",
        "127.0.0.1:*",
    ],
    allowed_origins=[
        "https://exam-mcp-vercel.vercel.app",
        "http://localhost:9000",
        "http://127.0.0.1:9000",
    ],
)

# Create MCP server
mcp = FastMCP(
    "Exam Challenge Server",
    stateless_http=True,
    json_response=True,
    streamable_http_path="/mcp",
    host="0.0.0.0",
    transport_security=security,
)


# Expose exactly one MCP tool
@mcp.tool()
def solve_challenge() -> str:
    """Return the exam response from the HTTP challenge header."""

    request = request_ctx.get().request

    challenge = request.headers.get(
        "x-exam-challenge", ""
    )

    if not re.fullmatch(r"[0-9a-f]{32}", challenge):
        raise ValueError(
            "Invalid or missing X-Exam-Challenge"
        )

    payload = f"{challenge}:{EMAIL}"

    return hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()[:16]


# ASGI application for Vercel
app = mcp.streamable_http_app()


# Local development on port 9000
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9000
    )
