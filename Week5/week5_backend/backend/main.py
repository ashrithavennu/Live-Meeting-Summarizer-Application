from pipeline import run_pipeline
from live_pipeline import run_live_pipeline

print("Choose Mode")
print("1. Recorded Audio")
print("2. Live Meeting")

choice = input("Enter choice: ")

if choice == "1":
    transcript, summary = run_pipeline()
    print("\nTranscript:\n", transcript)
    print("\nSummary:\n", summary)

elif choice == "2":
    transcript, summary = run_live_pipeline()
    print("\nTranscript:\n", transcript)
    print("\nSummary:\n", summary)

else:
    print("Invalid choice")