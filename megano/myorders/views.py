from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from mycatalog.serializers import ProductSerializer
from .services import Basket, aply_count_for_product
from mycatalog.models import Product
from typing import Any, Tuple, Dict
from .models import Order
from .serializers import (
    OrderSerializer,
    OrderDetailSerializer,
    OrderAcceptedSerializer,
    PaymentSerializer,
    OrdersGetSerializer
)


class BasketView(APIView):

    """Представление корзины"""

    def post(self, request: Request) -> Response:

        """Метод для добавления товара в корзину"""

        data = request.data
        product_id = data['id']
        count = data['count']
        product = Product.objects.get(id=int(product_id))
        products_count = product.count
        basket = Basket(request)
        basket.add_item(product_id, products_count, count)
        items = basket.dell_value_equals_zero()
        ids = basket.get_ids()
        products = Product.objects.filter(id__in=ids)
        serializer = ProductSerializer(instance=products, many=True)
        result = aply_count_for_product(serializer.data, items)
        return Response(data=result, status=status.HTTP_200_OK)

    def get(self, request: Request) -> Response:

        """Метод для отображиния товара в корзине"""

        basket = Basket(request)
        items = basket.dell_value_equals_zero()
        ids = basket.get_ids()
        products = Product.objects.filter(id__in=ids)
        serializer = ProductSerializer(instance=products, many=True)
        result = aply_count_for_product(serializer.data, items)

        return Response(data=result, status=status.HTTP_200_OK)

    def delete(self, request: Request) -> Response:

        """Метод для удаления товара из корзины"""

        data = request.data
        product_id = data['id']
        count = data['count']
        basket = Basket(request)
        basket.remove_item(product_id, count)
        items = basket.dell_value_equals_zero()
        ids = basket.get_ids()
        products = Product.objects.filter(id__in=ids)
        serializer = ProductSerializer(instance=products, many=True)
        result = aply_count_for_product(serializer.data, items)
        return Response(data=result, status=status.HTTP_200_OK)


class OrdersView(APIView):

    """Представление для заказов"""

    def post(self, request: Request) -> Response:

        """Метод для создания заказа"""

        data = {"products": request.data}
        serializer = OrderSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                data={"orderId": order.id},
                status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request) -> Response:

        """Метод для отображения заказа"""

        user = request.user
        orders = Order.objects.filter(user=user)
        basket = request.session.get("basket")
        serializer = OrdersGetSerializer(instance=orders, context={"basket": basket}, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class OrdersDetailView(APIView):

    """Представление для ввода и вывода детальных данных заказов"""

    def post(self, request: Request, **kwargs: Any) -> Response:

        """Метод для ввода детальных данных заказов"""

        id = int(kwargs.get("pk"))
        user = request.user
        data = request.data
        data["user"] = user.id
        order = Order.objects.get(id=id)
        products = data.get("products")
        serializer = OrderAcceptedSerializer(
            instance=order,
            data=data,
            context={
                "products": products,
            },
            partial=True
        )
        if serializer.is_valid():
            serializer.update(order, serializer.validated_data)
            return Response(data={"orderId": id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request, **kwargs: Any) -> Response:

        """Метод для вывода детальных данных заказов"""

        id = int(kwargs.get("pk"))
        order = Order.objects.get(id=id)
        basket = request.session.get("basket")
        serializer = OrderDetailSerializer(instance=order, context={"basket": basket})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PaymentView(APIView):

    """Метод для ввода данных карты
    также меняет статус заказа на оплаченный, и удаляет корзину из сессии"""

    def post(self, request: Request, **kwargs: Any) -> Response:
        data = request.data
        data["order_rel"] = kwargs["pk"]
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            del request.session["basket"]
            order = Order.objects.get(id=kwargs["pk"])
            order.status = "payed"
            order.save()
            return Response(data={"message": "order has been successfully payed"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
