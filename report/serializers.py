from rest_framework import serializers
from .models import Custom_ai_report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_ai_report
        fields = ['id', 'user','title','section','style','instruction', 'docs_id', 'report']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        docs_ids = validated_data.pop('docs_id', []) 

        obj = Custom_ai_report.objects.create(user=user, **validated_data)
        if docs_ids:
            obj.docs_id.set(docs_ids)
        return obj