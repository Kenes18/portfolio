from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ConversationMessageForm
from .service import (
    get_item,
    get_user_conversations,
    create_conversation,
    get_conversations,
    get_conversation,
    save_conversation_message
)


@login_required
def new_conversation(request, item_pk):
    """
    Создает новый разговор о товаре
    """
    item = get_item(item_pk)
    if item.created_by == request.user:
        return redirect('dashboard:index')

    conversations = get_user_conversations(request.user, item)

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        conversation = create_conversation(form, item, request.user)

        if conversation:
            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()
    
    return render(request, 'conversation/new.html', {
        'form': form
    })

@login_required
def inbox(request):
    """
    Отображает список разговоров для текущего пользователя
    """
    conversations = get_conversations(request.user)

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
    """
    Отображает детали конкретного разговора и позволяет отправлять новые сообщения
    """
    conversation = get_conversation(request.user, pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        save_conversation_message(form, conversation, request.user)

        return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })