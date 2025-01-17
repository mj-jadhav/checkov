from __future__ import annotations

import os

from checkov.common.graph.graph_builder import CustomAttributes
from checkov.common.images.graph.image_referencer_provider import GraphImageReferencerProvider
from checkov.common.images.image_referencer import Image
from checkov.common.util.consts import START_LINE, END_LINE
from checkov.common.util.str_utils import removeprefix


class BaseKubernetesProvider(GraphImageReferencerProvider):

    def extract_images_from_resources(self) -> list[Image]:
        images = []

        supported_resources_graph = self.extract_nodes()

        for _, resource in supported_resources_graph.nodes(data=True):
            resource_type = resource[CustomAttributes.RESOURCE_TYPE]

            extract_images_func = self.supported_resource_types.get(resource_type)
            if extract_images_func:
                for name in extract_images_func(resource):
                    images.append(
                        Image(
                            file_path=resource[CustomAttributes.FILE_PATH],
                            name=name,
                            start_line=resource[START_LINE],
                            end_line=resource[END_LINE],
                            related_resource_id=f'{removeprefix(resource.get("file_path_"), os.getenv("BC_ROOT_DIR", ""))}:{resource.get("id_")}',
                        )
                    )

        return images
