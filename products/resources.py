from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Product, Category
from datetime import datetime
from developer_auth.models import Developer

class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')  # Match by category name
    )
    
    developer = fields.Field(
        column_name='developer',
        attribute='developer',
        widget=ForeignKeyWidget(Developer, 'id')  # Match by developer name
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category', 'stock_quantity', 'created_date', 'developer')
        import_id_fields = ('id',)
        export_order = fields

    def dehydrate_category(self, product):
        return product.category.name if product.category else ''  # Handle None case

    def dehydrate_developer(self, product):
        return product.developer.id if product.developer else ''  # Export developer name

    def before_import_row(self, row, **kwargs):
        # Handle 'created_date' field
        if 'created_date' in row:
            try:
                row['created_date'] = datetime.strptime(row['created_date'], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                row['created_date'] = None  # Or leave it empty

        return row
