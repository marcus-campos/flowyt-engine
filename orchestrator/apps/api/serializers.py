from apps.core.serializers import GenericSerializer

class BuildSerializer(GenericSerializer):
    def rules(self, rule):
        rule.add_argument('test', type=str, required=True)
    
    
