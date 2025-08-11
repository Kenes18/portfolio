from django.shortcuts import get_object_or_404
from .models import Item, Conversation


def get_item(item_pk):
    return get_object_or_404(Item, pk=item_pk)

def get_user_conversations(user, item):
    return Conversation.objects.filter(item=item).filter(members__in=[user.id])

def create_conversation(form, item, user):
    if form.is_valid():
        conversation = Conversation.objects.create(item=item)
        conversation.members.add(user)
        conversation.members.add(item.created_by)
        conversation.save()

        conversation_message = form.save(commit=False)
        conversation_message.conversation = conversation
        conversation_message.created_by = user
        conversation_message.save()
        return conversation
    return None

def get_conversations(user):
    return Conversation.objects.filter(members__in=[user.id])

def get_conversation(user, pk):
    return Conversation.objects.filter(members__in=[user.id]).get(pk=pk)

def save_conversation_message(form, conversation, user):
    if form.is_valid():
        conversation_message = form.save(commit=False)
        conversation_message.conversation = conversation
        conversation_message.created_by = user
        conversation_message.save()
        return conversation_message
    return None
