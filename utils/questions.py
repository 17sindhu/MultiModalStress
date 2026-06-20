# =============================================================================
# questions.py  (v2 – trilingual: English, Tamil, Kannada)
#
# Each question bank is a dict keyed by language code:
#   "english" | "tamil" | "kannada"
#
# Usage in interview_screen.py:
#   from utils.questions import get_questions
#   q_list = get_questions("baseline", lang="tamil")
# =============================================================================

# ══════════════════════════════════════════════════════════════════════════════
# BASELINE
# ══════════════════════════════════════════════════════════════════════════════

_BASELINE = {

"english": [
    "What did you have for breakfast or lunch today?",
    "Describe the layout of your bedroom or current workspace.",
    "What path or mode of transport do you usually take to go to your college or workplace?",
    "What is your favourite season of the year, and why?",
    "Describe a typical evening routine at home.",
],

"tamil": [
    "இன்று காலை அல்லது மதியம் என்ன சாப்பிட்டீர்கள்?",
    "உங்கள் படுக்கையறை அல்லது தற்போதைய பணியிடத்தின் அமைப்பை விவரிக்கவும்.",
    "நீங்கள் வழக்கமாக கல்லூரி அல்லது பணியிடத்திற்கு எந்த வழியில் அல்லது எந்த வாகனத்தில் செல்வீர்கள்?",
    "உங்களுக்கு மிகவும் பிடித்த பருவகாலம் எது, ஏன்?",
    "வீட்டில் ஒரு வழக்கமான மாலை நேர வழக்கத்தை விவரிக்கவும்.",
],

"kannada": [
    "ಇಂದು ಬೆಳಿಗ್ಗೆ ಅಥವಾ ಮಧ್ಯಾಹ್ನ ನೀವು ಏನು ತಿಂದಿದ್ದೀರಿ?",
    "ನಿಮ್ಮ ಮಲಗುವ ಕೋಣೆ ಅಥವಾ ಪ್ರಸ್ತುತ ಕೆಲಸದ ಸ್ಥಳದ ವಿನ್ಯಾಸವನ್ನು ವಿವರಿಸಿ.",
    "ನೀವು ಸಾಮಾನ್ಯವಾಗಿ ಕಾಲೇಜು ಅಥವಾ ಕೆಲಸದ ಸ್ಥಳಕ್ಕೆ ಯಾವ ಮಾರ್ಗ ಅಥವಾ ಸಾರಿಗೆ ಬಳಸುತ್ತೀರಿ?",
    "ನಿಮ್ಮ ನೆಚ್ಚಿನ ಋತು ಯಾವುದು ಮತ್ತು ಏಕೆ?",
    "ಮನೆಯಲ್ಲಿ ಒಂದು ವಿಶಿಷ್ಟ ಸಂಜೆಯ ದಿನಚರಿಯನ್ನು ವಿವರಿಸಿ.",
],

}

# ══════════════════════════════════════════════════════════════════════════════
# SOCIAL STRESS
# ══════════════════════════════════════════════════════════════════════════════

_SOCIAL_STRESS = {

"english": [
    "Tell me about your single greatest academic failure. Why did you fall short, and what does that say about your current capabilities?",
    "If your closest friends or classmates were asked to name your biggest personality flaw, what would they say? Be specific.",
    "Describe a situation where a teacher or professor criticised your work harshly in front of others. How did you react to that public embarrassment?",
    "Why do you think some of your peers manage to balance high grades and internships effortlessly, while you struggle with academic pressure?",
    "Tell me about a time you let your parents down regarding your career choices or exam scores. How did you justify your performance to them?",
    "If we were to interview your past group-project partners, what complaints would they have about your work ethic or contributions?",
    "Explain a scenario where you had to lead a presentation, lost your train of thought, and realised the audience noticed. What went wrong?",
    "What is the most critical feedback you have ever received about your communication or intelligence? Why did that feedback hurt you?",
    "Describe a time you felt completely unqualified or inferior compared to everyone else in a classroom or interview room.",
    "You have 30 seconds to explain why we should value your potential over a student with a significantly higher GPA and a cleaner track record. Start now.",
],

"tamil": [
    "உங்கள் மிகப்பெரிய கல்வித் தோல்வியைப் பற்றி சொல்லுங்கள். நீங்கள் ஏன் தோல்வியடைந்தீர்கள், அது உங்கள் தற்போதைய திறன்களைப் பற்றி என்ன கூறுகிறது?",
    "உங்கள் நெருங்கிய நண்பர்கள் அல்லது வகுப்பு தோழர்கள் உங்கள் மிகப்பெரிய குணக் குறையை கூறுமாறு கேட்கப்பட்டால், அவர்கள் என்ன சொல்வார்கள்? குறிப்பாக கூறுங்கள்.",
    "ஒரு ஆசிரியர் அல்லது பேராசிரியர் மற்றவர்கள் முன்னிலையில் உங்கள் பணியை கடுமையாக விமர்சித்த சூழ்நிலையை விவரிக்கவும். அந்த பொது அவமானத்திற்கு நீங்கள் எவ்வாறு எதிர்வினையாற்றினீர்கள்?",
    "சில சக மாணவர்கள் உயர் மதிப்பெண்கள் மற்றும் இன்டர்ன்ஷிப்களை எளிதாக சமநிலைப்படுத்தும்போது, நீங்கள் கல்வி அழுத்தத்தில் போராடுவது ஏன் என்று நினைக்கிறீர்கள்?",
    "உங்கள் வாழ்க்கை தேர்வுகள் அல்லது தேர்வு மதிப்பெண்கள் தொடர்பாக நீங்கள் பெற்றோரை ஏமாற்றிய நேரத்தைப் பற்றி சொல்லுங்கள். அவர்களிடம் உங்கள் செயல்திறனை எவ்வாறு நியாயப்படுத்தினீர்கள்?",
    "உங்கள் கடந்த கால குழு திட்ட கூட்டாளிகளை நாங்கள் நேர்காணல் செய்தால், உங்கள் பணி நெறிமுறை அல்லது பங்களிப்புகளைப் பற்றி என்ன புகார்கள் கூறுவார்கள்?",
    "நீங்கள் ஒரு விளக்கக்காட்சியை வழிநடத்த வேண்டியிருந்த, சிந்தனையை இழந்த, மற்றும் பார்வையாளர்கள் கவனித்தனர் என்பதை உணர்ந்த சூழ்நிலையை விளக்குங்கள். என்ன தவறு நடந்தது?",
    "உங்கள் தொடர்புத் திறன் அல்லது புத்திசாலித்தனம் பற்றி நீங்கள் பெற்ற மிக கடுமையான கருத்து என்ன? அந்த கருத்து உங்களை ஏன் பாதித்தது?",
    "ஒரு வகுப்பறையில் அல்லது நேர்காணல் அறையில் நீங்கள் முற்றிலும் தகுதியற்றவராக அல்லது மற்றவர்களை விட தாழ்ந்தவராக உணர்ந்த நேரத்தை விவரிக்கவும்.",
    "கணிசமாக அதிக GPA மற்றும் சிறந்த சாதனை கொண்ட மாணவரை விட நாங்கள் உங்கள் திறனை ஏன் மதிக்க வேண்டும் என்று 30 வினாடிகளில் விளக்குங்கள். இப்போதே தொடங்குங்கள்.",
],

"kannada": [
    "ನಿಮ್ಮ ಅತ್ಯಂತ ದೊಡ್ಡ ಶೈಕ್ಷಣಿಕ ವಿಫಲತೆಯ ಬಗ್ಗೆ ಹೇಳಿ. ನೀವು ಏಕೆ ವಿಫಲರಾದಿರಿ ಮತ್ತು ಅದು ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಸಾಮರ್ಥ್ಯಗಳ ಬಗ್ಗೆ ಏನು ಹೇಳುತ್ತದೆ?",
    "ನಿಮ್ಮ ಆತ್ಮೀಯ ಗೆಳೆಯರು ಅಥವಾ ಸಹಪಾಠಿಗಳನ್ನು ನಿಮ್ಮ ಅತಿ ದೊಡ್ಡ ವ್ಯಕ್ತಿತ್ವ ದೋಷ ಹೇಳಲು ಕೇಳಿದರೆ, ಅವರು ಏನು ಹೇಳುತ್ತಾರೆ? ನಿರ್ದಿಷ್ಟವಾಗಿ ಹೇಳಿ.",
    "ಶಿಕ್ಷಕರು ಅಥವಾ ಪ್ರಾಧ್ಯಾಪಕರು ಇತರರ ಮುಂದೆ ನಿಮ್ಮ ಕೆಲಸವನ್ನು ಕಟುವಾಗಿ ಟೀಕಿಸಿದ ಸಂದರ್ಭವನ್ನು ವಿವರಿಸಿ. ಆ ಸಾರ್ವಜನಿಕ ಅವಮಾನಕ್ಕೆ ನೀವು ಹೇಗೆ ಪ್ರತಿಕ್ರಿಯಿಸಿದಿರಿ?",
    "ಕೆಲವು ಸಹಪಾಠಿಗಳು ಉತ್ತಮ ಅಂಕಗಳು ಮತ್ತು ಇಂಟರ್ನ್‌ಶಿಪ್‌ಗಳನ್ನು ಸಲೀಸಾಗಿ ಸಮತೋಲಿಸುವಾಗ, ನೀವು ಶೈಕ್ಷಣಿಕ ಒತ್ತಡದಲ್ಲಿ ಏಕೆ ಹೆಣಗಾಡುತ್ತೀರಿ ಎಂದು ನೀವು ಏಕೆ ಭಾವಿಸುತ್ತೀರಿ?",
    "ನಿಮ್ಮ ವೃತ್ತಿ ಆಯ್ಕೆಗಳು ಅಥವಾ ಪರೀಕ್ಷೆಯ ಅಂಕಗಳ ಬಗ್ಗೆ ನೀವು ಪೋಷಕರನ್ನು ನಿರಾಶೆಗೊಳಿಸಿದ ಸಮಯದ ಬಗ್ಗೆ ಹೇಳಿ. ನಿಮ್ಮ ಸಾಧನೆಯನ್ನು ಅವರಿಗೆ ಹೇಗೆ ಸಮರ್ಥಿಸಿಕೊಂಡಿರಿ?",
    "ನಿಮ್ಮ ಹಿಂದಿನ ಗುಂಪು ಯೋಜನೆಯ ಪಾಲುದಾರರನ್ನು ನಾವು ಸಂದರ್ಶಿಸಿದರೆ, ನಿಮ್ಮ ಕೆಲಸದ ನೀತಿ ಅಥವಾ ಕೊಡುಗೆಗಳ ಬಗ್ಗೆ ಏನು ದೂರುತ್ತಾರೆ?",
    "ನೀವು ಪ್ರಸ್ತುತಿಯನ್ನು ಮುನ್ನಡೆಸಬೇಕಾಗಿ ಬಂದ, ಆಲೋಚನೆ ಕಳೆದುಕೊಂಡ ಮತ್ತು ಪ್ರೇಕ್ಷಕರು ಗಮನಿಸಿದ್ದಾರೆ ಎಂದು ಅರಿತ ಸನ್ನಿವೇಶವನ್ನು ವಿವರಿಸಿ. ಏನು ತಪ್ಪಾಯಿತು?",
    "ನಿಮ್ಮ ಸಂವಹನ ಅಥವಾ ಬುದ್ಧಿಮತ್ತೆಯ ಬಗ್ಗೆ ನೀವು ಎಂದಾದರೂ ಪಡೆದ ಅತ್ಯಂತ ಕಟು ಪ್ರತಿಕ್ರಿಯೆ ಯಾವುದು? ಆ ಪ್ರತಿಕ್ರಿಯೆ ನಿಮ್ಮನ್ನು ಏಕೆ ನೋಯಿಸಿತು?",
    "ತರಗತಿ ಅಥವಾ ಸಂದರ್ಶನ ಕೊಠಡಿಯಲ್ಲಿ ಇತರರಿಗೆ ಹೋಲಿಸಿದರೆ ನೀವು ಸಂಪೂರ್ಣ ಅನರ್ಹ ಅಥವಾ ಕೀಳಾಗಿ ಭಾಸವಾದ ಸಮಯವನ್ನು ವಿವರಿಸಿ.",
    "ಗಣನೀಯವಾಗಿ ಹೆಚ್ಚಿನ GPA ಮತ್ತು ಉತ್ತಮ ಸಾಧನೆ ಹೊಂದಿರುವ ವಿದ್ಯಾರ್ಥಿಗಿಂತ ನಾವು ನಿಮ್ಮ ಸಾಮರ್ಥ್ಯವನ್ನು ಏಕೆ ಮೌಲ್ಯಮಾಪನ ಮಾಡಬೇಕು ಎಂಬುದನ್ನು 30 ಸೆಕೆಂಡ್‌ಗಳಲ್ಲಿ ವಿವರಿಸಿ. ಈಗಲೇ ಪ್ರಾರಂಭಿಸಿ.",
],

}

# ══════════════════════════════════════════════════════════════════════════════
# COGNITIVE LOAD
# ══════════════════════════════════════════════════════════════════════════════

_COGNITIVE = {

"english": [
    "Please count backward aloud from 1,022 in steps of 13 as quickly as you can. Do not pause.",
    "Spell the word 'MULTIMODAL' completely backward, then immediately state the total number of vowels contained in that word.",
    "If a train leaves Chennai at 60 km/h and another leaves Bangalore 2 hours later at 80 km/h on the same track, how many hours until they cross? You have 15 seconds to answer.",
    "Mentally multiply 14 by 17, subtract 11 from the result, and state only the final number aloud.",
    "Recite the months of the year in reverse chronological order, but skip every second month. Start with December.",
    "Take the number 800. Continuously subtract 17 from it out loud until I tell you to stop. Go.",
    "Listen to this sequence of digits: 7, 3, 9, 1, 5, 8. Now, recite them back to me in exact ascending numerical order.",
    "Spell the name of your native city or hometown completely backward while continuously tapping your desk with your index finger at a steady rhythm.",
    "If an assessment has 45 total questions, and you answer two-fifths of them incorrectly, exactly how many questions did you answer correctly?",
    "Repeat the alphabet backward starting from the letter Z, but alternate by saying a number after each letter starting with 1. For example: Z-1, Y-2. Go as fast as possible.",
],

"tamil": [
    "1,022 இலிருந்து 13 படிகளில் பின்னோக்கி எண்ணுங்கள். நிறுத்தாமல் விரைவாக செய்யுங்கள்.",
    "'MULTIMODAL' என்ற வார்த்தையை முழுவதும் தலைகீழாக உச்சரித்து, பின்னர் அந்த வார்த்தையில் உள்ள மொத்த உயிர் எழுத்துகளின் எண்ணிக்கையை உடனே கூறுங்கள்.",
    "ஒரு ரயில் சென்னையிலிருந்து 60 கி.மீ./மணி வேகத்திலும், இன்னொரு ரயில் 2 மணி நேரம் பின்னர் பெங்களூரிலிருந்து 80 கி.மீ./மணி வேகத்திலும் ஒரே தண்டவாளத்தில் புறப்பட்டால், எத்தனை மணி நேரத்தில் சந்திப்பார்கள்? 15 வினாடிகளில் பதில் சொல்லுங்கள்.",
    "மனதில் 14-ஐ 17-ஆல் பெருக்கி, முடிவிலிருந்து 11-ஐ கழித்து, இறுதி எண்ணை மட்டும் சத்தமாக கூறுங்கள்.",
    "ஆண்டின் மாதங்களை தலைகீழ் வரிசையில் ஒவ்வொரு இரண்டாவது மாதத்தை தவிர்த்து சொல்லுங்கள். டிசம்பரில் தொடங்குங்கள்.",
    "800 என்ற எண்ணிலிருந்து தொடர்ந்து 17-ஐ கழித்துக் கொண்டே போங்கள். நான் நிறுத்தச் சொல்லும் வரை தொடருங்கள்.",
    "இந்த தொடர் இலக்கங்களை கவனியுங்கள்: 7, 3, 9, 1, 5, 8. இப்போது அவற்றை ஏறுவரிசையில் சொல்லுங்கள்.",
    "உங்கள் சொந்த ஊர் அல்லது நகரத்தின் பெயரை முழுவதும் தலைகீழாக உச்சரியுங்கள், அதே நேரத்தில் உங்கள் ஆட்காட்டி விரலால் மேஜையை தொடர்ந்து தட்டுங்கள்.",
    "ஒரு தேர்வில் 45 கேள்விகள் இருக்கின்றன. நீங்கள் ஐந்தில் இரண்டு பங்கு கேள்விகளுக்கு தவறான பதில் அளித்தால், சரியாக எத்தனை கேள்விகளுக்கு பதில் சொன்னீர்கள்?",
    "Z என்ற எழுத்திலிருந்து தலைகீழாக அகரவரிசையை திரும்புங்கள், ஆனால் ஒவ்வொரு எழுத்திற்கு பிறகும் 1 இலிருந்து தொடங்கும் ஒரு எண்ணைச் சொல்லுங்கள். உதாரணம்: Z-1, Y-2. விரைவாக செய்யுங்கள்.",
],

"kannada": [
    "1,022 ರಿಂದ 13 ಹೆಜ್ಜೆಗಳಲ್ಲಿ ಹಿಮ್ಮುಖವಾಗಿ ಎಣಿಸಿ. ನಿಲ್ಲಿಸದೆ ವೇಗವಾಗಿ ಮಾಡಿ.",
    "'MULTIMODAL' ಪದವನ್ನು ಸಂಪೂರ್ಣ ಹಿಮ್ಮುಖವಾಗಿ ಉಚ್ಚರಿಸಿ, ನಂತರ ಆ ಪದದಲ್ಲಿರುವ ಒಟ್ಟು ಸ್ವರಗಳ ಸಂಖ್ಯೆಯನ್ನು ತಕ್ಷಣ ಹೇಳಿ.",
    "ಒಂದು ರೈಲು ಚೆನ್ನೈನಿಂದ 60 ಕಿ.ಮೀ./ಗಂ ವೇಗದಲ್ಲಿ ಮತ್ತು ಮತ್ತೊಂದು 2 ಗಂಟೆ ನಂತರ ಬೆಂಗಳೂರಿನಿಂದ 80 ಕಿ.ಮೀ./ಗಂ ವೇಗದಲ್ಲಿ ಅದೇ ಹಳಿಯಲ್ಲಿ ಹೊರಟರೆ, ಎಷ್ಟು ಗಂಟೆಗಳಲ್ಲಿ ಭೇಟಿಯಾಗುತ್ತಾರೆ? 15 ಸೆಕೆಂಡ್‌ಗಳಲ್ಲಿ ಉತ್ತರಿಸಿ.",
    "ಮನಸ್ಸಿನಲ್ಲಿ 14 ಅನ್ನು 17 ರಿಂದ ಗುಣಿಸಿ, ಫಲಿತಾಂಶದಿಂದ 11 ಕಳೆದು, ಅಂತಿಮ ಸಂಖ್ಯೆಯನ್ನು ಮಾತ್ರ ಜೋರಾಗಿ ಹೇಳಿ.",
    "ವರ್ಷದ ತಿಂಗಳುಗಳನ್ನು ಹಿಮ್ಮುಖ ಕ್ರಮದಲ್ಲಿ, ಪ್ರತಿ ಎರಡನೇ ತಿಂಗಳನ್ನು ಬಿಟ್ಟು ಹೇಳಿ. ಡಿಸೆಂಬರ್‌ನಿಂದ ಪ್ರಾರಂಭಿಸಿ.",
    "800 ಸಂಖ್ಯೆಯಿಂದ ನಿರಂತರವಾಗಿ 17 ಕಳೆಯುತ್ತಾ ಹೋಗಿ. ನಾನು ನಿಲ್ಲಿಸಲು ಹೇಳುವವರೆಗೂ ಮುಂದುವರಿಸಿ.",
    "ಈ ಅಂಕಿ ಅನುಕ್ರಮವನ್ನು ಗಮನಿಸಿ: 7, 3, 9, 1, 5, 8. ಈಗ ಅವುಗಳನ್ನು ಆರೋಹಣ ಕ್ರಮದಲ್ಲಿ ಹೇಳಿ.",
    "ನಿಮ್ಮ ಸ್ವಂತ ಊರು ಅಥವಾ ನಗರದ ಹೆಸರನ್ನು ಸಂಪೂರ್ಣ ಹಿಮ್ಮುಖವಾಗಿ ಉಚ್ಚರಿಸಿ, ಅದೇ ಸಮಯದಲ್ಲಿ ಹೆಬ್ಬೆರಳಿನಿಂದ ಮೇಜನ್ನು ನಿರಂತರವಾಗಿ ತಟ್ಟಿ.",
    "ಒಂದು ಮೌಲ್ಯಮಾಪನದಲ್ಲಿ 45 ಪ್ರಶ್ನೆಗಳಿವೆ. ನೀವು ಐದರಲ್ಲಿ ಎರಡು ಭಾಗ ಪ್ರಶ್ನೆಗಳಿಗೆ ತಪ್ಪು ಉತ್ತರ ನೀಡಿದರೆ, ಸರಿಯಾಗಿ ಎಷ್ಟು ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಿದಿರಿ?",
    "Z ಅಕ್ಷರದಿಂದ ಪ್ರಾರಂಭಿಸಿ ವರ್ಣಮಾಲೆಯನ್ನು ಹಿಮ್ಮುಖವಾಗಿ ಹೇಳಿ, ಆದರೆ ಪ್ರತಿ ಅಕ್ಷರದ ನಂತರ 1 ರಿಂದ ಪ್ರಾರಂಭಿಸುವ ಸಂಖ್ಯೆ ಹೇಳಿ. ಉದಾ: Z-1, Y-2. ವೇಗವಾಗಿ ಮಾಡಿ.",
],

}

# ══════════════════════════════════════════════════════════════════════════════
# RECOVERY
# ══════════════════════════════════════════════════════════════════════════════

_RECOVERY = {

"english": [
    "Tell me about your favourite hobby or what you like to do to unwind on weekends.",
    "What is a place you love visiting or would love to visit? Describe it.",
    "Tell me about a happy memory from your childhood.",
],

"tamil": [
    "உங்கள் நெறிய பொழுதுபோக்கு அல்லது வார இறுதியில் நீங்கள் ஓய்வெடுக்க விரும்புவதைப் பற்றி சொல்லுங்கள்.",
    "நீங்கள் விரும்பி செல்லும் அல்லது செல்ல விரும்பும் இடம் எது? அதை விவரிக்கவும்.",
    "உங்கள் குழந்தை பருவத்தில் இருந்து ஒரு மகிழ்ச்சியான நினைவைப் பற்றி சொல்லுங்கள்.",
],

"kannada": [
    "ನಿಮ್ಮ ನೆಚ್ಚಿನ ಹವ್ಯಾಸ ಅಥವಾ ವಾರಾಂತ್ಯದಲ್ಲಿ ವಿಶ್ರಾಂತಿ ತೆಗೆದುಕೊಳ್ಳಲು ನೀವು ಏನು ಮಾಡಲು ಇಷ್ಟಪಡುತ್ತೀರಿ ಎಂಬುದರ ಬಗ್ಗೆ ಹೇಳಿ.",
    "ನೀವು ಭೇಟಿ ಮಾಡಲು ಇಷ್ಟಪಡುವ ಅಥವಾ ಭೇಟಿ ಮಾಡಲು ಬಯಸುವ ಸ್ಥಳ ಯಾವುದು? ಅದನ್ನು ವಿವರಿಸಿ.",
    "ನಿಮ್ಮ ಬಾಲ್ಯದ ಸಂತೋಷದ ನೆನಪನ್ನು ಹೇಳಿ.",
],

}

# ══════════════════════════════════════════════════════════════════════════════
# PSS-10
# ══════════════════════════════════════════════════════════════════════════════

_PSS = {

"english": [
    "In the last month, how often have you been upset because of something that happened unexpectedly?",
    "In the last month, how often have you felt that you were unable to control the important things in your life?",
    "In the last month, how often have you felt nervous and stressed?",
    "In the last month, how often have you felt confident about your ability to handle your personal problems?",
    "In the last month, how often have you felt that things were going your way?",
    "In the last month, how often have you been able to control irritations in your life?",
    "In the last month, how often have you felt that you were on top of things?",
    "In the last month, how often have you been angered because of things that were outside of your control?",
    "In the last month, how often have you felt difficulties were piling up so high that you could not overcome them?",
    "In the last month, how often have you been able to control the way you spend your time?",
],

"tamil": [
    "கடந்த மாதம், எதிர்பாராத விதமாக நடந்த ஒன்றால் எத்தனை முறை மனம் வருந்தினீர்கள்?",
    "கடந்த மாதம், உங்கள் வாழ்வில் முக்கியமான விஷயங்களை கட்டுப்படுத்த முடியவில்லை என்று எத்தனை முறை உணர்ந்தீர்கள்?",
    "கடந்த மாதம், எத்தனை முறை பதட்டமாகவும் மன அழுத்தத்திலும் இருந்தீர்கள்?",
    "கடந்த மாதம், உங்கள் தனிப்பட்ட பிரச்சனைகளை சமாளிக்கும் திறனில் எத்தனை முறை நம்பிக்கையாக இருந்தீர்கள்?",
    "கடந்த மாதம், விஷயங்கள் உங்களுக்கு சாதகமாக நடக்கின்றன என்று எத்தனை முறை உணர்ந்தீர்கள்?",
    "கடந்த மாதம், உங்கள் வாழ்வில் எரிச்சல்களை எத்தனை முறை கட்டுப்படுத்த முடிந்தது?",
    "கடந்த மாதம், நீங்கள் எல்லாவற்றையும் கட்டுப்பாட்டில் வைத்திருக்கிறீர்கள் என்று எத்தனை முறை உணர்ந்தீர்கள்?",
    "கடந்த மாதம், உங்கள் கட்டுப்பாட்டிற்கு வெளியே உள்ள விஷயங்களால் எத்தனை முறை கோபமடைந்தீர்கள்?",
    "கடந்த மாதம், சிரமங்கள் மிகவும் அதிகமாக குவிந்து வருகின்றன என்று எத்தனை முறை உணர்ந்தீர்கள்?",
    "கடந்த மாதம், உங்கள் நேரத்தை எப்படி செலவிடுகிறீர்கள் என்பதை எத்தனை முறை கட்டுப்படுத்த முடிந்தது?",
],

"kannada": [
    "ಕಳೆದ ತಿಂಗಳಲ್ಲಿ, ಅನಿರೀಕ್ಷಿತವಾಗಿ ಸಂಭವಿಸಿದ ಯಾವುದಾದರೂ ಕಾರಣದಿಂದ ನೀವು ಎಷ್ಟು ಬಾರಿ ಮನನೊಂದಿದ್ದೀರಿ?",
    "ಕಳೆದ ತಿಂಗಳಲ್ಲಿ, ನಿಮ್ಮ ಜೀವನದ ಪ್ರಮುಖ ವಿಷಯಗಳನ್ನು ನಿಯಂತ್ರಿಸಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ ಎಂದು ಎಷ್ಟು ಬಾರಿ ಅನ್ನಿಸಿದೆ?",
    "ಕಳೆದ ತಿಂಗಳಲ್ಲಿ, ನೀವು ಎಷ್ಟು ಬಾರಿ ಆತಂಕ ಮತ್ತು ಒತ್ತಡ ಅನುಭವಿಸಿದ್ದೀರಿ?",
    "ಕಳೆದ ತಿಂಗಳಲ್ಲಿ, ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ಸಮಸ್ಯೆಗಳನ್ನು ನಿಭಾಯಿಸಲು ಎಷ್ಟು ಬಾರಿ ಆತ್ಮವಿಶ್ವಾಸ ಅನ್ನಿಸಿತು?",
    "ಕಳೆದ ತಿಂಗಳಲ್ಲಿ, ವಿಷಯಗಳು ನಿಮ್ಮ ಅನುಕೂಲಕ್ಕೆ ತಕ್ಕಂತೆ ನಡೆಯುತ್ತಿವೆ ಎಂದು ಎಷ್ಟು ಬಾರಿ ಅನ್ನಿಸಿತು?",
    "ಕಳೆದ ತಿಂಗಳಲ್ಲಿ, ನಿಮ್ಮ ಜೀವನದಲ್ಲಿ ಕಿರಿಕಿರಿಗಳನ್ನು ಎಷ್ಟು ಬಾರಿ ನಿಯಂತ್ರಿಸಲು ಸಾಧ್ಯವಾಯಿತು?",
    "ಕಳೆದ ತಿಂಗಳಲ್ಲಿ, ನೀವು ಎಲ್ಲವನ್ನೂ ನಿಯಂತ್ರಣದಲ್ಲಿ ಇಟ್ಟಿದ್ದೀರಿ ಎಂದು ಎಷ್ಟು ಬಾರಿ ಅನ್ನಿಸಿತು?",
    "ಕಳೆದ ತಿಂಗಳಲ್ಲಿ, ನಿಮ್ಮ ನಿಯಂತ್ರಣದ ಹೊರಗಿದ್ದ ವಿಷಯಗಳಿಂದ ಎಷ್ಟು ಬಾರಿ ಕೋಪಗೊಂಡಿದ್ದೀರಿ?",
    "ಕಳೆದ ತಿಂಗಳಲ್ಲಿ, ತೊಂದರೆಗಳು ತುಂಬಾ ಹೆಚ್ಚಾಗಿ ಪೇರಿಸಿಕೊಳ್ಳುತ್ತಿವೆ ಎಂದು ಎಷ್ಟು ಬಾರಿ ಅನ್ನಿಸಿತು?",
    "ಕಳೆದ ತಿಂಗಳಲ್ಲಿ, ನಿಮ್ಮ ಸಮಯವನ್ನು ಹೇಗೆ ಕಳೆಯುತ್ತೀರಿ ಎಂಬುದನ್ನು ಎಷ್ಟು ಬಾರಿ ನಿಯಂತ್ರಿಸಲು ಸಾಧ್ಯವಾಯಿತು?",
],

}

# ── PSS scale options ──────────────────────────────────────────────────────────

_PSS_OPTIONS = {
    "english": ["0 – Never", "1 – Almost Never", "2 – Sometimes", "3 – Fairly Often", "4 – Very Often"],
    "tamil":   ["0 – ஒருபோதும் இல்லை", "1 – கிட்டத்தட்ட இல்லை", "2 – சில சமயம்", "3 – அடிக்கடி", "4 – மிகவும் அடிக்கடி"],
    "kannada": ["0 – ಎಂದಿಗೂ ಇಲ್ಲ", "1 – ಬಹುತೇಕ ಇಲ್ಲ", "2 – ಕೆಲವೊಮ್ಮೆ", "3 – ಸಾಕಷ್ಟು ಬಾರಿ", "4 – ತುಂಬಾ ಬಾರಿ"],
}

# ── Consent text ───────────────────────────────────────────────────────────────

CONSENT_TEXT = {
    "english": (
        "I explicitly consent to the collection and commercial processing of my "
        "anonymised video/audio features for product development. I also state that "
        "I am above 18 years and legally allowed to take this test and accept this consent."
    ),
    "tamil": (
        "தயாரிப்பு மேம்பாட்டிற்காக என்னுடைய அநாமதேய வீடியோ/ஆடியோ அம்சங்களை சேகரிக்கவும் "
        "வணிக ரீதியாக செயலாக்கவும் நான் வெளிப்படையாக சம்மதிக்கிறேன். "
        "நான் 18 வயதுக்கு மேற்பட்டவன்/மேற்பட்டவள் மற்றும் இந்த சோதனையை எடுக்க சட்டப்பூர்வமாக "
        "அனுமதிக்கப்பட்டவன்/அனுமதிக்கப்பட்டவள் என்றும் இந்த சம்மதத்தை ஏற்றுக்கொள்கிறேன் என்றும் கூறுகிறேன்."
    ),
    "kannada": (
        "ಉತ್ಪನ್ನ ಅಭಿವೃದ್ಧಿಗಾಗಿ ನನ್ನ ಅನಾಮಧೇಯ ವೀಡಿಯೋ/ಆಡಿಯೋ ವೈಶಿಷ್ಟ್ಯಗಳ ಸಂಗ್ರಹ ಮತ್ತು ವಾಣಿಜ್ಯ ಸಂಸ್ಕರಣೆಗೆ "
        "ನಾನು ಸ್ಪಷ್ಟವಾಗಿ ಒಪ್ಪಿಗೆ ನೀಡುತ್ತೇನೆ. "
        "ನಾನು 18 ವರ್ಷಕ್ಕಿಂತ ಹೆಚ್ಚಿನ ವಯಸ್ಸಿನವನು/ಳು ಮತ್ತು ಈ ಪರೀಕ್ಷೆ ತೆಗೆದುಕೊಳ್ಳಲು ಕಾನೂನುಬದ್ಧವಾಗಿ "
        "ಅನುಮತಿ ಪಡೆದವನು/ಳು ಎಂದು ಹೇಳಿ ಈ ಒಪ್ಪಿಗೆಯನ್ನು ಒಪ್ಪುತ್ತೇನೆ."
    ),
}

# ── UI labels ──────────────────────────────────────────────────────────────────

UI_LABELS = {
    "english": {
        "consent_title":    "Informed Consent",
        "consent_check":    "I have read and I accept the consent statement above",
        "name_prompt":      "Please enter your full name:",
        "proceed":          "Proceed  →",
        "next_q":           "Next Question  →",
        "restart":          "↺  Restart Question",
        "recording":        "🔴  Recording — please respond now",
        "reading":          "🔊  Avatar is reading the question…",
        "prepare_social":   "Prepare — recording starts in",
        "prepare_cog":      "Get ready — recording starts in",
        "pause_warning":    "⏸  More than 3 seconds of silence — please press Restart.",
        "wrong_answer":     "⚠  Incorrect answer — please press Restart and try again.",
        "response_time":    "Response time (sec):",
        "pss_title":        "Perceived Stress Scale (PSS-10)",
        "pss_instruction":  "Choose how often you felt this way in the last month.",
        "pss_submit":       "Submit PSS Test",
        "session_complete": "Session Complete",
        "thank_you":        "Thank you for participating.\nAll recordings and results have been saved.",
    },
    "tamil": {
        "consent_title":    "தகவல் அறிவிக்கப்பட்ட சம்மதம்",
        "consent_check":    "மேலே உள்ள சம்மத அறிக்கையை படித்து ஏற்றுக்கொள்கிறேன்",
        "name_prompt":      "உங்கள் முழு பெயரை உள்ளிடவும்:",
        "proceed":          "தொடர்க  →",
        "next_q":           "அடுத்த கேள்வி  →",
        "restart":          "↺  மீண்டும் தொடங்கு",
        "recording":        "🔴  பதிவு நடக்கிறது — இப்போது பதில் சொல்லுங்கள்",
        "reading":          "🔊  அவதார் கேள்வியை படிக்கிறது…",
        "prepare_social":   "தயாராகுங்கள் — பதிவு தொடங்கும் நேரம்",
        "prepare_cog":      "ஆயத்தமாகுங்கள் — பதிவு தொடங்கும் நேரம்",
        "pause_warning":    "⏸  3 வினாடிகளுக்கும் அதிகமான மௌனம் — மீண்டும் தொடங்கவும்.",
        "wrong_answer":     "⚠  தவறான பதில் — மீண்டும் தொடங்கி முயற்சிக்கவும்.",
        "response_time":    "பதில் நேரம் (வினாடி):",
        "pss_title":        "உணரப்பட்ட மன அழுத்த அளவுகோல் (PSS-10)",
        "pss_instruction":  "கடந்த மாதம் எவ்வளவு அடிக்கடி இந்த உணர்வு இருந்தது என்பதை தேர்வு செய்யவும்.",
        "pss_submit":       "PSS சோதனையை சமர்ப்பிக்கவும்",
        "session_complete": "அமர்வு முடிந்தது",
        "thank_you":        "பங்கேற்றதற்கு நன்றி.\nஅனைத்து பதிவுகளும் முடிவுகளும் சேமிக்கப்பட்டன.",
    },
    "kannada": {
        "consent_title":    "ಮಾಹಿತಿಯುಕ್ತ ಒಪ್ಪಿಗೆ",
        "consent_check":    "ಮೇಲಿನ ಒಪ್ಪಿಗೆ ಹೇಳಿಕೆಯನ್ನು ಓದಿ ಸ್ವೀಕರಿಸುತ್ತೇನೆ",
        "name_prompt":      "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪೂರ್ತಿ ಹೆಸರು ನಮೂದಿಸಿ:",
        "proceed":          "ಮುಂದುವರಿಸು  →",
        "next_q":           "ಮುಂದಿನ ಪ್ರಶ್ನೆ  →",
        "restart":          "↺  ಮರು ಪ್ರಾರಂಭಿಸು",
        "recording":        "🔴  ರೆಕಾರ್ಡಿಂಗ್ — ಈಗ ಉತ್ತರಿಸಿ",
        "reading":          "🔊  ಅವತಾರ್ ಪ್ರಶ್ನೆ ಓದುತ್ತಿದ್ದಾರೆ…",
        "prepare_social":   "ಸಿದ್ಧರಾಗಿ — ರೆಕಾರ್ಡಿಂಗ್ ಪ್ರಾರಂಭವಾಗಲು",
        "prepare_cog":      "ಸಿದ್ಧರಾಗಿ — ರೆಕಾರ್ಡಿಂಗ್ ಪ್ರಾರಂಭವಾಗಲು",
        "pause_warning":    "⏸  3 ಸೆಕೆಂಡ್‌ಗಿಂತ ಹೆಚ್ಚು ಮೌನ — ದಯವಿಟ್ಟು ಮರು ಪ್ರಾರಂಭಿಸಿ.",
        "wrong_answer":     "⚠  ತಪ್ಪು ಉತ್ತರ — ಮರು ಪ್ರಾರಂಭಿಸಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "response_time":    "ಪ್ರತಿಕ್ರಿಯೆ ಸಮಯ (ಸೆಕೆಂಡ್):",
        "pss_title":        "ಗ್ರಹಿಸಿದ ಒತ್ತಡ ಮಾಪಕ (PSS-10)",
        "pss_instruction":  "ಕಳೆದ ತಿಂಗಳಲ್ಲಿ ಈ ಭಾವನೆ ಎಷ್ಟು ಬಾರಿ ಇತ್ತು ಎಂಬುದನ್ನು ಆಯ್ಕೆ ಮಾಡಿ.",
        "pss_submit":       "PSS ಪರೀಕ್ಷೆ ಸಲ್ಲಿಸಿ",
        "session_complete": "ಅಧಿವೇಶನ ಪೂರ್ಣಗೊಂಡಿದೆ",
        "thank_you":        "ಭಾಗವಹಿಸಿದ್ದಕ್ಕೆ ಧನ್ಯವಾದಗಳು.\nಎಲ್ಲಾ ರೆಕಾರ್ಡಿಂಗ್‌ಗಳು ಮತ್ತು ಫಲಿತಾಂಶಗಳನ್ನು ಉಳಿಸಲಾಗಿದೆ.",
    },
}

# ── PSS scoring constants (language-independent) ───────────────────────────────
PSS_REVERSED = {3, 4, 5, 6, 9}

# ══════════════════════════════════════════════════════════════════════════════
# Public API
# ══════════════════════════════════════════════════════════════════════════════

def get_questions(phase: str, lang: str = "english") -> list:
    """Return question list for a phase in the requested language."""
    lang = lang.lower()
    banks = {
        "baseline":         _BASELINE,
        "social_stress":    _SOCIAL_STRESS,
        "cognitive_stress": _COGNITIVE,
        "recovery":         _RECOVERY,
        "pss":              _PSS,
    }
    bank = banks.get(phase, _BASELINE)
    return bank.get(lang, bank["english"])

def get_pss_options(lang: str = "english") -> list:
    return _PSS_OPTIONS.get(lang, _PSS_OPTIONS["english"])

def get_consent_text(lang: str = "english") -> str:
    return CONSENT_TEXT.get(lang, CONSENT_TEXT["english"])

def get_ui_labels(lang: str = "english") -> dict:
    return UI_LABELS.get(lang, UI_LABELS["english"])

# Legacy aliases so old imports still work without changes
BASELINE_QUESTIONS       = _BASELINE["english"]
SOCIAL_STRESS_QUESTIONS  = _SOCIAL_STRESS["english"]
COGNITIVE_QUESTIONS      = _COGNITIVE["english"]
RECOVERY_QUESTIONS       = _RECOVERY["english"]
PSS_QUESTIONS            = _PSS["english"]
PSS_OPTIONS              = _PSS_OPTIONS["english"]
