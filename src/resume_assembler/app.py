from mcp.register import register_mcp
from robyn import Robyn

app = Robyn(__file__)

register_mcp(app)

if __name__ == "__main__":
    app.start()
