from typing import Any

from framework.resources.base_resource import BaseResource

from app.models.nutrition import NutritionInfo
from app.services.service_factory import ServiceFactory


class NutritionResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)

        # TODO -- Replace with dependency injection.
        #
        self.data_service = ServiceFactory.get_service("NutritionResourceDataService")
        self.database = "testnu"
        self.nutrition_info = "nutrition_info"
        self.key_field="name"

    def get_by_key(self, key: str) -> NutritionInfo:

        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.nutrition_info, key_field=self.key_field, key_value=key
        )

        result = NutritionInfo(**result)
        return result

    def update_by_key(self, key: str, data: dict) -> NutritionInfo:
      d_service = self.data_service
      d_service.update_data(
        self.database, self.nutrition_info, data, key_field=self.key_field, key_value=key
      )
      return self.get_by_key(key)

    def delete_by_key(self, key: str) -> None:
      d_service = self.data_service
      d_service.delete_data(
        self.database, self.nutrition_info, key_field=self.key_field, key_value=key
      )
