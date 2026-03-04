from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

#  A tool to read a doc
@mcp.tool(
    name="read_document",
    description="Read the contents of a document",
)
def read_document(
    doc_id: str = Field(description="The ID of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")
    return docs[doc_id]

#  A tool to edit a doc
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing the contents with new contents",
)
def edit_document(
    doc_id: str = Field(description="The ID of the document to edit"),
    old_content: str = Field(description="The old contents of the document. Must be replaced with new contents."),
    new_content: str = Field(description="The new contents of the document. Must replace the old contents."),
):
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_content, new_content)
    

# TODO: Write a resource to return all doc id's
# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
