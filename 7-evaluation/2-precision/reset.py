try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False
load_dotenv()

from langsmith import Client

DATASET_NAME = "evaluation_precision_dataset"
client = Client()

try:
    dataset = client.read_dataset(dataset_name=DATASET_NAME)
    client.delete_dataset(dataset_id=dataset.id)
    print(f"Dataset deletado: {DATASET_NAME}")
except Exception as e:
    print(f"Dataset nao encontrado ou ja deletado: {DATASET_NAME}")
