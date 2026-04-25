from django.contrib import admin

from bot.models import ChatReplyLog, FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
	list_display = ('Question', 'Answer')
	search_fields = ('Question', 'Answer')


@admin.register(ChatReplyLog)
class ChatReplyLogAdmin(admin.ModelAdmin):
	list_display = ('id', 'user_id', 'match_source', 'confidence', 'created_at')
	search_fields = ('user_message', 'bot_reply', 'session_key')
	list_filter = ('match_source', 'created_at')
	readonly_fields = ('created_at',)
