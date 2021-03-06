from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

from coldmaterhttp.models import User, Machine
from coldmaterhttp.serializers import UserSerializer, MachineSerializer #, UserSerializer2

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MachineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


def check_login(request, username, password):    
    print("Username = " + username)
    print("Password = " + password)
    query = 'SELECT * FROM coldmaterhttp_user where username = "' + username + '" and password = "' + password + '"'
    print(query)    
    try:        
        result = User.objects.raw(query)    
        return JsonResponse({"success" : "True", "userid" : result[0].userid, "machineid" : result[0].machineid})         
    except:
        return JsonResponse({"success" : "False", "userid" : None, "machineid" : None})    

#@api_view(['GET', 'POST'])
@csrf_exempt
def login_form(request):

    if request.method == 'GET':
        if request.session.has_key('coldmateruser'):
            userid = request.session['coldmateruser']
            machineid = request.session['coldmatermachineid']
            return redirect(dashboard, userid = userid, machineid = machineid)
        else:
            return render(request, "coldmaterhttp/login_form.html", {"login": "new"})

    elif request.method == 'POST':
        username = request.POST.get("username")        
        password = request.POST.get("password")        
        query = 'SELECT * FROM coldmaterhttp_user where username = "' + username + '" and password = "' + password + '"'        
        result = User.objects.raw(query)             
        try:                                
            userid = result[0].userid
            machineid = result[0].machineid
            request.session['coldmateruser'] = userid
            request.session['coldmatermachineid'] = machineid
            request.session.set_expiry(7*24*60*60)
            return redirect(dashboard, userid = userid, machineid = machineid)
            #return redirect(dashboard, userid = result[0].userid)
        except:
            return render(request, "coldmaterhttp/login_form.html", {"login": "error"})

def logout(request):

    try:
      del request.session['coldmateruser']      
    except:
      pass
    return redirect(login_form)

@csrf_exempt
def dashboard(request, userid, machineid):

    if request.method == 'GET':        
        query = 'SELECT * FROM coldmaterhttp_user where userid = "' + userid + '"'
        users = User.objects.raw(query)
        query = 'SELECT * FROM coldmaterhttp_machine where machineid = "' + machineid + '"'
        machines = Machine.objects.raw(query)    
        return render(request, "coldmaterhttp/dashboard.html", { "user": users[0], "machine": machines[0] })        

    if request.method == 'POST':
        machine_status = request.POST.get("optradio")
        set_temp = request.POST.get("set_temp")   
        #query = 'UPDATE coldmaterhttp_machine SET set_temp = "' + set_temp + '";' #+ ' WHERE machineid = "' + machineid + '"'   
        obj = Machine.objects.get(machineid=machineid)
        obj.machine_status = machine_status
        obj.set_temp = set_temp
        obj.save()        
        return redirect(dashboard, userid = userid, machineid = machineid)

def index(request):

    if request.method == 'GET':   
        return render(request, "coldmaterhttp/index.html")

def update_temps(request, machineid, ambt, watert):

    if request.method == 'GET':
        print(machineid, ambt, watert)
        obj = Machine.objects.get(machineid=machineid)
        obj.ambient_temp = ambt
        obj.water_temp = watert
        obj.save()     
        query = 'SELECT * FROM coldmaterhttp_machine where machineid = "' + machineid + '"'
        try:        
            machines = Machine.objects.raw(query)
            return JsonResponse({"success" : "True", "set_temp" : machines[0].set_temp})         
        except:
            return JsonResponse({"success" : "False", "set_temp" : None})           
        return HttpResponse("OK")

"""
def user_detail(request, id):
	try:
		user = User.objects.get(id=id)
	except User.DoesNotExist:
		raise Http404('This item does not exist')
	return render(request, 'coldmaterhttp/user_detail.html', {
		'user': user,	
	})


@csrf_exempt
def user_list(request):
    
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer2(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer2(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def user_details(request, pk):    
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404("User does not exist!")

    if request.method == 'GET':
        serializer = UserSerializer2(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer2(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'POST'])
def user_list1(request, format=None):    
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer2(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer2(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_details1(request, pk, format=None):
   
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer2(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer2(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class user_list2(APIView):
    
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer2(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer2(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class user_details2(APIView):
    
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer2(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer2(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class user_list3(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer2

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class user_details3(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset =User.objects.all()
    serializer_class = UserSerializer2

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class user_list4(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer2


class user_details4(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer2

"""