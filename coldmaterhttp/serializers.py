from coldmaterhttp.models import User, Machine
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'userid', 'fname', 'lname', 'org', 'orgtype', 'username', 'password')

class MachineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Machine
        fields = ('id', 'machineid', 'machine_status', 'ambient_temp', 'water_temp', 'set_temp', 'temp_set_by')

"""
class UserSerializer2(serializers.Serializer):
	id 		  = serializers.IntegerField(read_only=True)
	userid    = serializers.CharField()
	fname     = serializers.CharField()
	lname     = serializers.CharField()
	org       = serializers.CharField()
	orgtype   = serializers.CharField()
	username  = serializers.CharField()
	password  = serializers.CharField()
	machineid = serializers.CharField()
	lastLogin = serializers.DateTimeField(required=False)

	def create(self, validated_data):
		return User.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.userid = validated_data.get('userid', instance.userid)
		instance.fname = validated_data.get('fname', instance.fname)
		instance.lname = validated_data.get('lname', instance.lname)
		instance.org = validated_data.get('org', instance.org)
		instance.username = validated_data.get('username', instance.username)
		instance.password = validated_data.get('password', instance.password)
		instance.machineid = validated_data.get('machineid', instance.machineid)
		instance.lastLogin = validated_data.get('lastLogin', instance.lastLogin)
		instance.save()
		return instance


"""