import random
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from foodies.models import *
from foodies.forms import *
from foodies.serializers import *

def start(request): #render page
    return render(request, 'start.html')

def home(request):
    return render(request, 'home.html')

def stall(request, id):
    context = { 'stall_id': id }
    return render(request, 'stall.html', context)

def new_stall(request):
    return render(request, 'new_stall.html')

def new_menu(request, id):
    context = { 'stall_id': id }
    return render(request, 'new_menu.html', context)

def admin_home(request):
    return render(request, 'admin_home.html')

def admin_stall(request, id):
    context = { 'stall_id': id }
    return render(request, 'admin_stall.html', context)

def order_stall(request, id):
    context = { 'stall_id': id }
    return render(request, 'order_stall.html', context)

@api_view(['GET','POST']) 
def stall_api(request):
    def get():
        # Get all stalls
        stalls = Stall.objects.all()
        stalls_serialized = StallSerializer(instance=stalls, many=True)
        return Response(stalls_serialized.data, status=status.HTTP_200_OK)

    def post():
        # Create new stall
        form = StallForm(request.POST)
        if (form.is_valid()):
            new_stall = Stall.objects.create(
                name = form.cleaned_data.get('name'),
                category = form.cleaned_data.get('category'),
                photo = form.cleaned_data.get('photo'),
            )
            new_stall_serialized = StallSerializer(instance=new_stall)
            return Response(new_stall_serialized.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if (request.method == 'GET'): return get()
    elif (request.method == 'POST'): return post()

@api_view(['GET','PUT','DELETE'])
def stall_id_api(request, id):
    def get():
        # Get details of stall :id
        stall = Stall.objects.get(id=id)
        stall_serialized = StallSerializer(instance=stall)
        return Response(stall_serialized.data, status=status.HTTP_200_OK)

    def put():
        # Edit stall :id
        pass

    def delete():
        # Delete stall :id
        stall = Stall.objects.get(id=id)
        stall.delete()
        return Response(status=status.HTTP_200_OK)

    if (request.method == 'GET'): return get()
    elif (request.method == 'PUT'): return put()
    elif (request.method == 'DELETE'): return delete()

@api_view(['GET','POST'])
def menu_id_api(request, id):
    def get():
        # Get details of menu :id
        menu = Menu.objects.get(id=id)
        menu_serialized = MenuSerializer(instance=menu)
        return Response(menu_serialized.data, status=status.HTTP_200_OK)

    def post():
        # Create new menu to stall :id
        stall = Stall.objects.get(id=id)
        if (stall != None):
            form = MenuForm(request.POST)
            if (form.is_valid()):
                new_menu = Menu.objects.create(
                    stall = stall,
                    name = form.cleaned_data.get('name'),
                    price = form.cleaned_data.get('price'),
                    hot = form.cleaned_data.get('hot'),
                    category = form.cleaned_data.get('category'),
                    peanut = form.cleaned_data.get('peanut'),
                    shrimp = form.cleaned_data.get('shrimp'),
                    lactose = form.cleaned_data.get('lactose'),
                    halal = form.cleaned_data.get('halal'),
                    vegetarian = form.cleaned_data.get('vegetarian'),
                    photo = form.cleaned_data.get('photo'),
                )
                new_menu_serialized = MenuSerializer(instance=new_menu)
                return Response(new_menu_serialized.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete():
        # Delete menu :id
        menu = Menu.objects.get(id=id)
        menu.delete()
        return Response(status=status.HTTP_200_OK)

    if (request.method == 'GET'): return get()
    elif (request.method == 'POST'): return post()
    elif (request.method == 'DELETE'): return delete()

@api_view(['POST'])
def order_api(request):
    def post():
        # Create new order 
        form = OrderForm(request.POST)
        if (form.is_valid()):
            form.save()
            new_order = form.instance
            new_order_serialized = OrderSerializer(instance=new_order)
            return Response(new_order_serialized.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if (request.method == 'POST'): return post()

@api_view(['GET'])
def order_id_api(request, id):
    def get():
        # Get order cart :id
        order = Order.objects.get(id=id)
        order_serialized = OrderSerializer(instance=order)
        return Response(order_serialized.data, status=status.HTTP_200_OK)

    if (request.method == 'GET'): return get()

@api_view(['GET'])
def order_stall_api(request, order_id, stall_id):
    def get():
        # Create new order stall
        stall = Stall.objects.get(id=stall_id)
        order = Order.objects.get(id=order_id)
        if (stall != None and order != None):
            prev_order_stall = OrderStall.objects.filter(stall=stall, order=order)
            if (len(prev_order_stall) == 0):
                new_order_stall = OrderStall.objects.create(
                    stall = stall, 
                    order = order
                )
                new_order_stall_serialized = OrderStallSerializer(instance=new_order_stall)
                return Response(new_order_stall_serialized.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if (request.method == 'GET'): return get()

@api_view(['GET','PUT'])
def order_stall_id_api(request, id):
    def get():
        # Get all orders for stall :id
        stall = Stall.objects.get(id=id)
        orders = OrderStall.objects.filter(stall=stall)
        orders_serialized = OrderStallSerializer(instance=orders, many=True)
        return Response(orders_serialized.data, status=status.HTTP_200_OK)

    def put():
        # Change order stall :id status
        order = OrderStall.objects.get(id=id)
        if (order.status != 'Done'):
            if (order.status == 'In Progress'): order.status = 'Ready for Pickup'
            elif (order.status == 'Ready for Pickup'): order.status = 'Done'
            order.save()
            order_serialized = OrderStallSerializer(instance=order)
            return Response(order_serialized.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

    if (request.method == 'GET'): return get()
    elif (request.method == 'PUT'): return put()

@api_view(['POST'])
def order_menu_api(request, order_stall_id, menu_id):
    def post():
        # Add menu :menu_id to order stall :order_stall_id
        form = OrderMenuForm(request.POST)
        if (form.is_valid()):
            order_stall = OrderStall.objects.get(id=order_stall_id)
            menu = Menu.objects.get(id=menu_id)
            if (order_stall != None and menu != None):
                prev_order_menu = OrderMenu.objects.filter(
                    order_stall = order_stall,
                    menu = menu
                )
                if (len(prev_order_menu) == 0):
                    new_order_menu = OrderMenu.objects.create(
                        order_stall = order_stall,
                        menu = menu,
                        quantity = form.cleaned_data.get('quantity')
                    )
                    new_order_menu_serialized = OrderMenuSerializer(instance=new_order_menu)
                    return Response(new_order_menu_serialized.data, status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if (request.method == 'POST'): return post()

@api_view(['POST'])
def order_menu_v2_api(request, order_id, menu_id):
    def post():
        # Add menu :menu_id to order stall :order_stall_id
        form = OrderMenuForm(request.POST)
        if (form.is_valid()):
            menu = Menu.objects.get(id=menu_id)
            order = Order.objects.get(id=order_id)
            if (order != None and menu != None):
                order_stall = OrderStall.objects.filter(stall=menu.stall, order=order)
                if (len(order_stall) == 0):
                    order_stall = OrderStall.objects.create(stall=menu.stall, order=order)
                else:
                    order_stall = order_stall[0]
                prev_order_menu = OrderMenu.objects.filter(
                    order_stall = order_stall,
                    menu = menu
                )
                if (len(prev_order_menu) == 0):
                    new_order_menu = OrderMenu.objects.create(
                        order_stall = order_stall,
                        menu = menu,
                        quantity = form.cleaned_data.get('quantity')
                    )
                    new_order_menu_serialized = OrderMenuSerializer(instance=new_order_menu)
                    return Response(new_order_menu_serialized.data, status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if (request.method == 'POST'): return post()

@api_view(['GET','PUT'])
def order_menu_id_api(request, id):
    def get():
        # Get order menu :id
        order_menu = OrderMenu.objects.get(id=id)
        order_menu_serialized = OrderMenuSerializer(instance=order_menu)
        return Response(order_menu_serialized.data, status=status.HTTP_200_OK)

    def put():
        # Edit order menu :id
        order_menu = OrderMenu.objects.get(id=id)
        form = OrderMenuForm(request.POST)
        if (form.is_valid() and order_menu != None):
            order_menu.quantity = form.cleaned_data.get('quantity')
            if (order_menu.quantity == 0):
                OrderMenu.objects.get(id=id).delete()
            else:
                order_menu.save()
            order_menu_serialized = OrderMenuSerializer(instance=order_menu)
            return Response(order_menu_serialized.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if (request.method == 'GET'): return get()
    elif (request.method == 'PUT'): return put()

@api_view(['GET'])
def checkout_api(request, id):
    def get():
        # Checkout (pay) order :id
        order = Order.objects.get(id=id)
        order.paid = True
        order.save()
        OrderStall.objects.filter(order_id=id, menus__isnull=True).delete()
        order_serialized = OrderSerializer(instance=order)
        return Response(order_serialized.data, status=status.HTTP_200_OK)

    if (request.method == 'GET'): return get()

@api_view(['GET'])
def random_api(request):
    def get():
        # Get random menu satisfied requirements
        min_price = float(request.GET.get('minPrice'))
        max_price = float(request.GET.get('maxPrice'))
        category = request.GET.get('category')
        hot = request.GET.get('hot') == 'true'
        vegetarian = request.GET.get('vegetarian') == 'true'
        halal = request.GET.get('halal') == 'true'
        peanut = request.GET.get('peanut') == 'true'
        shrimp = request.GET.get('shrimp') == 'true'
        lactose = request.GET.get('lactose') == 'true'

        def filter_menu(menu):
            return (
                min_price <= menu['price'] and menu['price'] <= max_price and
                (category == None or menu['category'] == category) and 
                (hot == None or menu['hot'] == hot) and 
                (vegetarian == None or menu['vegetarian'] == vegetarian) and 
                (halal == None or menu['halal'] == halal) and 
                (not peanut or menu['peanut'] == peanut) and
                (not shrimp or menu['shrimp'] == shrimp) and
                (not lactose or menu['lactose'] == lactose)
            )

        menus = Menu.objects.all()
        menus_serialized = MenuSerializer(instance=menus, many=True) 
        filtered_menus = list(filter(filter_menu, menus_serialized.data))
        
        if (len(filtered_menus) > 0):
            chosen_menu = random.choice(filtered_menus)
            return Response(chosen_menu, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if (request.method == 'GET'): return get()