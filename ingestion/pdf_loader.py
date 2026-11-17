
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF_FOLDER = PROJECT_ROOT / "data" / "raw_pdfs"


def load_pdf_documents(pdf_folder=PDF_FOLDER):
    """
    Load all PDF files from the specified folder.

    Returns:
        documents: List of LangChain Document objects.
    """

    pdf_folder = Path(pdf_folder)

    if not pdf_folder.exists():
        raise FileNotFoundError(
            f"PDF folder does not exist: {pdf_folder}"
        )

    pdf_files = sorted(pdf_folder.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in: {pdf_folder}\n"
            "Please add at least one PDF document."
        )

    all_documents = []

    for pdf_file in pdf_files:

        print(f"\nProcessing PDF: {pdf_file.name}")

        try:
            loader = PyPDFLoader(str(pdf_file))
            pages = loader.load()

            extracted_pages = 0

            for document in pages:

                # Extract and clean page text
                text = document.page_content.strip()

                if not text:
                    print(
                        f"Warning: Empty page found in "
                        f"{pdf_file.name}"
                    )
                    continue

                # PyPDFLoader normally provides a zero-based page.
                page_index = document.metadata.get("page", 0)

                document.metadata["source"] = pdf_file.name
                document.metadata["page"] = int(page_index) + 1
                document.metadata["file_path"] = str(pdf_file)

                all_documents.append(document)
                extracted_pages += 1

            print(
                f"Successfully extracted "
                f"{extracted_pages} pages"
            )

        except Exception as error:
            print(
                f"Error processing {pdf_file.name}: {error}"
            )

    if not all_documents:
        raise ValueError(
            "No readable text was extracted from the PDFs."
        )

    print("\nPDF ingestion completed.")
    print(f"Total pages extracted: {len(all_documents)}")

    return all_documents


if __name__ == "__main__":
    documents = load_pdf_documents()

    print("\nSample extracted content:")
    print(documents[0].page_content[:500])

    print("\nSample metadata:")
    print(documents[0].metadata)
