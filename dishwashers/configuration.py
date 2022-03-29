import os
from pathlib import Path

input_data_path = os.environ.get("ARTICLE_DATA_PATH", "/data/mnt/dataplatform/DimArticle.csv")
datalake_base_path = os.environ.get("DATALAKE_BASE_PATH", "data/")


class ProjectPath:
    def __init__(self, path: str):
        self.path = path
        self.has_tag = path.find("<TAG>") > -1

    def __call__(self, spark: bool = False, tag: str = "default_value") -> str:
        result = os.path.join(datalake_base_path, self.path)

        if spark:
            result = self.path.replace("/dbfs", "")

        if self.has_tag:
            if tag == "default_value":
                raise ValueError(f"Unvalid tag, for {self.path}")
            result = result.replace("<TAG>", str(tag))

        path_dir = Path(os.path.dirname(result))
        path_dir.mkdir(parents=True, exist_ok=True)

        return result


labels_path = ProjectPath(path="input/labels.csv")
predictions_path = ProjectPath(path="output/predictions/healt_predictions_<TAG>/")
cpdna_embedding_path = ProjectPath(path="models/cpdna/cpdna_embedding_<TAG>.csv")
healt_model_path = ProjectPath(path="models/healt/model/healt_model_<TAG>")
