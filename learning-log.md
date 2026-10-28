# Learning Log

## Day 1
- Validation checks shape, not correctness (the "sharma trdrs" lesson)
- The prompt, not the model size, fixed the typo problem
- Both models scored 3/3, so I need harder tests to compare them
- The first call is slow because of model loading, so ignore it when comparing speed
- Don't trust a script change until the output proves it (the model name bug)
- Added a 7th test (previous balance trap). The 4B model failed it: answered 7124 instead of 2124
- Validation accepted the wrong answer because it was a valid number. Only the answer key caught it
- Fixed it by adding one sentence to the prompt, then re-ran all tests to check nothing broke
- Loop to remember: write test, see it fail, find the cause, fix one thing, re-run everything
- Model output is text: pydantic turns it into checked data, but it only checks shape, not truth
- The model fixed "sharma trdrs" because it learned patterns from lots of text, and my prompt told it to fix typos
- The model predicts the next piece of text one step at a time; the prompt shifts which piece is most likely
- Temperature 0 gives the same answer every time; higher temperature only adds variety where several answers are reasonable
- Use temperature 0 for extraction (reproducible), higher for brainstorming
