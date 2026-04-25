(function () {
  var widget = document.getElementById("chatbot-widget");
  if (!widget) return;

  var panel = document.getElementById("chatbot-panel");
  var toggle = document.getElementById("chatbot-toggle");
  var messages = document.getElementById("chatbot-messages");
  var form = document.getElementById("chatbot-form");
  var input = document.getElementById("chatbot-input");

  function addMessage(text, type) {
    var div = document.createElement("div");
    div.className = "chat-msg " + type;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function fetchOpening() {
    fetch("/bot/chat/opening/")
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (data.reply) {
          addMessage(data.reply, "bot");
        }
      })
      .catch(function () {
        addMessage("Unable to connect right now. Please try again.", "bot");
      });
  }

  function sendMessage(text) {
    fetch("/bot/chat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ message: text }).toString(),
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (data.reply) {
          addMessage(data.reply, "bot");
        }
      })
      .catch(function () {
        addMessage("Sorry, something went wrong. Please try again.", "bot");
      });
  }

  var openedOnce = false;
  toggle.addEventListener("click", function () {
    panel.classList.toggle("open");

    if (panel.classList.contains("open") && !openedOnce) {
      openedOnce = true;
      fetchOpening();
      input.focus();
    }
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";
    sendMessage(text);
  });
})();
