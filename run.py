
import argparse
import os

def run_app(mode):
    if mode == "arena":
        os.system("python app_arena_v2.3.py")
    elif mode == "five":
        os.system("python app_v2.2_five_question_test.py")
    else:
        os.system("python app.py")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run persona consistency modes.")
    parser.add_argument('--mode', choices=["default", "arena", "five"], default="default", help="Select mode to run")
    args = parser.parse_args()
    run_app(args.mode)
