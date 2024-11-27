from import_export import resources, fields
from dash_board.models import Shipment
from import_export.widgets import ForeignKeyWidget

class dash_boardResource(resources.ModelResource):
	category= fields.Field(
		column_name='category',
		attribute='category',
		widget=ForeignKeyWidget(Category, field='name'))

class Meta:
        model = dash_board
        fields =(
        	'shipment_id',
        	'consignee',
        	'ata',        	
        	'cargo_available',
        	'date_cleared',
        	'actual_delivery',
        	'cont',
        	'twenty_ft',
        	'forty_ft',
        	'uw',
        	'weight',
        	) 