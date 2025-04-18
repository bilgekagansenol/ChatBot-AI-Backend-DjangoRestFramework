from rest_framework import serializers

from promptbox_api.models import PromptBoxDialogue , PromptBoxItem

class PromptBoxDialogueSerializer(serializers.ModelSerializer):
    """Serializer of Dialogue model"""
    class Meta:
        model = PromptBoxDialogue
        fields = ['prompt', 'response']


class PromptBoxItemSerializer(serializers.ModelSerializer):
    """Serializer of promptboxitem that can contain one or more dialogues"""
    dialogue = PromptBoxDialogueSerializer(many = True)
   
    class Meta:
        model = PromptBoxItem
        fields = ['id','PromptBoxItem_information','dialogue', 'is_favourite']


    def validate(self, data):
        if not data.get('dialogue'):
            raise serializers.ValidationError('at least need 1 prompt-response ')
        return data
    

    def  create(self , validated_data):
        dialogues_data = validated_data.pop('dialogue')
        item = PromptBoxItem.objects.create(
            **validated_data
        )

        for dialogue in dialogues_data:
            PromptBoxDialogue.objects.create(promptbox_item=item , **dialogue)
        return item


    def update(self , instance , validated_data):
        instance.PromptBoxItem_information = validated_data.get(
            'PromptBoxItem_information',
            instance.PromptBoxItem_information
        )
        instance.is_favourite = validated_data.get(
            'is_favourite',
            instance.is_favourite
        )
         # when updating no allow to change dialogues just information cause of  we just change info.
 
        instance.save()
        return instance