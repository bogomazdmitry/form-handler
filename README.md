# Form for this

Simple telegram congratulation sender from chat gpt with image and text.

Flow:

1. Person accepts form
2. Form sends request to POST_URL (need to set up)
3. API send message with bot to TELEGRAM_CHAT_ID (need to deploy)

My form:

https://docs.google.com/forms/d/1ha0GUlMViFGe0gI-zgZMTPupxTcq1QoxGKQ7L7OW57g/edit

# Script from form

```
var POST_URL = "https://form-handler-co7z.onrender.com/beyoung/v1/8-march";

function onSubmit(e) {
    var form = FormApp.getActiveForm();
    var allResponses = form.getResponses();
    var latestResponse = allResponses[allResponses.length - 1];
    var response = latestResponse.getItemResponses();
    var payload = {};
    for (var i = 0; i < response.length; i++) {
        var question = response[i].getItem().getTitle();
        var answer = response[i].getResponse();
        payload[question] = answer;
    }
  
    var options = {
        "method": "post",
        "contentType": "application/json",
        "payload": JSON.stringify(payload)
    };
    UrlFetchApp.fetch(POST_URL, options);
};
```

# Deploy

https://dashboard.render.com/
