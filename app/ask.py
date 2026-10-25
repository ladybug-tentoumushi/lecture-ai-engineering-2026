
import argparse
import time

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    client = genai.Client(api_key=get_api_key())

    # 会話履歴を保持するチャットを作成
    chat = client.chats.create(model=MODEL)

    print(f"[model] {MODEL}")

    question = args.question

    # 何度も質問できるようにする
    while True:
        print(f"\n[質問] {question}")

        try:
            start_time = time.perf_counter()
            response = chat.send_message(question)
            elapsed_time = time.perf_counter() - start_time
            print(f"[応答時間] {elapsed_time:.2f}秒")
            print(f"\n[回答] {response.text}")

            usage = response.usage_metadata
            if usage is not None:
                print(
                    f"[トークン数] 入力: {usage.prompt_token_count}, "
                    f"出力: {usage.candidates_token_count}"
                )

        except errors.APIError as e:
            print(api_error_message(e.code, e.message))
            break

        # 次の質問を受け取る
        try:
            question = input("\n次の質問（exitで終了）: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if question.lower() == "exit":
            break

        if not question:
            question = "続けてください"


if __name__ == "__main__":
    main()
