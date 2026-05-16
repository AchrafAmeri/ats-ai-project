from fastapi import UploadFile, HTTPException, status

def validate_pdf_file(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seul le format PDF est accepté."
        )
    return True