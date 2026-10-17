from main import app as mcp_app


async def app(scope, receive, send):
    if scope["type"] == "http":
        scope = dict(scope)
        scope["path"] = "/mcp"
        scope["raw_path"] = b"/mcp"
        scope["root_path"] = ""

    await mcp_app(scope, receive, send)
