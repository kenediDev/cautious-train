import os
from rest_framework import serializers
from database.models.product import Category, Product
from ds_product.serializer.base import Base
from django.utils.translation import gettext as _


class ProductSerializer(Base):
    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)

    def get_fields(self, *args, **kwargs):
        fields = super(ProductSerializer, self).get_fields(*args, **kwargs)
        return fields

    def create(self, validated_data):
        if self.context['args'] == 'category':
            return self.c_c(validated_data)
        if self.context['args'] == "product":
            return self.p_c(validated_data)
        return validated_data

    def c_c(self, options):
        self.c_already(options)
        create = Category(name=options.get('name'), icon=options.get(
            'icon'), user=options.get('user'))
        create.save()
        return create

    def c_already(self, options):
        check = Category.objects.filter(name=options.get('name')).first()
        if check:
            raise serializers.ValidationError(
                _("Name already exists, please choose another one"))
        return check

    def p_c(self, options):
        self.p_already(options)
        category = options.get('category')
        create = Product(name=options.get('name'), photo=options.get(
            'photo'), sell=options.get('sell'), promo=options.get('promo'),
            agent=options.get('agent'), description=options.get('description'),
            author=options.get('author'), category=category)
        create.save()
        category.product_many.add(create)
        return create

    def p_already(self, options):
        check = Product.objects.filter(name=options.get('name')).first()
        if check:
            raise serializers.ValidationError(
                _("Name already exists, please choose another one"))
        return check

    def update(self, instance, validated_data):
        if self.context['args'] == 'category':
            return self.u_c(validated_data, instance)
        elif self.context['args'] == 'product':
            return self.u_p(validated_data, instance)
        return instance

    def u_p(self, options, context):
        if options.get('photo'):
            if context.photo:
                splits = str(context.photo).split("/")
                path = "media/product/%s" % splits[len(splits) - 1]
                os.system("rm %s" % path)
            context.photo = options.get('photo')
        context.name = options.get('name')
        context.photo = options.get('photo')
        context.sell = options.get('sell')
        context.promo = options.get('promo')
        context.agent = options.get('agent')
        context.description = options.get('description')
        context.save()
        return context

    def u_c(self, options, context):
        if context.icon:
            splits = str(context.icon).split("/")
            path = "media/category/%s" % splits[len(splits) - 1]
            os.system("rm %s" % path)
        context.icon = options.get('icon')
        context.save()
        return context


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
