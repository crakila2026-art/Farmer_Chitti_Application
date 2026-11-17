
# Farming Chitti – Test Plan

## 1. Objective

Validate the functional, technical, multilingual,
retrieval and evidence-grounding capabilities of
the Farming Chitti application.

## 2. Test Environment

- OS: Windows 11
- IDE: Visual Studio Code
- Language: Python
- Framework: Streamlit
- Environment: .venv
- Application: Farming Chitti
- AI Architecture: RAG + Hybrid Search

## 3. Test Scenarios

| ID | Test Scenario | Expected Result |
|---|---|---|
| TC01 | Application startup | Streamlit loads successfully |
| TC02 | English question | Relevant answer generated |
| TC03 | Tamil question | Tamil response generated |
| TC04 | Hindi question | Hindi response generated |
| TC05 | Follow-up question | Context maintained |
| TC06 | Reset conversation | History cleared |
| TC07 | Relevant PDF retrieval | Correct source retrieved |
| TC08 | Unsupported question | No fabricated answer |
| TC09 | Evidence validation | Unsupported claims rejected |
| TC10 | Farmer registration | Profile saved |
| TC11 | Invalid mobile number | Validation error displayed |
| TC12 | Scheme eligibility | Preliminary assessment displayed |
| TC13 | Missing farmer details | Additional information requested |
| TC14 | Missing API key | Graceful error displayed |
| TC15 | Empty user question | No unnecessary processing |

## 4. Test Execution Results

Record the following for every test:

- Test Case ID
- Actual Result
- Status: PASS / FAIL / BLOCKED
- Defect Description
- Screenshot Evidence

## 5. Exit Criteria

- All critical test cases pass.
- No unresolved critical defects.
- Multilingual responses verified.
- RAG retrieval tested.
- Evidence validation tested.
- Farmer profile tested.
- Release checklist completed.

## 6. Sign-off

Project: Farming Chitti

Tested By: Project Developer

Status: Pending Execution
