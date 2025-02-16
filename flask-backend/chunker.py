from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter # type: ignore
from langchain_core.documents import Document # type: ignore


def mdDocumentChunker(fileContent):
    result = []
    headers_to_split_on = [
        ("##", "Header 1"),
        ("###", "Header 2"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
    md_header_splits = markdown_splitter.split_text(fileContent)
    for split in md_header_splits:
        # Convert each split into a LangChain Document
        doc = split
        result.append(doc)
    
    print("MD Document loaded")
    return result

def recursiveChunker(document, chunkSize=700, chunkOverlap=100):
    text = document.page_content
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunkSize,
        chunk_overlap=chunkOverlap,
        length_function=len,
        is_separator_regex=False,
    )
    result = text_splitter.create_documents([text])
    for r in result:
        r.metadata = document.metadata
    return result