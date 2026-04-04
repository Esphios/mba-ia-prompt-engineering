"""Upload dataset to Langfuse with metadata support."""
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
PARENT_DIR = SCRIPT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from shared.clients import get_langfuse_client
from shared.datasets import upload_langfuse_dataset
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False
load_dotenv()

SCRIPT_DIR = Path(__file__).parent
DATASET_FILE = SCRIPT_DIR / "dataset2.jsonl"
DATASET_NAME = "go-ds"

langfuse = get_langfuse_client()

count = upload_langfuse_dataset(
    DATASET_FILE,
    DATASET_NAME,
    "Dataset for Go code analyzer",
    langfuse,
    metadata_override={
        "source": "5-langfuse"
    }
)

print("="*60)
print(f"Dataset '{DATASET_NAME}' updated with {count} examples")
print()
print("Access Langfuse UI at: http://localhost:3000")
print("Navigate to: Datasets > dataset_docgen")
