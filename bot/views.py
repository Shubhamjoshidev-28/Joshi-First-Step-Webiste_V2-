import re
from difflib import SequenceMatcher

from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from bot.models import ChatReplyLog, FAQ
from chatbot.settings import DEFAULT_FROM_EMAIL
from user.models import UserInfo


SCHOOL_INFO = {
	"name": "Joshi's First Step School",
	"location": "Bharat Colony, Old Rajpura, Punjab",
	"phone": "+91 99888 20977",
	"email": "pinkijoshi2015@gmail.com",
	"fees_monthly": "INR 1000 per month",
	"fees_yearly": "INR 12000 per year",
}

SUPPORTED_KEYWORDS = {
	"admission": "Admissions are open. Please visit the admission page and fill out the form with student details.",
	"fees": f"Fees are {SCHOOL_INFO['fees_monthly']} or {SCHOOL_INFO['fees_yearly']}.",
	"activity": "We offer learning activities, student events, and classroom engagement programs.",
	"activities": "We offer learning activities, student events, and classroom engagement programs.",
	"contact": f"You can contact us at {SCHOOL_INFO['phone']} or {SCHOOL_INFO['email']}.",
	"phone": f"Our phone number is {SCHOOL_INFO['phone']}.",
	"email": f"Our email is {SCHOOL_INFO['email']}.",
	"location": f"We are located at {SCHOOL_INFO['location']}.",
	"address": f"Our location is {SCHOOL_INFO['location']}.",
	"facility": "Our facilities include child-friendly classrooms and a supportive learning environment.",
	"facilities": "Our facilities include child-friendly classrooms and a supportive learning environment.",
}


def _get_state(request):
	return request.session.get(
		"bot_state",
		{
			"stage": "ask_name",
			"name": "",
			"phone": "",
			"email": "",
			"welcome_sent": False,
		},
	)


def _save_state(request, state):
	request.session["bot_state"] = state
	request.session.modified = True


def _is_phone(text):
	cleaned = re.sub(r"\s+", "", text)
	return bool(re.fullmatch(r"\+?\d{10,13}", cleaned))


def _is_email(text):
	return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", text))


def _normalize_tokens(text):
	return set(re.findall(r"[a-z0-9]+", text.lower()))


def _faq_match(user_message):
	question = user_message.strip().lower()
	if not question:
		return None, 0.0

	user_tokens = _normalize_tokens(question)
	best_answer = None
	best_score = 0.0

	for faq in FAQ.objects.all():
		faq_question = faq.Question.strip().lower()
		if not faq_question:
			continue

		if faq_question in question:
			return faq.Answer, 1.0

		ratio = SequenceMatcher(None, question, faq_question).ratio()
		faq_tokens = _normalize_tokens(faq_question)
		token_overlap = 0.0
		if user_tokens and faq_tokens:
			token_overlap = len(user_tokens & faq_tokens) / len(user_tokens | faq_tokens)

		score = (0.7 * ratio) + (0.3 * token_overlap)
		if score > best_score:
			best_score = score
			best_answer = faq.Answer

	if best_score >= 0.62:
		return best_answer, best_score

	return None, best_score


def _best_keyword_match(user_message):
	message = user_message.strip().lower()
	if not message:
		return None, None, 0.0

	for keyword, answer in SUPPORTED_KEYWORDS.items():
		if keyword in message:
			return keyword, answer, 0.95

	best_keyword = None
	best_answer = None
	best_score = 0.0

	for keyword, answer in SUPPORTED_KEYWORDS.items():
		score = SequenceMatcher(None, message, keyword).ratio()
		if score > best_score:
			best_score = score
			best_keyword = keyword
			best_answer = answer

	if best_score >= 0.68:
		return best_keyword, best_answer, best_score

	return None, None, best_score


def _school_reply(user_message):
	faq_answer, faq_score = _faq_match(user_message)
	if faq_answer:
		if faq_score < 0.9:
			return f"Based on your question, this should help: {faq_answer}", "faq_fuzzy", faq_score
		return faq_answer, "faq", faq_score

	keyword, keyword_answer, keyword_score = _best_keyword_match(user_message)
	if keyword_answer:
		if keyword_score < 0.9:
			return f"I think this matches '{keyword}'. {keyword_answer}", "keyword_fuzzy", keyword_score
		return keyword_answer, "keyword", keyword_score

	fallback = "I can help with admissions, fees, activities, facilities, location, and contact details. For anything else, please use the contact page."
	return fallback, "fallback", 0.3


def _save_reply_log(request, user_message, reply, match_source, confidence):
	if not request.session.session_key:
		request.session.save()

	ChatReplyLog.objects.create(
		user_id=request.session.get("user_id"),
		session_key=request.session.session_key or "",
		user_message=user_message,
		bot_reply=reply,
		match_source=match_source,
		confidence=round(float(confidence), 3),
	)


def _respond(request, user_message, reply, match_source="system", confidence=1.0, status=200):
	_save_reply_log(request, user_message, reply, match_source, confidence)
	return JsonResponse({"reply": reply}, status=status)


def _send_welcome_email(name, email):
	subject = "Welcome to Joshi's First Step School"
	html_body = render_to_string("bot/welcome_email.html", {"name": name})
	text_body = strip_tags(html_body)
	message = EmailMultiAlternatives(subject, text_body, DEFAULT_FROM_EMAIL, [email])
	message.attach_alternative(html_body, "text/html")
	message.send(fail_silently=True)


@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
	user_message = (request.POST.get("message") or "").strip()

	if not user_message:
		return _respond(
			request,
			user_message,
			"Please type your question so I can help you.",
			match_source="validation",
			confidence=1.0,
			status=400,
		)

	user_id = request.session.get("user_id")
	user_name = request.session.get("user_name", "")

	if user_id:
		lower = user_message.lower()
		if any(word in lower for word in ["hi", "hello", "hey"]):
			return _respond(
				request,
				user_message,
				f"Hello {user_name}! How can I assist you today?",
				match_source="greeting",
				confidence=1.0,
			)
		reply, match_source, confidence = _school_reply(user_message)
		return _respond(request, user_message, reply, match_source=match_source, confidence=confidence)

	state = _get_state(request)
	stage = state.get("stage", "ask_name")

	if stage == "ask_name":
		state["name"] = user_message
		state["stage"] = "ask_phone"
		_save_state(request, state)
		return _respond(
			request,
			user_message,
			"Please enter your phone number.",
			match_source="onboarding",
			confidence=1.0,
		)

	if stage == "ask_phone":
		if not _is_phone(user_message):
			return _respond(
				request,
				user_message,
				"Please enter a valid phone number.",
				match_source="validation",
				confidence=1.0,
			)
		state["phone"] = user_message
		state["stage"] = "ask_email"
		_save_state(request, state)
		return _respond(
			request,
			user_message,
			"Please enter your email.",
			match_source="onboarding",
			confidence=1.0,
		)

	if stage == "ask_email":
		if not _is_email(user_message):
			return _respond(
				request,
				user_message,
				"Please enter a valid email address.",
				match_source="validation",
				confidence=1.0,
			)

		if UserInfo.objects.filter(email__iexact=user_message).exists():
			state["email"] = user_message
			state["stage"] = "completed"
			_save_state(request, state)
			return _respond(
				request,
				user_message,
				"This email is already registered. Please login to continue. No welcome email has been sent.",
				match_source="registered_email",
				confidence=1.0,
			)

		state["email"] = user_message
		state["stage"] = "completed"
		if not state.get("welcome_sent"):
			_send_welcome_email(state.get("name", "Parent"), user_message)
			state["welcome_sent"] = True
		_save_state(request, state)

		return _respond(
			request,
			user_message,
			"Thanks! We've sent you a welcome email. Please register to access full features like student profile and fee tracking.",
			match_source="welcome_email",
			confidence=1.0,
		)

	reply, match_source, confidence = _school_reply(user_message)
	return _respond(request, user_message, reply, match_source=match_source, confidence=confidence)


@require_http_methods(["GET"])
def chat_opening_prompt(request):
	if request.session.get("user_id"):
		reply = f"Hello {request.session.get('user_name', '')}! How can I assist you today?"
		return _respond(
			request,
			"__opening_prompt__",
			reply,
			match_source="opening_prompt",
			confidence=1.0,
		)
	return _respond(
		request,
		"__opening_prompt__",
		"Hi! May I know your name?",
		match_source="opening_prompt",
		confidence=1.0,
	)
