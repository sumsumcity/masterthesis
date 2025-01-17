## 4.4. Insecure output handling
> Category: runtime application security threat  

Impact: Textual model output may contain 'traditional' injection attacks such as XSS-Cross site scripting, which can create a vulnerability when processed (e.g. shown on a website, execute a command).

This is like the standard output encoding issue, but the particularity is that the output of AI may include attacks such as XSS.

