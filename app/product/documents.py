# from django_elasticsearch_dsl import (
#     Document,
#     fields
# )
# from django_elasticsearch_dsl.registries import registry
# from core.models import Product
#
#
# @registry.register_document
# class ProductDocument(Document):
#     """product docment for quick search"""
#
#     product = fields.ObjectField(
#         properties = {
#             "name": fields.TextField()
#         }
#     )
#
#     class Index:
#         name = "Product"
#
#     class Django:
#         model = Product
#         fields = [
#             'id', 'name', 'price', 'about_item',
#             'description', 'product_details', 'stock'
#         ]
