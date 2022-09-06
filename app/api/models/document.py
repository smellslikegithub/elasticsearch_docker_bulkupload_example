
from dataclasses import dataclass


@dataclass
class DocumentModel:
    product: str
    build: str
    branch: str
    content: str
    
    def __init__(self, product: str, build: str, branch:str, content: str) -> None:
        self.product = product
        self.build = build
        self.branch = branch
        self.content = content
    
    def __repr__(self) -> str:
        return (
            'DocumentModel('
            f'product={self.product!r}, build={self.build!r}, '
            f'branch={self.branch!r}, content={self.content!r}')

        