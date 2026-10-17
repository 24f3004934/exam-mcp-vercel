import hashlib
import re

from mcp.server.fastmcp import FastMCP
from mcp.server.lowlevel.server import request_ctx
from mcp.server.transport_security import TransportSecuritySettings

EMAIL = "24f3004934@ds.study.iitm.ac.in"

mcp = FastMCP(
    "Exam Challenge Server",
    stateless_http=True,
    json_response=True,
    streamable_http_path="/mcp",
)


security = TransportSecuritySettings(
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

app = mcp.streamable_http_app(
    transport_security=security
)


@mcp.tool()
def solve_challenge() -> str:
    """Return the exam response derived from the HTTP challenge header."""
    request = request_ctx.get().request
    challenge = request.headers.get("x-exam-challenge", "")
    if not re.fullmatch(r"[0-9a-f]{32}", challenge):
        raise ValueError("Invalid or missing X-Exam-Challenge")
    return hashlib.sha256(f"{challenge}:{EMAIL}".encode()).hexdigest()[:16]


app = mcp.streamable_http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
