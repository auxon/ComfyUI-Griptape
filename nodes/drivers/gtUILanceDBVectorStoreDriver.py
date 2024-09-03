from griptape.drivers.vector.pydantic_pyarrow_lancedb_ray_driver import PydanticPyArrowDaftRayLanceDBDriver
from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

DEFAULT_DB_PATH = "LANCE_DB_PATH"
DEFAULT_TABLE_NAME = "vectors"


class gtUILanceDBVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape LanceDB Vector Store Driver: https://lancedb.github.io/"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "db_path_env": ("STRING", {"default": DEFAULT_DB_PATH}),
            }
        )
        inputs["optional"].update(
            {
                "table_name": ("STRING", {"default": DEFAULT_TABLE_NAME}),
            }
        )

        return inputs

    def create(self, **kwargs):
        embedding_driver = kwargs.get("embedding_driver", None)
        db_path_env = kwargs.get("db_path_env", DEFAULT_DB_PATH)
        table_name = kwargs.get("table_name", DEFAULT_TABLE_NAME)

        # Get environment variables for LanceDB path
        db_path = self.getenv(db_path_env)

        params = {
            "lancedb_path": db_path,
            "table_name": table_name,
        }

        if embedding_driver:
            params["embedding_driver"] = embedding_driver
        else:
            params["embedding_driver"] = self.get_default_embedding_driver()

        # Initialize the LanceDB driver with the parameters
        driver = PydanticPyArrowDaftRayLanceDBDriver(**params)
        return (driver,)
