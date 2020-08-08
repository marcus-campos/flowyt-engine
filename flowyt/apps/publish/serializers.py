from utils.serializers import GenericSerializer


class PublishSerializer(GenericSerializer):
    def rules(self, rule):
        rule.add_argument("test", type=str, required=True)
