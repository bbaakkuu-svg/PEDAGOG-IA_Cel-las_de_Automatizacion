from pydantic import BaseModel\n\nclass RepoConfig(BaseModel):\n    name: str\n    owner: str
