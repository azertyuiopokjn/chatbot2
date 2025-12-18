diff --git a/chatbot/__init__.py b/chatbot/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..36dd4b3e2140fd56c4ff55006ad7ca57bc3291be
--- /dev/null
+++ b/chatbot/__init__.py
@@ -0,0 +1,5 @@
+"""Simple rule-based chatbot package."""
+
+from .chatbot import ChatSession, load_chatbot
+
+__all__ = ["ChatSession", "load_chatbot"]
