from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']

    def create(self, validated_data):
        print(validated_data, '-' * 100)
        return super().create(validated_data)


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        StockProduct.objects.bulk_create([StockProduct(stock=stock,
                                                       product=position.get('product'),
                                                       quantity=position.get('quantity'),
                                                       price=position.get('price')) for position in positions])

        return stock

    def update(self, instance, validated_data):
        positions = (sorted(validated_data.pop('positions'), key=lambda p: p.get('product').pk))

        stock = super().update(instance, validated_data)
        stock_product = StockProduct.objects.filter(stock=stock)

        for position, new_values in zip(stock_product, positions):
            if position.product == new_values.get('product'):
                if new_values.get('quantity'):
                    position.quantity = new_values.get('quantity')
                if new_values.get('price'):
                    position.price = new_values.get('price')

        StockProduct.objects.bulk_update(stock_product, ['quantity', 'price'])

        return stock
