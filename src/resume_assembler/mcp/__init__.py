from mcp.tools import register
from robyn import BaseRobyn


def register_mcp_tools(app: BaseRobyn) -> None:
    register(app)
