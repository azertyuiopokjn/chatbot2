diff --git a/tests/test_chatbot.py b/tests/test_chatbot.py
new file mode 100644
index 0000000000000000000000000000000000000000..ac33b07b59d89d0f9da319e6fa6ae3e4d1335761
--- /dev/null
+++ b/tests/test_chatbot.py
@@ -0,0 +1,54 @@
+import http.client
+import json
+import unittest
+
+from chatbot.chatbot import load_chatbot
+from chatbot.server import create_server, serve_in_thread
+
+
+class ChatbotTests(unittest.TestCase):
+    def test_greeting_response(self):
+        bot = load_chatbot()
+        reply = bot.respond("hello")
+        self.assertNotEqual(reply.strip().lower(), "hello")
+        self.assertTrue("help" in reply.lower() or "hi" in reply.lower() or "hello" in reply.lower())
+
+    def test_name_is_remembered(self):
+        bot = load_chatbot()
+        bot.respond("my name is Alex")
+        reply = bot.respond("do you know my name?")
+        self.assertIn("Alex", reply)
+
+
+class ChatServerTests(unittest.TestCase):
+    def test_api_persists_session(self):
+        server = create_server(port=0)  # choose a free port
+        thread, server = serve_in_thread(server)
+        host, port = server.server_address
+
+        def send(body):
+            conn = http.client.HTTPConnection(host, port)
+            conn.request(
+                "POST",
+                "/chat",
+                body=json.dumps(body),
+                headers={"Content-Type": "application/json"},
+            )
+            response = json.loads(conn.getresponse().read())
+            conn.close()
+            return response
+
+        try:
+            first = send({"message": "my name is Sam"})
+            second = send({"message": "do you know my name?", "session_id": first["session_id"]})
+
+            self.assertEqual(second["session_id"], first["session_id"])
+            self.assertIn("Sam", second["reply"])
+        finally:
+            server.shutdown()
+            server.server_close()
+            thread.join(timeout=2)
+
+
+if __name__ == "__main__":
+    unittest.main()
