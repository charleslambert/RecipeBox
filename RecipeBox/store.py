import json
from pathlib import Path


class Store:
    """Class to handle Loading, Saving, Placement of storage file"""

    def __init__(self, filepath=None):
        if not filepath:
            self.storage_fp = Path.home().joinpath(".RecipeBox",
                                                   "recipes.json")
        else:
            self.storage_fp = filepath

        self.create_storage()

    def create_storage(self):
        self.storage_fp.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_fp:
            with self.storage_fp.open("w") as f:
                recipes = []
                json.dump(recipes, f)

    def save(self, recipes):
        with self.storage_fp.open("w") as f:
            json.dump(f)

    def load(self):
        with self.storage_fp.open() as f:
            return json.load(f)
