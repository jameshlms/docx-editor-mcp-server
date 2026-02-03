from mcp import register_mcp_tools
from robyn import Robyn

app = Robyn(__file__)

register_mcp_tools(app)

if __name__ == "__main__":
    app.start()
