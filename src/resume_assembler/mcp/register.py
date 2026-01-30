from mcp.tools import docx_tools, process_tools
from robyn import BaseRobyn


def register_mcp(app: BaseRobyn) -> None:
    process_tools.register(app)
    docx_tools.register(app)
