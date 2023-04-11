from rest_framework import serializers

from .models import Constraint


class ConstraintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Constraint
        fields = ['id', 'code', 'max_limit',
                  'constraint_type']
