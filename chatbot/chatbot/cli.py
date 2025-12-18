 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/chatbot/cli.py b/chatbot/cli.py
new file mode 100644
index 0000000000000000000000000000000000000000..211471f8738e9843ceac4a40c1e36a7008c6aa8e
--- /dev/null
+++ b/chatbot/cli.py
@@ -0,0 +1,32 @@
+"""Command line interface for the simple chatbot."""
+
+from __future__ import annotations
+
+import sys
+
+from .chatbot import load_chatbot
+
+
+EXIT_COMMANDS = {"exit", "quit", "bye"}
+
+
+def main():
+    chatbot = load_chatbot()
+    print("🤖  Chatbot ready! Type 'exit' to quit.\n")
+    while True:
+        try:
+            user_input = input("You: ").strip()
+        except (EOFError, KeyboardInterrupt):
+            print("\nGoodbye!")
+            sys.exit(0)
+
+        if user_input.lower() in EXIT_COMMANDS:
+            print("Bot: See you next time!")
+            break
+
+        reply = chatbot.respond(user_input)
+        print(f"Bot: {reply}")
+
+
+if __name__ == "__main__":
+    main()
 
EOF
)
